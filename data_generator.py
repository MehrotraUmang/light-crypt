'''
# Example usage:
data_generator = DataGenerator()

# Generate a CSV file with 10 rows and 5 columns
data_generator.generate_csv(num_rows=10, num_columns=5, filename='sample_dataset.csv')

# Generate a text file with 100 tokens
data_generator.generate_txt(num_tokens=100, filename='sample_text.txt')
'''
import csv
import os
from faker import Faker

class DataGenerator:
    def __init__(self, output_directory='generated'):
        self.output_directory = output_directory

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def generate_csv(self, num_rows, num_columns, filename='random_dataset.csv'):
        """
        Generate a CSV file with fake data.

        Args:
            num_rows (int): Number of rows in the CSV.
            num_columns (int): Number of columns in the CSV.
            filename (str, optional): Name of the generated CSV file. Defaults to 'random_dataset.csv'.
        """
        fake = Faker()
        header = [f"Column_{i}" for i in range(1, num_columns + 1)]
        data = []

        for _ in range(num_rows):
            row = [fake.pyfloat(left_digits=3, right_digits=2, positive=True) 
                   for _ in range(num_columns)]
            data.append(row)

        filepath = os.path.join(self.output_directory, filename)
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(data)
    
    def generate_txt(self, num_tokens, filename='random_text.txt'):
        """
        Generate a text file with fake text.

        Args:
            num_tokens (int): Number of tokens (words) in the text.
            filename (str, optional): Name of the generated text file. Defaults to 'random_text.txt'.
        """
        fake = Faker()
        words_list = fake.words(num_tokens)
        text = ' '.join(words_list)
        
        filepath = os.path.join(self.output_directory, filename)
        with open(filepath, 'w') as file:
            file.write(str(text))
