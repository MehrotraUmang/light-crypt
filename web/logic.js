var returnedListGlobal = []
function getList() {
    var pText;
    pText = textInp.value;
    eel.process(pText)(function (returnedList) {
        returnedListGlobal = returnedList;
        document.getElementById('textInp').innerHTML = returnedListGlobal[4];
        document.getElementById('eccprvkey').innerHTML = returnedListGlobal[0];
        document.getElementById('eccpubkey').innerHTML = returnedListGlobal[1];
        document.getElementById('aeskey').innerHTML = returnedListGlobal[2];
        document.getElementById('ciphertext').innerHTML = returnedListGlobal[3]

    });
}

function getMessage() {
    document.getElementById('plaintext').innerHTML = returnedListGlobal[4];
}
