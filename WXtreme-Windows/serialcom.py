# Import necessary libraries
import serial
import datetime
import array as arr
import time
from tkinter import *
from tkinter.ttk import *
import os
import json
import matplotlib.pyplot as plt
import matplotlib
from sys import exit

# Force Tkinter
matplotlib.use('TkAgg')


crcarray = arr.array('i', [0x0, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
0x1231, 0x210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
0x2462, 0x3443, 0x420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
0x3653, 0x2672, 0x1611, 0x630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
0x48c4, 0x58e5, 0x6886, 0x78a7, 0x840, 0x1861, 0x2802, 0x3823,
0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0xa50, 0x3a33, 0x2a12,
0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0xc60, 0x1c41,
0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0xe70,
0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
0x1080, 0xa1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
0x2b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
0x34e2, 0x24c3, 0x14a0, 0x481, 0x7466, 0x6447, 0x5424, 0x4405,
0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
0x26d3, 0x36f2, 0x691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x8e1, 0x3882, 0x28a3,
0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
0x4a75, 0x5a54, 0x6a37, 0x7a16, 0xaf1, 0x1ad0, 0x2ab3, 0x3a92,
0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0xcc1,
0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0xed1, 0x1ef0])

def calcCRC(data_bytes):

    # Init
    crc = 0

    # Iterate through array and calculate CRC
    for i in data_bytes:
        index = ((crc >> 8) ^ i)
        temp = crcarray[index]
        crc = (0x00FFFF & (crc << 8))
        crc = crc ^ temp

    # Return CRC value
    return(crc)

