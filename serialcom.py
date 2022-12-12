# Import necessary libraries
import serial
import subprocess


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
        ser = serial.Serial(
            port=(f'/dev/{sliced}'),
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None,
        )

        # Poll station for current data, save results in hexData
        ser.write(str.encode("LPS2 1\n"))
        self.hexData = bytes.hex(ser.read(100))

        # Poll station for highs & lows, save results in hexData1
        ser.write(str.encode("HILOWS\n"))
        self.hexData1 = bytes.hex(ser.read(437))

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



