function getList() {
    eel.process(taskinp.value)(function (my_list) {
        document.getElementById('eccprvkey').innerHTML = my_list[0];
        document.getElementById('eccpubkey').innerHTML = my_list[1];
        document.getElementById('aeskey').innerHTML = my_list[2];
        document.getElementById('ciphertext').innerHTML = my_list[3]
        document.getElementById('');
    });
}

function getMessage() {
    eel.process(taskinp.value)(
        function (my_list1) {
        document.getElementById('plaintext').innerHTML = my_list1[4];
    });
}
