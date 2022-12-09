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
        curintemp = self.read2byte(20)
        curintemp = curintemp[:-1] + '.' + curintemp[-1:]
        return curintemp

    # Get current indoor humidity
    def getcurinhum(self):
        curinhum = self.read1byte(24)
        return curinhum

    # Get current outdoor temp
    def getouttemp(self):
        curouttemp = self.read2byte(26)
        curouttemp = curouttemp[:-1] + '.' + curouttemp[-1:]
        return curouttemp

    # Get current wind speed
    def getcurwinspeed(self):
        curwinspeed = self.read1byte(30)
        return curwinspeed

    # Get current wind direction
    def getcurwindir(self):
        curwindir = self.read2byte(34)
        if curwindir >= 11 and curwindir < 34:
            curwindir = 'NNE'
        elif curwindir >= 34 and curwindir < 56:
            curwindir = 'NE'
        elif curwindir >= 56 and curwindir < 79:
            curwindir = 'ENE'
        elif curwindir >= 79 and curwindir < 101:
            curwindir = 'E'
        elif curwindir >= 101 and curwindir < 124:
            curwindir = 'ESE'
        elif curwindir >=126 and curwindir < 146:
            curwindir = 'SE'
        elif curwindir >= 146 and curwindir < 169:
            curwindir = 'SSE'
        elif curwindir >= 169 and curwindir < 191:
            curwindir = 'S'
        elif curwindir >= 191 and curwindir < 214:
            curwindir = 'SSW'
        elif curwindir >= 214 and curwindir < 236:
            curwindir = 'SW'
        elif curwindir >= 236 and curwindir < 259:
            curwindir = 'WSW'
        elif curwindir >= 259 and curwindir < 281:
            curwindir = 'W'
        elif curwindir >= 281 and curwindir < 304:
            curwindir = 'WNW'
        elif curwindir >= 304 and curwindir < 326:
            curwindir = 'NW'
        elif curwindir >= 326 and curwindir < 349:
            curwindir = 'NNW'
        elif curwindir >= 349 and curwindir <= 360:
            curwindir = 'N'
        elif curwindir >=1 and curwindir < 11:
            curwindir = 'N'
        return curwindir

    # Get outside humidity
    def getcurouthum(self):
        curouthum = self.read1byte(68)
        return curouthum

    # Get daily rain
    def getcurdailrain(self):
        curdailrain = self.read2byte(102)
        curdailrain = str(int(curdailrain / 100))
        return curdailrain

    # Get rain rate
    def getcurraterain(self):
        curraterain = self.read2byte(84)
        curraterain = str(int(curraterain / 100))
        return curraterain

    # Get high daily wind speed
    def gethiwinspeed(self):
        hiwinspeed = self.read1byte1(34)
        return hiwinspeed

    # Get high daily indoor temp
    def gethiintemp(self):
        hiintemp = self.read2byte1(44)
        hiintemp = hiintemp[:-1] + '.' + hiintemp[-1:]
        return hiintemp

    # Get low daily indoor temp
    def getlointemp(self):
        lointemp = self.read2byte1(48)
        lointemp = lointemp[:-1] + '.' + lointemp[-1:]
        return lointemp

    # Get high daily indoor humidity
    def gethiinhum(self):
        hiinhum = self.read1byte1(76)
        return hiinhum

    # Get low daily indoor humidity
    def getloinhum(self):
        loinhum = self.read1byte1(78)
        return loinhum

    # Get high daily outdoor temperature
    def gethiouttemp(self):
        hiouttemp = self.read2byte1(100)
        hiouttemp = hiouttemp[:-1] + '.' + hiouttemp[-1:]
        return hiouttemp

    # Get low daily outdoor temperature
    def getloouttemp(self):
        loouttemp = self.read2byte1(96)
        loouttemp = loouttemp[:-1] + '.' + loouttemp[-1:]
        return loouttemp


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



