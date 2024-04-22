# Tugas 3 II4031 2024: Algoritma RSA pada Aplikasi Percakapan (chat)

Program Algoritma RSA untuk Simulasi Enkripsi pada Aplikasi Percakapan (chat)

#### Spesifikasi
- Program dapat membangkitan kunci privat dan kunci publik
- Kunci publik dan kunci privat dapat disimpan dalam file terpisah (*.pub dan *.pri)
- Program dapat mengenkripsi file dan teks dengan RSA.
- Program dapat mendekripsi file dan teks dengan RSA.
- Program menampilkan teks plainteks dan cipherteks (base64) di layer percakapan.
- Program dapat menyimpan cipherteks ke dalam file.
- Program dapat mendekripsi file cipherteks menjadi file plainteks.

## Langkah instalasi
- Pasang Python versi 3.10 ke atas
- Pasang modul `Flet` menggunakan perintah `pip install flet`
- Unduh atau lakukan kloning pada repo ini
- Buka folder `src` pada repo ini dan jalankan perintah berikut:
```bash
python3 app.py
```

## Langkah penggunaan program
- Jalankan `python3 app.py` di terminal
- Tekan *switch* untuk mengubah user (Bob atau Alice)
- Generate key pair dengan menekan tombol "Generate Key", atau upload key pair yang sudah ada
- Send public key ke partner dengan menekan tombol Send Public Key
- Jika "Key status" dan "Friend key status" sudah "Ready", maka Anda dapat mengirim pesan
- Ketikkan teks atau unggah berkas yang hendak dienkripsi atau didekripsi
- Tekan tombol "Encrypt and Save" untuk mengenkripsi dan menyimpan pesan, atau "Encrypt and Send" untuk mengenkripsi dan mengirim pesan
- Jika tombol "Encrypt and Send" ditekan, pesan akan muncul jika user di-*switch* ke partner
- Teks yang diterima ditampilkan pada layar sebagai cipherteks dan dapat didekripsi dengan menekan tombol "Show decrypted message" dan disimpan dengan menekan tombol "Save to file"
- File yang diterima (terenkripsi) dapat diunduh dengan menekan tombol "Download encrypted file" dan disimpan hasil dekripsinya dengan menekan tombol "Download file"


## Anggota kelompok
- Aufar Ramadhan 18221163
- Naura Valda Prameswari 18221173
