import serial
import subprocess

class CurData:
    def __init__(self):
        sub = "ttyUSB"

        usbout = subprocess.Popen("dmesg | grep 'cp210x converter now attached'", stdout=subprocess.PIPE, shell=True)
        temp = str(usbout.stdout.read())
        index = temp.rindex(sub)
        sliced = temp[index:index + 7]

        ser = serial.Serial(
            port=(f'/dev/{sliced}'),
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None,
        )

        ser.write(str.encode("LPS2 1\n"))
        self.hexData = bytes.hex(ser.read(100))

        ser.write(str.encode("HILOWS\n"))
        self.hexData1 = bytes.hex(ser.read(437))

    def read2byte(self, dataindex):
        curvalhi = self.hexData[dataindex+2:dataindex+4]
        curvallo = self.hexData[dataindex:dataindex+2]
        curval = curvalhi + curvallo
        curval = str(int(curval, 16))
        return curval

    def read1byte(self, dataindex):
        curval = self.hexData[dataindex:dataindex+2]
        curval = str(int(curval, 16))
        return curval

    def read2byte1(self, dataindex):
        curvalhi = self.hexData1[dataindex+2:dataindex+4]
        curvallo = self.hexData1[dataindex:dataindex+2]
        curval = curvalhi + curvallo
        curval = str(int(curval, 16))
        return curval

    def read1byte1(self, dataindex):
        curval = self.hexData1[dataindex:dataindex+2]
        curval = str(int(curval, 16))
        return curval

    # Get current indoor temp
    def getcurintemp(self):
        self.curintemp = self.read2byte(20)
        self.curintemp = self.curintemp[:-1] + '.' + self.curintemp[-1:]
        return self.curintemp

    # Get current indoor humidity
    def getcurinhum(self):
        self.curinhum = self.read1byte(24)
        return self.curinhum

    # Get current outdoor temp
    def getouttemp(self):
        self.curouttemp = self.read2byte(26)
        self.curouttemp = self.curouttemp[:-1] + '.' + self.curouttemp[-1:]
        return self.curouttemp

    # Get current wind speed
    def getcurwinspeed(self):
        self.curwinspeed = self.read1byte(30)
        return self.curwinspeed

    # Get current wind direction
    def getcurwindir(self):
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
        elif self.curwindir >=126 and self.curwindir < 146:
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
        elif self.curwindir >=1 and self.curwindir < 11:
            self.curwindir = 'N'
        return self.curwindir

    # Get outside humidity
    def getcurouthum(self):
        self.curouthum = self.read1byte(68)
        return self.curouthum

    # Get daily rain
    def getcurdailrain(self):
        self.curdailrain = self.read2byte(102)
        self.curdailrain = str(int(self.curdailrain / 100))
        return self.curdailrain

    # Get rain rate
    def getcurraterain(self):
        self.curraterain = self.read2byte(84)
        self.curraterain = str(int(self.curraterain / 100))
        return self.curraterain

    # Get high daily wind speed
    def gethiwinspeed(self):
        self.hiwinspeed = self.read1byte1(34)
        return self.hiwinspeed

    # Get high daily indoor temp
    def gethiintemp(self):
        self.hiintemp = self.read2byte1(44)
        self.hiintemp = self.hiintemp[:-1] + '.' + self.hiintemp[-1:]
        return self.hiintemp

    # Get low daily indoor temp
    def getlointemp(self):
        self.lointemp = self.read2byte1(48)
        self.lointemp = self.lointemp[:-1] + '.' + self.lointemp[-1:]
        return self.lointemp

    # Get high daily indoor humidity
    def gethiinhum(self):
        self.hiinhum = self.read1byte1(76)
        return self.hiinhum

    # Get low daily indoor humidity
    def getloinhum(self):
        self.loinhum = self.read1byte1(78)
        return self.loinhum

    # Get high daily outdoor temperature
    def gethiouttemp(self):
        self.hiouttemp = self.read2byte1(100)
        self.hiouttemp = self.hiouttemp[:-1] + '.' + self.hiouttemp[-1:]
        return self.hiouttemp

    # Get low daily outdoor temperature
    def getloouttemp(self):
        self.loouttemp = self.read2byte1(96)
        self.loouttemp = self.loouttemp[:-1] + '.' + self.loouttemp[-1:]
        return self.loouttemp


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



