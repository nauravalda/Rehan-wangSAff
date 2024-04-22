import flet as ft
import base64
from time import time
# from random import randbytes
import struct
import RSA as rsa

# async def genkey():
#     return ((210617, 266207), (65537, 266207))
# async def encrypt():
#     return randbytes(3)
# async def decrypt_file():
#     return randbytes(2)
# async def decrypt_text():
#     return "Budi Wangsaf"

async def main(page: ft.Page):

    # User data

    alice = {
        "name": "Alice",
        "privkey": None,
        "pubkey": None,
        "keyFilename": None,
        "friendkey": None,
        "friendkeyFilename": None,
        "rcvType": None, # None, "text", or "file"
        "rcvCipher": None,
        "rcvPlain": None,
        "rcvFilename": None,
        "sendFile": False,
        "sendPlain": None,
        "sendCipher": None,
        "sendFilename": None,
        "sendFilepath": None
    }
    bob = {
        "name": "Bob",
        "privkey": None,
        "pubkey": None,
        "keyFilename": None,
        "friendkey": None,
        "friendkeyFilename": None,
        "rcvType": None, # None, "text", or "file"
        "rcvCipher": None,
        "rcvPlain": None,
        "rcvFilename": None,
        "sendFile": False,
        "sendPlain": None,
        "sendCipher": None,
        "sendFilename": None,
        "sendFilepath": None
    }
    sender = alice
    recipient = bob
    

    # Handlers

    async def handleChangeUser(e:ft.ControlEvent):
        nonlocal sender, recipient
        sender, recipient = recipient, sender
        keyStatusText.value = "No key selected" if sender["privkey"] is None else "Ready"
        keySave.visible = False if sender["privkey"] is None else True
        friendKeyStatusText.value = "No key received" if sender["friendkey"] is None else "Ready"
        friendKeySave.visible = False if sender["friendkey"] is None else True
        if sender["rcvType"] is None:
            rcvNone.visible = True
            rcvText.visible = rcvFile.visible = False
        elif sender["rcvType"] == "text":
            rcvText.visible = True
            rcvNone.visible = rcvFile.visible = False
            base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
            cipherB64 = ""
            for i in sender["rcvCipher"]:
                cipherB64 = cipherB64 + base64_chars[i]
            rcvTextBox.value = cipherB64
        else:
            rcvFile.visible = True
            rcvText.visible = rcvNone.visible = False
            rcvFileInfo.value = sender["rcvFilename"]
        sendTextBox.value = ""
        sender["sendFilename"] = sender["sendFilepath"] = None
        sendFileInfo.value = ""
        content.update()
        

    async def handleChangeInput(e):
        sendFileBox.visible, sendTextBox.visible = sendTextBox.visible, sendFileBox.visible
        sendBox.update()

    async def handleKeyUpload(e):
        # privkey file format: (e,d,n)
        with open(e.files[0].path,'r') as f:
            key = eval(f.read())
        sender["privkey"] = (key[1], key[2])
        sender["pubkey"] = (key[0], key[2])
        sender["keyFilename"] = e.files[0].name
        keyStatusText.value = "Ready"
        keySave.visible = True
        selfKey.update()
        return
    
    async def handleGenerateKey(e): # mengubah penampilan (done)
        key = rsa.generate_key_pair()
        sender["privkey"]=key[0]
        sender["pubkey"]=key[1]
        keyStatusText.value = "Ready"
        keySave.visible = True
        selfKey.update()
        return
    
    async def handlePriKeySave(e):
        filename = f"/key_{int(time())}.pri"
        key = (sender["pubkey"][0], sender["privkey"][0], sender["privkey"][1])
        with open(e.path+filename, "w") as f:
            f.write(key)
        return
    
    async def handlePubKeySave(e):
        filename = f"/key_{int(time())}.pub"
        with open(e.path+filename, "w") as f:
            f.write(str(sender["pubkey"]))
        return
    
    async def handleFriendKeyUpload(e):
        with open(e.files[0].path,'r') as f:
            sender["friendkey"] = eval(f.read())
        sender["friendkeyFilename"] = e.files[0].name
        friendKeyStatusText.value = "Ready"
        friendKeySave.visible = True
        friendKey.update()
        return
    
    async def handleFriendKeySave(e):
        filename = f"/key_{int(time())}.pub"
        with open(e.path+filename, "w") as f:
            f.write(str(sender["friendkey"]))
        return
    
    async def handleRcvTextSave(e):
        if e.control.value == "Show decrypted message":
            filename = f"/message_{int(time())}.bin"
            with open(e.path+filename,'wb') as f:
                for i in sender["rcvCipher"]:
                    f.write(struct.pack('I',i))
        else:
            filename = f"/message_{int(time())}.txt"
            with open(e.path+filename,'w') as f:
                f.write(sender["rcvPlain"])
        return
    
    async def handleRcvFileSave(e):

        filename = f"/message_{int(time())}.bin"
        with open(e.path, 'rb') as f:
            data = f.read()
            num_integers = len(data) // 4
            ciphertext_in_file = struct.unpack(f"{num_integers}I", data)
            plaintext = rsa.decrypt(sender["privkey"], ciphertext_in_file)
            with open(e.path+filename, 'wb') as f:
                f.write(plaintext)
        return
    
    async def handleRcvRawSave(e):
        filename = f"/message_{int(time())}.bin"
        with open(e.path+filename,'wb') as f:
            for i in sender["rcvCipher"]:
                f.write(struct.pack('I',i))
        return
    
    async def handleSendFileUpload(e): # mengubah penampilan
        sender["sendFilename"] = e.files[0].name
        sender["sendFilepath"] = e.files[0].path
        sendFileInfo.value = sender["sendFilename"]
        sendFileInfo.update()
        return
    
    async def handleSendKey(e):
        recipient["friendkey"] = sender["pubkey"]
        return

    async def handleRcvText(e): # mengubah penampilan (done)
        if e.control.value == "Show decrypted message": # butuh tambah decrypt di sini (done)

            sender["rcvPlain"] = rsa.decrypt(sender["privkey"], sender["rcvCipher"]).decode('utf-8')
            
            rcvTextBox.value = sender["rcvPlain"]
            e.control.value = "Show original message"
        else:
            rcvTextBox.value = sender["rcvCipher"]
            e.control.value = "Show decrypted message"
        rcvText.update()
        return
    
    async def handleEncryptSave(e): # butuh tambah decrypt di sini (done)
        if sendTextBox.visible:
            sender["sendPlain"] = sendTextBox.value
            text_base64 = str(base64.b64encode(sender["sendPlain"].encode('utf-8')).decode('utf-8'))
            ciphertext = rsa.encrypt(sender["pubkey"], text_base64)
            filename = f"/encrypted_{int(time())}.bin"
            with open(e.path+filename,'wb') as f:
                for i in ciphertext:
                    f.write(struct.pack('I',i))
        else:
            with open(sender["sendFilepath"], 'rb') as file:
                data = file.read()
                base64_data = base64.b64encode(data).decode('utf-8')
                ciphertext = rsa.encrypt(sender["pubkey"], base64_data)
                filename = "/"+sender["sendFilename"]+".bin"
                with open(e.path+filename, 'wb') as file:
                    for integer in ciphertext:
                        file.write(struct.pack('I', integer))
            
        return
    
    async def handleEncryptSend(e): # butuh tambah decrypt di sini (done)
        nonlocal recipient
        if sendTextBox.visible:
            text_base64 = str(base64.b64encode((sendTextBox.value).encode('utf-8')).decode('utf-8'))
            recipient["rcvCipher"] = rsa.encrypt(recipient["pubkey"].text_base64)
            recipient["rcvType"] = "text"
        else:
            data_base64 = str(base64.b64encode((sender["sendFilename"]).encode('utf-8')).decode('utf-8'))
            recipient["rcvCipher"] = rsa.encrypt(recipient["pubkey"], data_base64)
            recipient["rcvType"] = "file"
            recipient["rcvFilename"] = sender["sendFilename"]
        return
    
    # Components
    
    ## File picker
    keyUploader = ft.FilePicker(on_result=handleKeyUpload)
    priKeyDownloader = ft.FilePicker(on_result=handlePriKeySave)
    pubKeyDownloader = ft.FilePicker(on_result=handlePubKeySave)
    friendKeyUploader = ft.FilePicker(on_result=handleFriendKeyUpload)
    friendKeyDownloader = ft.FilePicker(on_result=handleFriendKeySave)
    rcvTextDownloader = ft.FilePicker(on_result=handleRcvTextSave)
    rcvFileDownloader = ft.FilePicker(on_result=handleRcvFileSave)
    rcvRawDownloader = ft.FilePicker(on_result=handleRcvRawSave)
    sendFileUploader = ft.FilePicker(on_result=handleSendFileUpload)
    sendFileDownloader = ft.FilePicker(on_result=handleEncryptSave)

    page.overlay.append(keyUploader)
    page.overlay.append(priKeyDownloader)
    page.overlay.append(pubKeyDownloader)
    page.overlay.append(friendKeyDownloader)
    page.overlay.append(friendKeyUploader)
    page.overlay.append(rcvTextDownloader)
    page.overlay.append(rcvFileDownloader)
    page.overlay.append(rcvRawDownloader)
    page.overlay.append(sendFileUploader)
    page.overlay.append(sendFileDownloader)

    ## User switch
    userSwitch = ft.Row(
        [
            ft.Text("Alice", size=18),
            ft.Switch(value=False,on_change=handleChangeUser),
            ft.Text("Bob", size=18)
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )

    ## Self key
    keyStatusText = ft.Text("No key selected", size=18)
    keyStatus = ft.Row(
        [
            ft.Text("Key status: ", size=18),
            keyStatusText
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )
    keyGen = ft.FilledButton("Generate Key", on_click=handleGenerateKey)
    keyUpload = ft.FilledTonalButton("Upload Private Key", on_click=keyUploader.pick_files)
    keySend = ft.FilledButton("Send Public Key", on_click=handleSendKey)
    keyPriSave = ft.FilledButton("Save Private Key", on_click=priKeyDownloader.get_directory_path)
    keyPubSave = ft.FilledTonalButton("Save Public Key", on_click=pubKeyDownloader.get_directory_path)
    keySave = ft.Row(
                [
                    keyPriSave,
                    keyPubSave
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                visible = False
    )
    selfKey = ft.Column(
        [
            keyStatus,
            ft.Row(
                [
                    keyGen,
                    keyUpload
                ],
                alignment = ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    keySend
                ],
                alignment = ft.MainAxisAlignment.CENTER
            ),
            keySave
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )

    ## Friend key
    friendKeyStatusText = ft.Text("No key received", size=18)
    friendKeyStatus = ft.Row(
        [
            ft.Text("Friend key status: ", size=18),
            friendKeyStatusText
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )
    friendKeySave = ft.FilledButton("Upload Public Key", on_click=friendKeyUploader.pick_files, visible=False)
    friendKeyUpload = ft.FilledTonalButton("Save Public Key", on_click=friendKeyDownloader.get_directory_path)
    friendKey = ft.Column(
        [
            friendKeyStatus,
            ft.Row(
                [
                    friendKeySave,
                    friendKeyUpload
                ],
                alignment = ft.MainAxisAlignment.CENTER
            )
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )

    ## Received message
    rcvNone = ft.TextField(label = "Received message", multiline=True, max_lines=6, read_only=True, value="No message received")
    rcvTextBox = ft.TextField(label = "Received message", multiline=True, max_lines=6, read_only=True)
    rcvTextSave = ft.FilledTonalButton("Save to file", on_click=rcvTextDownloader.get_directory_path)
    rcvTextButton = ft.FilledButton("Show decrypted message", on_click=handleRcvText)
    rcvText = ft.Column(
        [
            rcvTextBox,
            ft.Row(
                [
                    rcvTextSave,
                    rcvTextButton
                ],
                alignment = ft.MainAxisAlignment.CENTER
            )
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        visible = False
    )
    rcvFileInfo = ft.TextField(label = "Filename", multiline=True, max_lines=6, read_only=True)
    rcvFileRaw = ft.FilledTonalButton("Download encrypted file", on_click=rcvRawDownloader.get_directory_path)
    rcvFileDecrypt = ft.FilledButton("Download file", on_click=rcvFileDownloader.get_directory_path)
    rcvFile = ft.Column(
        [
            rcvFileInfo,
            ft.Row(
                [
                    rcvFileRaw,
                    rcvFileDecrypt
                ],
                alignment = ft.MainAxisAlignment.CENTER
            )
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        visible = False
    )
    rcvItem = ft.Column(
        [
            rcvNone,
            rcvText,
            rcvFile
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )

    ## Send message
    sendSwitch = ft.Row(
        [
            ft.Text("Upload file", size=18),
            ft.Switch(value=False, on_change=handleChangeInput),
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )
    sendTextBox = ft.TextField(label="Input text", multiline=True,max_lines=8)
    sendFileButton = ft.FilledButton("Select a file", on_click=sendFileUploader.pick_files)
    sendFileInfo = ft.Text("No file selected")
    sendFileBox = ft.Row(
        [
            sendFileButton,
            sendFileInfo
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        visible=False
    )
    sendSaveButton = ft.FilledTonalButton("Encrypt and Save", on_click=sendFileDownloader.get_directory_path)
    sendButton = ft.FilledButton("Encrypt and Send", on_click=handleEncryptSend)
    sendBox = ft.Column(
        [
            sendSwitch,
            sendTextBox,
            sendFileBox,
            ft.Row(
                [sendSaveButton, sendButton],
                alignment = ft.MainAxisAlignment.CENTER
            )
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )

    # Main content

    content = ft.SafeArea (
        ft.Container (
            ft.Column(
                [
                    ft.Text("Wangsaff",size=36),
                    userSwitch,
                    ft.Divider(),
                    selfKey,
                    ft.Divider(),
                    friendKey,
                    ft.Divider(),
                    rcvItem,
                    ft.Divider(),
                    sendBox
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
            )
        )
    )
    page.add(content)
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # page.banner = ft.Banner(
    #     content=ft.Text(""),
    #     actions=[
    #         ft.TextButton("x", on_click=close_banner),
    #     ],
    # )

ft.app(target=main)