class SerData:

    # On creating class instance, connect to station and poll station for current data/highs & lows
    def __init__(self):
        workingdir = os.getcwd()

        # Open file
        try:
            with open(f'{workingdir}\\Assets\\comportconf.json', "r") as read_file:
                self.COMPort = json.load(read_file)
        except:
            self.COMPort = "COM3"
            with open(f'{workingdir}\\Assets\\comportconf.json', "w") as write_file:
                json.dump(self.COMPort, write_file)

        # Call openSerial
        self.openSerial()

    def openSerial(self):
        # Attempt to open serial
        try:
            self.ser = serial.Serial(
            port=self.COMPort,
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None,
            )

        # If this fails, open window to ask user for COM Port to communicate over
        except:
            workingdir = os.getcwd()

            # Save COM port settings to file
            def saveandexit():
                with open(f'{workingdir}\\Assets\\comportconf.json', "w") as write_file:
                    json.dump(self.COMPort, write_file)

                # Destroy sub-window
                comwin.destroy()

            def exitprogram():
                exit()

            # Set default option
            self.COMPort = "COM3"

            # Create window
            comwin = Tk()
            comwin.geometry("250x150")
            comwin.iconbitmap(f'{workingdir}\\icon.ico')
            comwin.title("Enter COM port settings")

            comwin.protocol("WM_DELETE_WINDOW", exitprogram)

            # Create list of Com options
            comoptions = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8']

            # Create com select variable as string
            comselect = StringVar(comwin)

            # Create window widgets
            comoption = OptionMenu(comwin, comselect, "COM3", *comoptions)
            comoption.place(relx=.5, rely=.33, anchor="center")

            saveandexit_button = Button(comwin, text="Save", command=saveandexit)
            saveandexit_button.place(relx=.5, rely=.66, anchor="center")


            # Get COM selection
            def change_com_dropdown(*args):
                self.COMPort = comselect.get()

            # If COM selection is changed, call change_com_dropdown
            comselect.trace('w', change_com_dropdown)

            comwin.mainloop()

            # Try to open serial again
            self.openSerial()


    def getData(self):

        try:
            # Initialize self.sensorData
            self.sensorData = {'curintemp': 'NULL', 'curinhum': 'NULL', 'curouttemp': 'NULL', 'curwinspeed': 'NULL',
                          'curwindir': 'NULL', 'curouthum': 'NULL', 'curdailrain': 'NULL', 'curraterain': 'NULL',
                          'hiwinspeed': 'NULL', 'hiintemp': 'NULL', 'lointemp': 'NULL', 'hiinhum': 'NULL',
                          'loinhum': 'NULL', 'hiouttemp': 'NULL', 'loouttemp': 'NULL'}

            # Poll station for current data, save results in hexData
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(str.encode("LPS2 1\n"))
            self.hexData = bytes.hex(self.ser.read(100))

            # Poll station for highs & lows, save results in hexData1
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(str.encode("HILOWS\n"))
            self.hexData1 = bytes.hex(self.ser.read(437))

            # Get current indoor temp
            self.curintemp = self.read2byte(20)
            self.curintemp = self.curintemp[:-1] + '.' + self.curintemp[-1:]
            self.sensorData.update({'curintemp': self.curintemp + '\u00b0F'})

            # Get current indoor humidity
            self.curinhum = self.read1byte(24)
            self.sensorData.update({'curinhum': self.curinhum + '%'})

            # Get current outdoor temp
            self.curouttemp = self.read2byte(26)
            self.curouttemp = self.curouttemp[:-1] + '.' + self.curouttemp[-1:]
            if self.curouttemp != '3276.7':
                self.sensorData.update({'curouttemp': self.curouttemp + '\u00b0F'})

            # Get current wind speed
            self.curwinspeed = self.read1byte(30)
            if self.curwinspeed != '255':
                self.sensorData.update({'curwinspeed': self.curwinspeed + 'MPH'})

            # Get current wind direction
            self.curwindir = self.read2byte(34)
            self.curwindir = int(self.curwindir)

            if self.curwindir >= 11 and self.curwindir < 34:
                self.curwindir = 'NNE'
            elif self.curwindir >= 34 and self.curwindir < 56:
                self.curwindir = 'NE'
            elif self.curwindir >= 56 and self.curwindir < 79:
                self.curwindir = 'ENE'
            elif self.curwindir >= 79 and self.curwindir < 101:
                self.curwindir = 'E'
            elif self.curwindir >= 101 and self.curwindir < 124:
                self.curwindir = 'ESE'
            elif self.curwindir >= 126 and self.curwindir < 146:
                self.curwindir = 'SE'
            elif self.curwindir >= 146 and self.curwindir < 169:
                self.curwindir = 'SSE'
            elif self.curwindir >= 169 and self.curwindir < 191:
                self.curwindir = 'S'
            elif self.curwindir >= 191 and self.curwindir < 214:
                self.curwindir = 'SSW'
            elif self.curwindir >= 214 and self.curwindir < 236:
                self.curwindir = 'SW'
            elif self.curwindir >= 236 and self.curwindir < 259:
                self.curwindir = 'WSW'
            elif self.curwindir >= 259 and self.curwindir < 281:
                self.curwindir = 'W'
            elif self.curwindir >= 281 and self.curwindir < 304:
                self.curwindir = 'WNW'
            elif self.curwindir >= 304 and self.curwindir < 326:
                self.curwindir = 'NW'
            elif self.curwindir >= 326 and self.curwindir < 349:
                self.curwindir = 'NNW'
            elif self.curwindir >= 349 and self.curwindir <= 360:
                self.curwindir = 'N'
            elif self.curwindir >= 1 and self.curwindir < 11:
                self.curwindir = 'N'

            if self.curwindir != 32767:
                self.sensorData.update({'curwindir': self.curwindir})

            # Get outside humidity
            self.curouthum = self.read1byte(68)
            if self.curouthum != '255':
                self.sensorData.update({'curouthum': self.curouthum + '%'})

            # Get daily rain
            self.curdailrain = self.read2byte(102)
            self.curdailrain = str(int(self.curdailrain) / 100)
            self.sensorData.update({'curdailrain': self.curdailrain + ' In.'})

            # Get rain rate
            self.curraterain = self.read2byte(84)
            self.curraterain = str(int(self.curraterain) / 100)
            if self.curraterain != '655.35':
                self.sensorData.update({'curraterain': self.curraterain + ' In./Hr'})

            # Get high daily wind speed
            self.hiwinspeed = self.read1byte1(34)
            self.sensorData.update({'hiwinspeed': self.hiwinspeed + 'MPH'})

            # Get high daily indoor temp
            self.hiintemp = self.read2byte1(44)
            self.hiintemp = self.hiintemp[:-1] + '.' + self.hiintemp[-1:]
            self.sensorData.update({'hiintemp': self.hiintemp + '\u00b0F'})

            # Get low daily indoor temp
            self.lointemp = self.read2byte1(48)
            self.lointemp = self.lointemp[:-1] + '.' + self.lointemp[-1:]
            self.sensorData.update({'lointemp': self.lointemp + '\u00b0F'})

            # Get high daily indoor humidity
            self.hiinhum = self.read1byte1(76)
            self.sensorData.update({'hiinhum': self.hiinhum + '%'})

            # Get low daily indoor humidity
            self.loinhum = self.read1byte1(78)
            self.sensorData.update({'loinhum': self.loinhum + '%'})

            # Get high daily outdoor temperature
            self.hiouttemp = self.read2byte1(100)
            self.hiouttemp = self.hiouttemp[:-1] + '.' + self.hiouttemp[-1:]
            if self.hiouttemp != '3276.8':
                self.sensorData.update({'hiouttemp': self.hiouttemp + '\u00b0F'})

            # Get low daily outdoor temperature
            self.loouttemp = self.read2byte1(96)
            self.loouttemp = self.loouttemp[:-1] + '.' + self.loouttemp[-1:]
            if self.loouttemp != '3276.7':
                self.sensorData.update({'loouttemp': self.loouttemp + '\u00b0F'})

            return self.sensorData

        except:
            pass

    # Converts a 2 byte sized data block into decimal format (for current data)
    def read2byte(self, dataindex):
        curvalhi = self.hexData[dataindex+2:dataindex+4]
        curvallo = self.hexData[dataindex:dataindex+2]
        curval = curvalhi + curvallo
        curval = str(int(curval, 16))
        return curval

    # Converts a 1 byte sized data block into decimal format (for current data)
    def read1byte(self, dataindex):
        curval = self.hexData[dataindex:dataindex+2]
        curval = str(int(curval, 16))
        return curval

    # Converts a 2 byte sized data block into decimal format (for highs & lows)
    def read2byte1(self, dataindex):
        curvalhi = self.hexData1[dataindex+2:dataindex+4]
        curvallo = self.hexData1[dataindex:dataindex+2]
        curval = curvalhi + curvallo
        curval = str(int(curval, 16))
        return curval

    # Converts a 1 byte sized data block into decimal format (for highs & lows)
    def read1byte1(self, dataindex):
        curval = self.hexData1[dataindex:dataindex+2]
        curval = str(int(curval, 16))
        return curval

    def setArchiveInt(self):
        try:
            # Send Archive Interval
            time.sleep(1.5)
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(str.encode("SETPER 60\n"))

        except:
            pass

    def updateTime(self):
        try:
            # Initialize Array
            data_bytes = arr.array("i")

            # Grab individual time pieces
            system_time_year = datetime.datetime.today().year
            system_time_year = (system_time_year - 1900)
            system_time_month = datetime.datetime.today().month
            system_time_day = datetime.datetime.today().day
            system_time_hour = datetime.datetime.today().hour
            system_time_minute = datetime.datetime.today().minute
            system_time_second = datetime.datetime.today().second

            # Insert into array
            data_bytes.insert(0, system_time_second)
            data_bytes.insert(1, system_time_minute)
            data_bytes.insert(2, system_time_hour)
            data_bytes.insert(3, system_time_day)
            data_bytes.insert(4, system_time_month)
            data_bytes.insert(5, system_time_year)

            # Calculate CRC
            crc_bytes = calcCRC(data_bytes)

            # Order CRC into high and low values
            hi = crc_bytes >> 8
            lo = crc_bytes & 0xff

            crcbytearray = bytearray([system_time_second, system_time_minute, system_time_hour, system_time_day, system_time_month, system_time_year, hi, lo])

            # Send time
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(str.encode("SETTIME\n"))
            time.sleep(.5)
            self.ser.write(crcbytearray)

        except:
            pass


