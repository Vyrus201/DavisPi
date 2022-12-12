# Import necessary libraries
from ftplib import FTP
import datetime
from cryptography.fernet import Fernet
import json
import ast

# Changes credentials used in FTP connection and saves to JSON file for later use
def changeFTP():
    # Initialize dictionary
    dict = {}

    # Generate new encryption key
    key = Fernet.generate_key()
    fernet = Fernet(key)

    # Ask for user input for each FTP connection property
    ftp_server = input("Enter ftp server: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    port = input("Enter port (Leave blank for default of 21): ")

    # Append values into the dictionary
    dict.update({"ftp_server": ftp_server})
    dict.update({"username": username})
    dict.update({"password": password})

    # If port value was left blank, enter 21 for default
    if not port:
        dict.update({"port": '21'})
    else:
        dict.update({"port": port})

    # Encrpyt dictionary and save to file
    encdict = str(dict)
    encdict = fernet.encrypt(encdict.encode()).decode()
    with open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\password.json", "w") as write_file:
        json.dump(encdict, write_file)

    # Decode key and save to file
    key = key.decode()
    with open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\key.json", "w") as write_file:
        json.dump(key, write_file)

# Connects to FTP server with previously provided credentials and sends a file
def sendData():

    # Create variables so dictionary can overwrite them later. Not *required*, but the compiler likes it better this way
    ftp_server = 0
    username = 0
    password = 0
    port = 0

    # Open password file and read file contents into dictionary (Currently encrypted, and not separated into individual values)
    with open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\password.json", "r") as read_file:
        currentdict = json.load(read_file)

    # Open key file and read contents into variable
    with open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\key.json", "r") as read_file:
        key = json.load(read_file)

    # Generate decryption key
    fernet = Fernet(key)

    # Decrypt password file contents. Now formatted as a single string
    currentdict = fernet.decrypt(currentdict).decode()

    # Convert string into dictionary key/value pairs
    currentdict = ast.literal_eval(currentdict)

    # Create a variable with the name of the dictionary key, and a value of the dictionary value
    # I.e. if dictionary contains: {"sampleKey": "sampleValue:}, a variable named "sampleKey" will be created
    # with value "sampleValue"
    for key, value in currentdict.items():
        exec(key + '=value')

    # Create FTP instance
    ftp = FTP()

    # Connect to and log in to FTP server according to saved information
    ftp.connect(ftp_server,int(port))
    ftp.login(username,password)

    # Sample FTP command. Lists folder contents
    print(ftp.nlst())

    # Opens file on local computer and sends to FTP server
    with open('test.txt', 'rb') as f:
        ftp.storbinary('STOR ' + 'test.txt', f)

    # Attempts to gracefully terminate FTP connection. If error, connection is forcefully closed and an event is written to the event log
    try:
        ftp.quit()
    except:
        fileout = open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\ErrorLog.txt", "a")
        fileout.write(f'{datetime.datetime.now()}: Unable to gracefully close connection to FTP server "{ftp_server}". FTP connection will now close forcefully.\n')
        fileout.close()
        ftp.close()
        exit()
