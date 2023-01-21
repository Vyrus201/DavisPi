# This is a sample Python script.

import serial
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

ser = serial.Serial(
    # port=(f'/dev/{sliced}'),
    port='COM3',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None,
)

#year = int(input(f'Enter Year'))
#month = int(input(f'Enter Month'))
#day = int(input(f'Enter Date'))

#hour = int(input(f'Enter Hour'))
#minute = int(input(f'Enter Minute'))

year = 2023
month = 1
day = 12

hour = 1
minute = 0

DateStamp = day + month*32 + (year-2000)*512
TimeStamp = 100*hour + minute

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

databytearray = bytearray([DateStamplo, DateStamphi, TimeStamplo, TimeStamphi])
crcbytearray = bytearray([hi, lo])


ser.flushInput()
ser.flushOutput()
ser.write(str.encode("DMPAFT\n"))
discard = str(bytes.hex(ser.read(1)))
print(discard)

ser.flushInput()
ser.flushOutput()
ser.write(databytearray)

ser.flushInput()
ser.flushOutput()
ser.write(crcbytearray)

ser.flushInput()
ser.flushOutput()
discard = str(bytes.hex(ser.read(1)))
print(discard)

pageInfo = str(bytes.hex(ser.read(4)))
ser.flushInput()
ser.flushOutput()
ack = 6
ack = bytearray([ack])
ser.write(ack)
hexData = str(bytes.hex(ser.read(267)))

pageCounthi = pageInfo[2:4]
pageCountlo = pageInfo[0:2]
pageCount = pageCounthi + pageCountlo
pageCount = int(pageCount, 16)

pageStarthi = pageInfo[6:8]
pageStartlo = pageInfo[4:6]
pageStart = pageStarthi + pageStartlo
pageStart = int(pageStart, 16)

iterationCounter = (pageCount-1)*5 + (6-pageStart)

for i in range(0, pageCount-1):
    ser.flushInput()
    ser.flushOutput()
    ser.write(ack)
    hexData += bytes.hex(ser.read(267))

dataString = ""
for i in range(0, pageCount):
    dataString = dataString + hexData[(i*534)+2:((i+1)*534)-12]

#if pageStart == 1:
if pageStart == 0:
    pass
else:
    dataString = dataString[(pageStart-1)*104:]


def read2bytefordatetime(dataindex):
    hi = dataString[dataindex + 2:dataindex + 4]
    lo = dataString[dataindex:dataindex + 2]
    returnval = hi + lo
    return returnval


def read2byte(dataindex):
    hi = dataString[dataindex+2:dataindex+4]
    lo = dataString[dataindex:dataindex+2]
    returnval = hi + lo
    returnval = str(int(returnval, 16))
    return returnval



def read1byte(dataindex):
    returnval = dataString[dataindex:dataindex+2]
    returnval = str(int(returnval, 16))
    return returnval

def WindDirection(DinoWind):

    DinoWind = int(DinoWind)

    if DinoWind == 0:
        returnWindDir = 'N'
    elif DinoWind == 1:
        returnWindDir = 'NNE'
    elif DinoWind == 2:
        returnWindDir = 'NE'
    elif DinoWind == 3:
        returnWindDir = 'ENE'
    elif DinoWind == 4:
        returnWindDir = 'E'
    elif DinoWind == 5:
        returnWindDir = 'ESE'
    elif DinoWind == 6:
        returnWindDir = 'SE'
    elif DinoWind == 7:
        returnWindDir = 'SSE'
    elif DinoWind == 8:
        returnWindDir = 'S'
    elif DinoWind == 9:
        returnWindDir = 'SSW'
    elif DinoWind == 10:
        returnWindDir = 'SW'
    elif DinoWind == 11:
        returnWindDir = 'WSW'
    elif DinoWind == 12:
        returnWindDir = 'W'
    elif DinoWind == 13:
        returnWindDir = 'WNW'
    elif DinoWind == 14:
        returnWindDir = 'NW'
    elif DinoWind == 15:
        returnWindDir = 'NNW'
    else:
        returnWindDir = "Error"

    return(returnWindDir)

def oldarchive():
    dinosaur = {}

    for i in range(0, iterationCounter):
        j = i * 104
        DinoDate = read2bytefordatetime(0+j)
        DinoTime = read2bytefordatetime(4+j)
        DinoKey = ConvertDateTime(DinoTime, DinoDate)
        DinoOutTemp = read2byte(8+j)
        DinoOutTemp = DinoOutTemp[:-1] + '.' + DinoOutTemp[-1:]
        DinoOutTempHigh = read2byte(12+j)
        DinoOutTempHigh = DinoOutTempHigh[:-1] + '.' + DinoOutTempHigh[-1:]
        DinoOutTempLow = read2byte(16 + j)
        DinoOutTempLow = DinoOutTempLow[:-1] + '.' + DinoOutTempLow[-1:]
        DinoRainfall = read2byte(20 + j)
        DinoInTemp = read2byte(40 + j)
        DinoInTemp = DinoInTemp[:-1] + '.' + DinoInTemp[-1:]
        DinoInHum = read1byte(44 + j)
        DinoOutHum = read1byte(46 + j)
        DinoAvWindSpeed = read1byte(48 + j)
        DinoHighWindSpeed = read1byte(50 + j)
        DinoWind = read1byte(52 + j)
        DinoDirHi = WindDirection(DinoWind)
        DinoWind = read1byte(54 + j)
        DinoPrevWind = WindDirection(DinoWind)

        dinolist = [DinoOutTemp, DinoOutTempHigh, DinoOutTempLow, DinoRainfall, DinoInTemp, DinoInHum, DinoOutHum, DinoAvWindSpeed, DinoHighWindSpeed, DinoDirHi, DinoPrevWind]

        dinosaur.update({DinoKey: dinolist})

    print(dinosaur)


def ConvertDateTime(DinoTime, DinoDate):
    Year = str(((int(DinoDate, 16)) >> 9) + 2000)
    Month = str(((int(DinoDate, 16)) >> 5) & 0b1111)
    Day = str((int(DinoDate, 16)) & 0b11111)

    DinoTime = int(DinoTime, 16)
    Hour = int(int(DinoTime) / 100)
    Minute = (int(DinoTime) - (Hour*100))
    if Minute < 10:
        Minute = "0" + str(Minute)

    returnVal = f'{Month}/{Day}/{Year} {Hour}:{Minute}'

    return(returnVal)




oldarchive()

