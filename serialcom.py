# Import necessary libraries
import serial
import subprocess
import datetime
import array as arr

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
    crc = 0
    for i in data_bytes:
        index = ((crc >> 8) ^ i)
        temp = crcarray[index]
        crc = (0x00FFFF & (crc << 8))
        crc = crc ^ temp
        print(f'New CRC: {hex(crc)}')
    return(crc)

class SerData:

    # On creating class instance, connect to station and poll station for current data/highs & lows
    def __init__(self):

        # Determine which USB port the station is connected to
        sub = "ttyUSB"
        usbout = subprocess.Popen("dmesg | grep 'cp210x converter now attached'", stdout=subprocess.PIPE, shell=True)
        temp = str(usbout.stdout.read())
        index = temp.rindex(sub)
        sliced = temp[index:index + 7]

        # Connect to serial interface over the specified USB port
        self.ser = serial.Serial(
            port=(f'/dev/{self.sliced}'),
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None,
        )

        # Poll station for current data, save results in hexData
        self.ser.write(str.encode("LPS2 1\n"))
        self.hexData = bytes.hex(self.ser.read(100))

        # Poll station for highs & lows, save results in hexData1
        self.ser.write(str.encode("HILOWS\n"))
        self.hexData1 = bytes.hex(self.ser.read(437))

        # Get current indoor temp
        self.curintemp = self.read2byte(20)
        self.curintemp = self.curintemp[:-1] + '.' + self.curintemp[-1:]

        # Get current indoor humidity
        self.curinhum = self.read1byte(24)

        # Get current outdoor temp
        self.curouttemp = self.read2byte(26)
        self.curouttemp = self.curouttemp[:-1] + '.' + self.curouttemp[-1:]

        # Get current wind speed
        self.curwinspeed = self.read1byte(30)

        # Get current wind direction
        self.curwindir = self.read2byte(34)
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

        # Get outside humidity
        self.curouthum = self.read1byte(68)

        # Get daily rain
        self.curdailrain = self.read2byte(102)
        self.curdailrain = str(int(self.curdailrain / 100))

        # Get rain rate
        self.curraterain = self.read2byte(84)
        self.curraterain = str(int(self.curraterain / 100))

        # Get high daily wind speed
        self.hiwinspeed = self.read1byte1(34)

        # Get high daily indoor temp
        self.hiintemp = self.read2byte1(44)
        self.hiintemp = self.hiintemp[:-1] + '.' + self.hiintemp[-1:]

        # Get low daily indoor temp
        self.lointemp = self.read2byte1(48)
        self.lointemp = self.lointemp[:-1] + '.' + self.lointemp[-1:]

        # Get high daily indoor humidity
        self.hiinhum = self.read1byte1(76)

        # Get low daily indoor humidity
        self.loinhum = self.read1byte1(78)

        # Get high daily outdoor temperature
        self.hiouttemp = self.read2byte1(100)
        self.hiouttemp = self.hiouttemp[:-1] + '.' + self.hiouttemp[-1:]

        # Get low daily outdoor temperature
        self.loouttemp = self.read2byte1(96)
        self.loouttemp = self.loouttemp[:-1] + '.' + self.loouttemp[-1:]

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

    # Return current indoor temp
    def getcurintemp(self):
        return self.curintemp

    # Return current indoor humidity
    def getcurinhum(self):
        return self.curinhum

    # Return current outdoor temp
    def getouttemp(self):
        return self.curouttemp

    # Return current wind speed
    def getcurwinspeed(self):
        return self.curwinspeed

    # Return current wind direction
    def getcurwindir(self):
        return self.curwindir

    # Return outside humidity
    def getcurouthum(self):
        return self.curouthum

    # Return daily rain
    def getcurdailrain(self):
        return self.curdailrain

    # Return rain rate
    def getcurraterain(self):
        return self.curraterain

    # Return high daily wind speed
    def gethiwinspeed(self):
        return self.hiwinspeed

    # Return high daily indoor temp
    def gethiintemp(self):
        return self.hiintemp

    # Return low daily indoor temp
    def getlointemp(self):
        return self.lointemp

    # Return high daily indoor humidity
    def gethiinhum(self):
        return self.hiinhum

    # Return low daily indoor humidity
    def getloinhum(self):
        return self.loinhum

    # Return high daily outdoor temperature
    def gethiouttemp(self):
        return self.hiouttemp

    # Return low daily outdoor temperature
    def getloouttemp(self):
        return self.loouttemp

    # Upon deletion of the class instance, print all data values. In actual deployment this should not exist. This is
    # useful for debugging, however. Shows that all values are being calculated properly
    def __del__(self):
        print(f'The highest wind speed today is: {self.hiwinspeed} MPH')
        print(f'The highest indoor temperature today is: {self.hiintemp}\u00b0F')
        print(f'The lowest indoor temperature today is: {self.lointemp}\u00b0F')
        print(f'The highest indoor humidity today is {self.hiinhum}%')
        print(f'The lowest indoor humidity today is {self.loinhum}%')
        print(f'The highest outdoor temperature today is: {self.hiouttemp}\u00b0F')
        print(f'The lowest outdoor temperature today is: {self.loouttemp}\u00b0F')

        print(f'The current indoor temperature is: {self.curintemp}\u00b0F')
        print(f'The current indoor humidity is: {self.curinhum}%')
        print(f'The current outdoor temperature is: {self.curouttemp}\u00b0F')
        print(f'The current wind speed is: {self.curwinspeed} MPH')
        print(f'The current wind direction is {self.curwindir}')
        print(f'The current outdoor humidity is: {self.curouthum}%')
        print(f'The daily rain is: {self.curdailrain} inches')
        print(f'The rain rate is: {self.curdailrain} inches per hour')


    def updateTime(self):

        # Initialize Array
        data_bytes = arr.array("i")

        system_time_year = datetime.datetime.today().year
        system_time_year = (system_time_year - 1900)
        system_time_month = datetime.datetime.today().month
        system_time_day = datetime.datetime.today().day
        system_time_hour = datetime.datetime.today().hour
        system_time_minute = datetime.datetime.today().minute
        system_time_second = datetime.datetime.today().second

        data_bytes.insert(0, system_time_second)
        data_bytes.insert(1, system_time_minute)
        data_bytes.insert(2, system_time_hour)
        data_bytes.insert(3, system_time_day)
        data_bytes.insert(4, system_time_month)
        data_bytes.insert(5, system_time_year)

        # data_bytes.insert(0, 0xc6)
        # data_bytes.insert(1, 0xce)
        # data_bytes.insert(2, 0xa2)
        # data_bytes.insert(3, 0x03)

        crc_bytes = calcCRC(data_bytes)

        hi = crc_bytes >> 8
        lo = crc_bytes & 0xff

        data_bytes.insert(6, hi)
        data_bytes.insert(7, lo)

        string = ''

        for i in data_bytes:
            string = string + str(i)

        # Send time
        self.ser.write(str.encode("SETTIME\n"))
        self.ser.write(str.encode(string))






