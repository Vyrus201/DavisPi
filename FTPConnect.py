from ftplib import FTP
import json
from cryptography.fernet import Fernet
import ast
import os
import datetime
import time

class SendFTP:
    def __init__(self):
        workingdir = os.getcwd()

        # Open password file and read file contents into dictionary (Currently encrypted, and not separated into individual values)
        with open(f'{workingdir}\\Assets\\FTPCred.json', "r") as read_file:
            self.currentlist = json.load(read_file)

        # Open key file and read contents into variable
        with open(f'{workingdir}\\Assets\\key.json', "r") as read_file:
            self.key = json.load(read_file)

        # Generate decryption key
        self.fernet = Fernet(self.key)

        # Decrypt password file contents. Now formatted as a single string
        self.currentlist = self.fernet.decrypt(self.currentlist).decode()

        # Convert string into dictionary key/value pairs
        self.currentlist = ast.literal_eval(self.currentlist)

        self.ftp_server = self.currentlist[0]
        self.username = self.currentlist[1]
        self.password = self.currentlist[2]
        self.port = self.currentlist[3]

        while True:
            initialtime = datetime.datetime.now()
            # Create FTP instance
            ftp = FTP()

            # Connect to and log in to FTP server according to saved information
            ftp.connect(self.ftp_server, int(self.port))
            ftp.login(self.username, self.password)

            # Sample FTP command. Lists folder contents
            print(ftp.nlst())

            # Attempts to gracefully terminate FTP connection. If error, connection is forcefully closed and an event is written to the event log
            try:
                ftp.quit()
            except:
                fileout = open(f'{self.workingdir}\\ErrorLog.txt', "a")
                fileout.write(
                    f'{datetime.datetime.now()}: Unable to gracefully close connection to FTP server "{self.ftp_server}". FTP connection will now close forcefully.\n')
                fileout.close()
                ftp.close()

            time.sleep(5)


