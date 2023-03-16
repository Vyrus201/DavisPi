from ftplib import *
import json
from cryptography.fernet import Fernet
import ast
import os
import datetime
import time
from sys import exit


class SendFTP:
    def __init__(self, ThreadStatus, FileStatus):
        workingdir = os.getcwd()

        # Open password file and read file contents into dictionary (Currently encrypted, and not separated into individual values)
        try:
            with open(f'{workingdir}\\Assets\\FTPCred.json', "r") as read_file:
                self.currentlist = json.load(read_file)
        except:
            exit()

        # Open key file and read contents into variable
        try:
            with open(f'{workingdir}\\Assets\\key.json', "r") as read_file:
                self.key = json.load(read_file)
        except:
            exit()

        # Read file
        try:
            with open(f'{workingdir}\\Assets\\ftpsensorconf.json', "r") as read_file:
                self.ftpsensorconfig = json.load(read_file)
        except:
            self.ftpsensorconfig = {}
            with open(f'{workingdir}\\Assets\\ftpsensorconf.json', "w") as write_file:
                json.dump(self.ftpsensorconfig, write_file)

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
        self.frequency = self.currentlist[4]
        self.filename = self.currentlist[5]

        # Make sure that FTP configuration file contents were valid
        try:
            # Create FTP instance
            ftp = FTP()

            ftp.connect(self.ftp_server, int(self.port))
            ftp.login(self.username, self.password)
            ftp.close()
        except:
            fileout = open(f'{workingdir}\\ErrorLog.txt', "a")
            fileout.write(f'{datetime.datetime.now()}: Unable to establish FTP connection. Re-enter FTP configuration\n')
            fileout.close()
            exit()

        counter = 0

        while True:
            now = time.localtime().tm_sec
            while now > 0:
                now = time.localtime().tm_sec
                if ThreadStatus.is_set():
                    exit()

            counter = counter + 1
            if counter == self.frequency:
                counter = 0

                while FileStatus.is_set():
                    print('this is set')

                # Read file
                try:
                    with open(f'{workingdir}\\Assets\\FTPData.json', "r") as read_file:
                        self.FTPData = json.load(read_file)
                except:
                    self.FTPData = {}
                    with open(f'{workingdir}\\Assets\\FTPData.json', "w") as write_file:
                        json.dump(self.FTPData, write_file)

                keys = []
                values = []

                for key, value in self.FTPData.items():
                    if key in self.ftpsensorconfig:
                        keys.append(key)
                        values.append(value)

                try:
                    with open(f'{workingdir}\\Assets\\{self.filename}.csv', 'w') as csvfile:
                        for i in keys:
                            csvfile.write(f'{i},')
                        csvfile.write("\n")
                        for i in values:
                            csvfile.write(f'{i},')

                    ftp = FTP()

                    # Connect to and log in to FTP server according to saved information
                    ftp.connect(self.ftp_server, int(self.port))
                    ftp.login(self.username, self.password)

                    with open(f'{workingdir}\\Assets\\{self.filename}.csv', "rb") as file:
                        ftp.storbinary(f'STOR {self.filename}.csv', file)
                    print('store')

                    # Attempts to gracefully terminate FTP connection. If error, connection is forcefully closed and an event is written to the event log
                    try:
                        ftp.quit()
                    except:
                        fileout = open(f'{self.workingdir}\\ErrorLog.txt', "a")
                        fileout.write(
                            f'{datetime.datetime.now()}: Unable to gracefully close connection to FTP server "{self.ftp_server}". FTP connection will now close forcefully.\n')
                        fileout.close()
                        ftp.close()

                except PermissionError:
                    print('permission error')
                    pass
                except:
                    pass

            # Prevent program from looping several times when seconds = 0
            time.sleep(1)