class graphArchiveData(SerData):


    def __init__(self, instance, startday, startmonth, startyear, starthour,
            startminute, endday, endmonth, endyear, endhour, endminute):

        try:
            self.startday = startday
            self.startmonth = startmonth
            self.startyear = startyear
            self.starthour = starthour
            self.startminute = startminute

            self.endday = endday
            self.endmonth = endmonth
            self.endyear = endyear
            self.endhour = endhour
            self.endminute = endminute


            ###############################################

            year = int(startyear)
            month = int(startmonth)
            day = int(startday)

            hour = int(starthour)
            minute = int(startminute)

            DateStamp = day + month * 32 + (year) * 512
            TimeStamp = 100 * hour + minute

            DateStamphi = DateStamp >> 8
            DateStamplo = DateStamp & 0xff

            TimeStamphi = TimeStamp >> 8
            TimeStamplo = TimeStamp & 0xff

            data_bytes = arr.array("i")

            # Insert into array
            data_bytes.insert(0, DateStamplo)
            data_bytes.insert(1, DateStamphi)
            data_bytes.insert(2, TimeStamplo)
            data_bytes.insert(3, TimeStamphi)

            # Calculate CRC
            crc_bytes = calcCRC(data_bytes)

            # Order CRC into high and low values
            hi = crc_bytes >> 8
            lo = crc_bytes & 0xff

            # Convert to bytearray
            databytearray = bytearray([DateStamplo, DateStamphi, TimeStamplo, TimeStamphi])
            crcbytearray = bytearray([hi, lo])
            #######################################################

            # Send DMPAFT command
            instance.ser.flushInput()
            instance.ser.flushOutput()
            instance.ser.write(str.encode("DMPAFT\n"))
            discard = str(bytes.hex(instance.ser.read(1)))
            print(discard)

            time.sleep(.1)

            # Write databytearray
            instance.ser.flushInput()
            instance.ser.flushOutput()
            instance.ser.write(databytearray)

            time.sleep(.1)

            # Write CRC
            instance.ser.flushInput()
            instance.ser.flushOutput()
            instance.ser.write(crcbytearray)

            # Ack
            instance.ser.flushInput()
            instance.ser.flushOutput()
            discard = str(bytes.hex(instance.ser.read(1)))
            print(discard)

            time.sleep(.1)

            # Read page information, send ACK
            pageInfo = str(bytes.hex(instance.ser.read(4)))
            instance.ser.flushInput()
            instance.ser.flushOutput()
            ack = 6
            ack = bytearray([ack])

            time.sleep(.25)

            # Read 1st page
            instance.ser.write(ack)
            hexData = str(bytes.hex(instance.ser.read(267)))

            # Calculate how many pages it is sending
            pageCounthi = pageInfo[2:4]
            pageCountlo = pageInfo[0:2]
            pageCount = pageCounthi + pageCountlo
            pageCount = int(pageCount, 16)

            pageStarthi = pageInfo[6:8]
            pageStartlo = pageInfo[4:6]
            pageStart = pageStarthi + pageStartlo
            pageStart = int(pageStart, 16)

            iterationCounter = (pageCount - 1) * 5 + (5 - pageStart)


            ##################################################

            # Read pages
            for i in range(0, pageCount - 1):
                instance.ser.flushInput()
                instance.ser.flushOutput()
                instance.ser.write(ack)
                hexData += bytes.hex(instance.ser.read(267))

            # Chop unnecessary information
            self.dataString = ""
            for i in range(0, pageCount):
                self.dataString = self.dataString + hexData[(i * 534) + 2:((i + 1) * 534) - 12]

            if pageStart == 0:
                pass
            else:
                self.dataString = self.dataString[(pageStart - 1) * 104:]

            self.decodeArchive(iterationCounter)

        except:
            pass

    def preloadArchive(self):
        startmonth = int(self.startmonth)
        startday = int(self.startday)
        startyear = int(self.startyear)
        endmonth = int(self.endmonth)
        endday = int(self.endday)
        endyear = int(self.endyear)

        startmonth1 = startmonth
        startday1 = startday

        # Sanitize dates with preceeding 0s
        if startmonth < 10:
            startmonth1 = '0' + str(startmonth)
        else:
            startmonth1 = startmonth
        if startday < 10:
            startday1 = '0' + str(startday)
        else:
            startday1 = startday

        if endmonth < 10:
            endmonth = '0' + str(endmonth)
        if endday < 10:
            endday = '0' + str(endday)

        # Convert dates to integers to be used in comparison
        startcompare = int(str(startyear) + str(startmonth1) + str(startday1))
        endcompare = int(str(endyear) + str(endmonth) + str(endday))

        date1 = datetime.datetime(day=int(startday), month=int(startmonth), year=2000 + int(startyear))
        date2 = datetime.datetime(day=int(endday), month=int(endmonth), year=2000 + int(endyear))

        self.timedifference = (date2 - date1).days

        # Create hourly X points between start and end ates
        while startcompare <= endcompare:
            i = 0
            while i < 24:
                if i == 0:
                    dtime = str(startmonth) + '/' + str(startday) + '/' + str(startyear) + ' ' + str(12) + ':00 AM'
                elif i == 12:
                    dtime = str(startmonth) + '/' + str(startday) + '/' + str(startyear) + ' ' + str(12) + ':00 PM'
                elif i < 13:
                    dtime = str(startmonth) + '/' + str(startday) + '/' + str(startyear) + ' ' + str(i) + ':00 AM'
                else:
                    dtime = str(startmonth) + '/' + str(startday) + '/' + str(startyear) + ' ' + str(i - 12) + ':00 PM'
                self.archiveDict.update(
                    {dtime: ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']})
                i = i + 1

            # Check current month. Handle month/year rollover
            if int(startmonth) == 2:
                if int(startday) == 28:
                    startmonth = int(startmonth) + 1
                    startmonth1 = int(startmonth1) + 1
                    startday = 1
                    startday1 = 1
                else:
                    startday = int(startday) + 1
                    startday1 = int(startday1) + 1

            elif int(startmonth) == 4 or int(startmonth) == 6 or int(startmonth) == 9 or int(startmonth) == 11:
                if int(startday) == 30:
                    startmonth = int(startmonth) + 1
                    startmonth1 = int(startmonth1) + 1
                    startday = 1
                    startday1 = 1
                else:
                    startday = int(startday) + 1
                    startday1 = int(startday1) + 1

            elif int(startmonth) == 1 or int(startmonth) == 3 or int(startmonth) == 5 or int(startmonth) == 7 or int(
                    startmonth) == 8 or int(startmonth) == 10:
                if int(startday) == 31:
                    startmonth = int(startmonth) + 1
                    startmonth1 = int(startmonth1) + 1
                    startday = 1
                    startday1 = 1
                else:
                    startday = int(startday) + 1
                    startday1 = int(startday1) + 1

            elif int(startmonth) == 12:
                if int(startday) == 31:
                    startyear = int(startyear + 1)
                    startmonth = 1
                    startmonth1 = 1
                    startday = 1
                    startday1 = 1
                else:
                    startday = int(startday) + 1
                    startday1 = int(startday1) + 1

            if int(startmonth) < 10:
                startmonth1 = '0' + str(startmonth)
            if int(startday) < 10:
                startday1 = '0' + str(startday)

            if int(endmonth) < 10:
                endmonth = '0' + str(endmonth)
            if int(endday) < 10:
                endday = '0' + str(endday)

            startcompare = int(str(startyear) + str(startmonth1) + str(startday1))

    def decodeArchive(self, iterationCounter):
        self.archiveDict = {}

        self.preloadArchive()

        # Get archive data for each page
        for i in range(0, iterationCounter):
            j = i * 104
            Date = self.read2bytefordatetime(0 + j)
            Time = self.read2bytefordatetime(4 + j)
            Key = self.ConvertDateTime(Time, Date)
            ArcOutTemp = self.read2bytearc(8 + j)
            ArcOutTemp = ArcOutTemp[:-1] + '.' + ArcOutTemp[-1:]
            ArcOutTempHigh = self.read2bytearc(12 + j)
            ArcOutTempHigh = ArcOutTempHigh[:-1] + '.' + ArcOutTempHigh[-1:]
            ArcOutTempLow = self.read2bytearc(16 + j)
            ArcOutTempLow = ArcOutTempLow[:-1] + '.' + ArcOutTempLow[-1:]
            ArcRainfall = self.read2bytearc(20 + j)
            ArcInTemp = self.read2bytearc(40 + j)
            ArcInTemp = ArcInTemp[:-1] + '.' + ArcInTemp[-1:]
            ArcInHum = self.read1bytearc(44 + j)
            ArcOutHum = self.read1bytearc(46 + j)
            ArcAvWindSpeed = self.read1bytearc(48 + j)
            ArcHighWindSpeed = self.read1bytearc(50 + j)
            ArcWind = self.read1bytearc(52 + j)
            ArcDirHi = self.WindDirection(ArcWind)
            ArcWind = self.read1bytearc(54 + j)
            ArcPrevWind = self.WindDirection(ArcWind)

            # Add all data points to list
            datalist = [ArcOutTemp, ArcOutTempHigh, ArcOutTempLow, ArcRainfall, ArcInTemp, ArcInHum, ArcOutHum,
                        ArcAvWindSpeed, ArcHighWindSpeed, ArcDirHi, ArcPrevWind]

            # Update dictionary values (preloaded with hourly keys) with data points within specified time range
            if int(self.Year) < int(self.startyear):
                pass
            elif int(self.Month) < int(self.startmonth):
                pass
            elif int(self.Day) < int(self.startday):
                pass
            elif int(self.Hour) < int(self.starthour):
                pass
            elif int(self.Minute) < self.startminute:
                pass

            elif int(self.Year) > int(self.endyear):
                pass
            elif int(self.Month) > int(self.endmonth):
                pass
            elif int(self.Day) > int(self.endday):
                pass
            elif int(self.Hour) > int(self.endhour):
                pass
            elif int(self.Minute) > self.endminute:
                pass

            else:
                self.archiveDict.update({Key: datalist})


    def ConvertDateTime(self, Time, Date):
        self.Year = str((int(Date, 16)) >> 9)
        self.Month = str(((int(Date, 16)) >> 5) & 0b1111)
        self.Day = str((int(Date, 16)) & 0b11111)

        Time = int(Time, 16)
        self.Hour = int(int(Time) / 100)
        if self.Hour >= 12:
            if self.Hour > 12:
                NewHour = self.Hour - 12
            else:
                NewHour = self.Hour
            AMPM = 'PM'
        elif self.Hour == 0:
            NewHour = 12
            AMPM = 'AM'
        else:
            NewHour = self.Hour
            AMPM = 'AM'
        self.Minute = (int(Time) - (self.Hour * 100))
        if self.Minute < 10:
            self.Minute = "0" + str(self.Minute)

        returnVal = f'{self.Month}/{self.Day}/{self.Year} {NewHour}:{self.Minute} {AMPM}'

        return (returnVal)

    def read2bytefordatetime(self, dataindex):
        hi = self.dataString[dataindex + 2:dataindex + 4]
        lo = self.dataString[dataindex:dataindex + 2]
        returnval = hi + lo
        return returnval

    def read2bytearc(self, dataindex):
        hi = self.dataString[dataindex + 2:dataindex + 4]
        lo = self.dataString[dataindex:dataindex + 2]
        returnval = hi + lo
        returnval = str(int(returnval, 16))
        return returnval

    def read1bytearc(self, dataindex):
        returnval = self.dataString[dataindex:dataindex + 2]
        returnval = str(int(returnval, 16))
        return returnval

    def WindDirection(self, ArcWind):

        ArcWind = int(ArcWind)

        if ArcWind == 0:
            returnWindDir = 'N'
        elif ArcWind == 1:
            returnWindDir = 'NNE'
        elif ArcWind == 2:
            returnWindDir = 'NE'
        elif ArcWind == 3:
            returnWindDir = 'ENE'
        elif ArcWind == 4:
            returnWindDir = 'E'
        elif ArcWind == 5:
            returnWindDir = 'ESE'
        elif ArcWind == 6:
            returnWindDir = 'SE'
        elif ArcWind == 7:
            returnWindDir = 'SSE'
        elif ArcWind == 8:
            returnWindDir = 'S'
        elif ArcWind == 9:
            returnWindDir = 'SSW'
        elif ArcWind == 10:
            returnWindDir = 'SW'
        elif ArcWind == 11:
            returnWindDir = 'WSW'
        elif ArcWind == 12:
            returnWindDir = 'W'
        elif ArcWind == 13:
            returnWindDir = 'WNW'
        elif ArcWind == 14:
            returnWindDir = 'NW'
        elif ArcWind == 15:
            returnWindDir = 'NNW'
        else:
            returnWindDir = "nan"

        return (returnWindDir)

    def createGraph(self, arcselect):

        try:
            # Create X ticks depending on date range graphed
            def fixXticks(xinput):
                labels = []
                if self.timedifference < 1:
                    for j in xinput:
                        labels.append(j)
                elif self.timedifference == 1:
                    for j in xinput:
                        labels.append(j)
                elif self.timedifference < 7:
                    i = 0
                    for j in xinput:
                        if i == 0:
                            labels.append(j)
                        else:
                            labels.append("")
                        i = i + 1
                        if i == 6:
                            i = 0
                elif self.timedifference < 14:
                    i = 0
                    for j in xinput:
                        if i == 0:
                            labels.append(j)
                        else:
                            labels.append("")
                        i = i + 1
                        if i == 12:
                            i = 0
                elif self.timedifference < 30:
                    i = 0
                    for j in xinput:
                        if i == 0:
                            labels.append(j)
                        else:
                            labels.append("")
                        i = i + 1
                        if i == 48:
                            i = 0
                elif self.timedifference <= 90:
                    i = 0
                    for j in xinput:
                        if i == 0:
                            labels.append(j)
                        else:
                            labels.append("")
                        i = i + 1
                        if i == 96:
                            i = 0
                return labels

            # Create X lists
            xouttemp = []
            xouttemphigh = []
            xouttemplow = []
            xrainfall = []
            xintemp = []
            xinhum = []
            xouthum = []
            xavwindspeed = []
            xhighwindspeed = []
            xwinddirhi = []
            xprevwind = []

            # Create Y lists
            youttemp = []
            youttemphigh = []
            youttemplow = []
            yrainfall = []
            yintemp = []
            yinhum = []
            youthum = []
            yavwindspeed = []
            yhighwindspeed = []
            ywinddirhi = []
            yprevwind = []

            # Get values from archiveDict. Add items to X and Y lists
            for key, value in self.archiveDict.items():
                outtemp, outtemphigh, outtemplow, rainfall, intemp, inhum, outhum, avwindspeed, highwindspeed, winddirhi, prevwind = [
                    value[i] for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)]

                if outtemp != '3276.7':
                    youttemp.append(float(outtemp))
                    xouttemp.append(key)
                else:
                    youttemp.append(float('nan'))
                    xouttemp.append(key)

                if outtemphigh != '3276.8':
                    youttemphigh.append(float(outtemphigh))
                    xouttemphigh.append(key)
                else:
                    youttemphigh.append(float('nan'))
                    xouttemphigh.append(key)

                if outtemplow != '3276.7':
                    youttemplow.append(float(outtemplow))
                    xouttemplow.append(key)
                else:
                    youttemplow.append(float('nan'))
                    xouttemplow.append(key)

                yrainfall.append(float(rainfall))
                xrainfall.append(key)

                if intemp != '3276.7':
                    yintemp.append(float(intemp))
                    xintemp.append(key)
                else:
                    yintemp.append(float('nan'))
                    xintemp.append(key)

                if inhum != '255':
                    yinhum.append(float(inhum))
                    xinhum.append(key)
                else:
                    yinhum.append(float('nan'))
                    xinhum.append(key)

                if outhum != '255':
                    youthum.append(float(outhum))
                    xouthum.append(key)
                else:
                    youthum.append(float('nan'))
                    xouthum.append(key)

                if yavwindspeed != '255':
                    yavwindspeed.append(float(avwindspeed))
                    xavwindspeed.append(key)
                else:
                    yavwindspeed.append(float('nan'))
                    xavwindspeed.append(key)

                yhighwindspeed.append(float(highwindspeed))
                xhighwindspeed.append(key)

                ywinddirhi.append(winddirhi)
                xwinddirhi.append(key)

                yprevwind.append(prevwind)
                xprevwind.append(key)

            # Create archive graph dependent on user selection
            if arcselect == "ArcOutTemp":
                plt.plot(xouttemp, youttemp, label='Outdoor Temperature')

                labels = fixXticks(xouttemp)

                plt.xticks(ticks=xouttemp, labels=labels)

                plt.ylabel('Degrees (\u00b0F)')
                plt.title('Outdoor Temperature')
            elif arcselect == "ArcOutTempHigh":
                plt.plot(xouttemphigh, youttemphigh, label='High Outdoor Temperature')

                labels = fixXticks(xouttemphigh)

                plt.xticks(ticks=xouttemphigh, labels=labels)

                plt.ylabel('Degrees (\u00b0F)')
                plt.title('High Outdoor Temperature')
            elif arcselect == "ArcOutTempLow":
                plt.plot(xouttemplow, youttemplow, label='Low Outdoor Temperature')

                labels = fixXticks(xouttemplow)

                plt.xticks(ticks=xouttemplow, labels=labels)

                plt.ylabel('Degrees (\u00b0F)')
                plt.title('Low Outdoor Temperature')
            elif arcselect == "ArcRainfall":
                plt.plot(xrainfall, yrainfall, label='Rainfall')

                labels = fixXticks(xrainfall)

                plt.xticks(ticks=xrainfall, labels=labels)

                plt.ylabel('Inches')
                plt.title('Rainfall')
            elif arcselect == "ArcInTemp":
                plt.plot(xintemp, yintemp, label='Indoor Temperature')

                labels = fixXticks(xintemp)

                plt.xticks(ticks=xintemp, labels=labels)

                plt.ylabel('Degrees (\u00b0F)')
                plt.title('Indoor Temperature')
            elif arcselect == "ArcInHum":
                plt.plot(xinhum, yinhum, label='Indoor Humidity')

                labels = fixXticks(xinhum)

                plt.xticks(ticks=xinhum, labels=labels)

                plt.ylabel('%')
                plt.title('Indoor Humidity')
            elif arcselect == "ArcOutHum":
                plt.plot(xouthum, youthum, label='Outdoor Humidity')

                labels = fixXticks(xouthum)

                plt.xticks(ticks=xouthum, labels=labels)

                plt.ylabel('%')
                plt.title('Outdoor Humidity')
            elif arcselect == "ArcAvWindSpeed":
                plt.plot(xavwindspeed, yavwindspeed, label='Average Wind Speed')

                labels = fixXticks(xavwindspeed)

                plt.xticks(ticks=xavwindspeed, labels=labels)

                plt.ylabel('MPH')
                plt.title('Average Wind Speed')
            elif arcselect == "ArcHighWindSpeed":
                plt.plot(xhighwindspeed, yhighwindspeed, label='High Wind Speed')

                labels = fixXticks(xhighwindspeed)

                plt.xticks(ticks=xhighwindspeed, labels=labels)

                plt.ylabel('MPH')
                plt.title('High Wind Speed')
            elif arcselect == "ArcDirHi":
                plt.scatter(xwinddirhi, ywinddirhi, label='High Wind Direction')

                labels = fixXticks(xwinddirhi)

                plt.xticks(ticks=xwinddirhi, labels=labels)

                plt.ylabel('Direction')
                plt.title('High Wind Direction')
            elif arcselect == "ArcPrevWind":
                plt.scatter(xprevwind, yprevwind, label='Prevailing Wind Direction')

                labels = fixXticks(xprevwind)

                plt.xticks(ticks=xprevwind, labels=labels)

                plt.ylabel('Direction')
                plt.title('Prevailing Wind Direction')

            # Rotate x labels
            plt.xticks(fontsize=8, rotation=60)
            plt.subplots_adjust(bottom=0.26)

            fig = plt.gcf()
            fig.canvas.manager.set_window_title('WXtreme Archive Graph')

            plt.xlabel('Date and Time')

            # Create grid
            plt.grid(linestyle=":")

        except:
            pass

    # Display graph
    def show_Graph(self):
        try:
            plt.show()
        except:
            pass