import serial
import subprocess

def read2byte(dataindex):
    curvalhi = hexData[index+2:index+4]
    curvallo = hexData[index:index+2]
    curval = curvalhi + curvallo
    curval = str(int(curval, 16))
    return curval

def read1byte(dataindex):
    curval = hexData[index:index+2]
    curval = str(int(curval, 16))
    return curval

sub = "ttyUSB"

usbout = subprocess.Popen("dmesg | grep 'cp210x converter now attached'", stdout=subprocess.PIPE, shell=True)
temp = str(usbout.stdout.read())
index = temp.rindex(sub)
sliced = temp[index:index+7]


ser = serial.Serial(
    port=(f'/dev/{sliced}'),
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None,
)

ser.write(str.encode("LPS2 1\n"))

hexData = bytes.hex(ser.read(100))

# Get current indoor temp
curintemp = read2byte(20)
curintemp = curintemp[:-1] + '.' + curintemp[-1:]

# Get current indoor humidity
curinhum = read1byte(24)

# Get current outdoor temp
curouttemp = read2byte(26)
curouttemp = curouttemp[:-1] + '.' + curintemp[-1:]

# Get current wind speed
curwinspeed = read1byte(30)

# Get current wind direction
curwindir = read2byte(34)
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

# Get outside humidity
curouthum = read1byte(68)

# Get daily rain
curdailrain = read2byte(102)
curdailrain = str(int(curdailrain / 100))

# Get rain rate
curraterain = read2byte(84)
curraterain = str(int(curraterain / 100))

print(f'The current indoor temperature is: {curintemp}\u00b0F')
print(f'The current indoor humidity is: {curinhum}%')
print(f'The current outdoor temperature is: {curouttemp}\u00b0F')
print(f'The current wind speed is: {curwinspeed} MPH')
print(f'The current wind direction is {curwindir}')
print(f'The current outdoor humidity is: {curouthum}%')
print(f'The daily rain is: {curdailrain} inches')
print(f'The rain rate is: {curdailrain} inches per hour')



ser.write(str.encode("HILOWS\n"))

hexData = bytes.hex(ser.read(437))

# Get high daily wind speed
hiwinspeed = read1byte(34)

# Get high daily indoor temp
hiintemp = read2byte(44)
hiintemp = hiintemp[:-1] + '.' + hiintemp[-1:]

# Get low daily indoor temp
lointemp = read2byte(48)
lointemp = lointemp[:-1] + '.' + lointemp[-1:]

# Get high daily indoor humidity
hiinhum = read1byte(76)

# Get low daily indoor humidity
loinhum = read1byte(78)

# Get high daily outdoor temperature
hiouttemp = read2byte(100)
hiouttemp = hiouttemp[:-1] + '.' + hiouttemp[-1:]

# Get low daily outdoor temperature
loouttemp = read2byte(96)
loouttemp = loouttemp[:-1] + '.' + loouttemp[-1:]


print(f'The highest wind speed today is: {hiwinspeed} MPH')
print(f'The highest indoor temperature today is: {hiintemp}\u00b0F')
print(f'The lowest indoor temperature today is: {lointemp}\u00b0F')
print(f'The highest indoor humidity today is {hiinhum}%')
print(f'The lowest indoor humidity today is {loinhum}%')
print(f'The highest outdoor temperature today is: {hiouttemp}\u00b0F')
print(f'The lowest outdoor temperature today is: {loouttemp}\u00b0F')



