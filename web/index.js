async function getDataFromPython() {
    document.getElementById("eccprkey").innerText = await eel.process()();
}


document.getElementById('encrypt').addEventListener('click', async () => {
    getDataFromPython();
    await eel.process(document.getElementById("taskinp").value)
    document.getElementById("eccprkey").value = privKey;
    document.getElementById("eccpkey").value = "pubkey";
    document.getElementById("aeskey").value = "b'\xf5\x8a+9\xc3@-\xeao\xb8\xe8!Y\xe2\xbc\xe8\xa6\xb30i \xa1\x00\xd1%\xf3\xa2\x8c64\\\xf7'";
    document.getElementById("ciphertext").value = "0x7be475547d3052c8ed5f3803ebf7f4fb277639b91e64d96bc995ca1f0e7508f21";
})


document.getElementById('decrypt').addEventListener('click', async () => {
    // await eel.send_data('Hello from JS');
    document.getElementById("plaintext").value = "hello world"
})


document.getElementById('reset').addEventListener('click', async () => {
    document.getElementById("taskinp").value = ""
    document.getElementById("eccprkey").value = ""
    document.getElementById("eccpkey").value = ""
    document.getElementById("aeskey").value = ""
    document.getElementById("ciphertext").value = ""
    document.getElementById("plaintext").value = ""
})