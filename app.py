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
        keySend.visible = keySave.visible = False if sender["privkey"] is None else True
        friendKeyStatusText.value = "No key received" if sender["friendkey"] is None else "Ready"
        sendButtons.visible = friendKeySave.visible = False if sender["friendkey"] is None else True
        if sender["rcvType"] is None:
            rcvNone.visible = True
            rcvText.visible = rcvFile.visible = False
        elif sender["rcvType"] == "text":
            rcvText.visible = True
            rcvNone.visible = rcvFile.visible = False
            cipherB64 = ""
            for i in sender["rcvCipher"]:
                cipherB64 = cipherB64 + str(i)
            rcvTextBox.value = base64.b64encode(cipherB64.encode()).decode()
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
        keySend.visible = keySave.visible = True
        selfKey.update()
        await alert(f"Private key successfully uploaded.")
        return
    
    async def handleGenerateKey(e):
        key = rsa.generate_key_pair()
        sender["privkey"]=key[1]
        sender["pubkey"]=key[0]
        keyStatusText.value = "Ready"
        keySend.visible = keySave.visible = True
        selfKey.update()
        await alert(f"Private key successfully generated.")
        return
    
    async def handlePriKeySave(e):
        filename = f"/key_{int(time())}.pri"
        key = (sender["pubkey"][0], sender["privkey"][0], sender["privkey"][1])
        with open(e.path+filename, "w") as f:
            f.write(str(key))
        await alert(f"Successfully saved at {e.path+filename}")
        return
    
    async def handlePubKeySave(e):
        filename = f"/key_{int(time())}.pub"
        with open(e.path+filename, "w") as f:
            f.write(str(sender["pubkey"]))
        await alert(f"Successfully saved at {e.path+filename}")
        return
    
    async def handleFriendKeyUpload(e):
        with open(e.files[0].path,'r') as f:
            sender["friendkey"] = eval(f.read())
        sender["friendkeyFilename"] = e.files[0].name
        friendKeyStatusText.value = "Ready"
        sendButtons.visible = friendKeySave.visible = True
        friendKey.update()
        await alert(f"Friend public key successfully uploaded.")
        return
    
    async def handleFriendKeySave(e):
        filename = f"/key_{int(time())}.pub"
        with open(e.path+filename, "w") as f:
            f.write(str(sender["friendkey"]))
        await alert(f"Successfully saved at {e.path+filename}")
        return
    
    async def handleRcvTextSave(e):
        if e.control.text == "Show decrypted message":
            filename = f"/message_{int(time())}.bin"
            with open(e.path+filename,'wb') as f:
                for i in sender["rcvCipher"]:
                    f.write(struct.pack('I',i))
        else:
            filename = f"/message_{int(time())}.txt"
            with open(e.path+filename,'w') as f:
                f.write(sender["rcvPlain"])
        await alert(f"Successfully saved at {e.path+filename}")
        return
    
    async def handleRcvFileSave(e):
        filename = f"/{sender['rcvFilename']}"
        sender["rcvPlain"] = rsa.decrypt(sender["privkey"],sender["rcvCipher"])
        with open(e.path+filename, 'wb') as f:
            f.write(sender["rcvPlain"])
        await alert(f"Successfully decrypted & saved at {e.path+filename}")
        return
    
    async def handleRcvRawSave(e):
        filename = f"/message_{int(time())}.bin"
        with open(e.path+filename,'wb') as f:
            for i in sender["rcvCipher"]:
                f.write(struct.pack('I',i))
        await alert(f"Successfully saved at {e.path+filename}")
        return
    
    async def handleSendFileUpload(e):
        sender["sendFilename"] = e.files[0].name
        sender["sendFilepath"] = e.files[0].path
        sendFileInfo.value = sender["sendFilename"]
        sendFileInfo.update()
        return
    
    async def handleSendKey(e):
        recipient["friendkey"] = sender["pubkey"]
        await alert("Public key successfully sent.")
        return

    async def handleRcvText(e):
        if e.control.text == "Show decrypted message":

            sender["rcvPlain"] = rsa.decrypt(sender["privkey"], sender["rcvCipher"]).decode('utf-8')
            
            rcvTextBox.value = sender["rcvPlain"]
            e.control.text = "Show original message"
        else:
            cipherB64 = ""
            for i in sender["rcvCipher"]:
                cipherB64 = cipherB64 + str(i)
            rcvTextBox.value = base64.b64encode(cipherB64.encode()).decode()
            e.control.text = "Show decrypted message"
        rcvText.update()
        return
    
    async def handleEncryptSave(e):
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
        await alert(f"Successfully encrypted & saved at {e.path+filename}")
        return
    
    async def handleEncryptSend(e):
        nonlocal recipient
        if sendTextBox.visible:
            text_base64 = base64.b64encode((sendTextBox.value).encode('utf-8')).decode('utf-8')
            recipient["rcvCipher"] = rsa.encrypt(recipient["pubkey"],text_base64)
            recipient["rcvType"] = "text"
        else:
            with open(sender["sendFilepath"], "rb") as f:
                recipient["rcvCipher"] = rsa.encrypt(sender["friendkey"], base64.b64encode(f.read()).decode('utf-8'))
            recipient["rcvType"] = "file"
            recipient["rcvFilename"] = sender["sendFilename"]
        await alert("Successfully encrypted & sent.")
        return
    
    async def alert(msg):
        page.snack_bar.content = ft.Text(msg)
        page.snack_bar.open = True
        page.update()
    
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
    keySend = ft.FilledButton("Send Public Key", on_click=handleSendKey, visible=False)
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
    friendKeyUpload = ft.FilledTonalButton("Upload Public Key", on_click=friendKeyUploader.pick_files)
    friendKeySave = ft.FilledTonalButton("Save Public Key", on_click=friendKeyDownloader.get_directory_path, visible=False)
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
    sendButtons = ft.Row(
        [sendSaveButton, sendButton],
        alignment = ft.MainAxisAlignment.CENTER,
        visible = False
    )
    sendBox = ft.Column(
        [
            sendSwitch,
            sendTextBox,
            sendFileBox,
            sendButtons
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
            ),
            theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.GREEN)) # Wangsaff theme
        )
    )
    page.add(content)
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.snack_bar = ft.SnackBar(content=[])

ft.app(target=main)