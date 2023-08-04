import csv
import os
from faker import Faker

# Ensure the "generated" directory exists
if not os.path.exists('generated'):
    os.makedirs('generated')

# Example usage:
# generate_csv(num_rows=10, num_columns=5)
def generate_csv(num_rows, num_columns, filename='random_dataset.csv'):
    fake = Faker()
    header = [f"Column_{i}" for i in range(1, num_columns + 1)]
    data = []

    for _ in range(num_rows):
        row = [fake.pyfloat(left_digits=3, right_digits=2, positive=True) 
               for _ in range(num_columns)]
        data.append(row)

    filepath = os.path.join('generated', filename)
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)

    print(f"Generated {num_rows} rows and {num_columns} columns of fake data in {filepath}")

# Example usage:
# generate_txt(num_tokens=100, filename="random_text.txt")
def generate_txt(num_tokens, filename='random_text.txt'):
    fake = Faker()
    words_list = fake.words(num_tokens)
    text = ' '.join(words_list)
    
    filepath = os.path.join('generated', filename)
    with open(filepath, 'w') as file:
        file.write(str(text))

    print(f'Generated {num_tokens} tokens into {filepath}')
