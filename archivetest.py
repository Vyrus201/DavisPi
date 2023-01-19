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
print(pageCount, pageStart)
print(iterationCounter)



for i in range(0, pageCount-1):
    ser.flushInput()
    ser.flushOutput()
    ser.write(ack)
    hexData += bytes.hex(ser.read(267))
    print("I'm doing something")

dataString = ""
for i in range(0, pageCount):
    dataString = dataString + hexData[(i*534)+2:((i+1)*534)-12]

if pageStart == 1:
    pass
else:
    dataString = dataString[(pageStart-1)*104:]

print(hexData)
print(dataString)


#datastring = "2c2e6400cf02d202cf020000000000000000bf02d202262f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2e8200c502d002c5020000000000000000be02d10226300000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2ec800cc02cc02c4020000000000000000bf02d60226300000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2ee600d502d502cc020000000000000000be02d802262f0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2e2c01d602d602d4020000000000000000bf02d802262f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2e4a01d902d902d6020000000000000000be02d902262e0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2e9001d802da02d8020000000000000000bf02da02262f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2eae01d802d802d6020000000000000000be02d902262f0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2ef401d002d802d0020000000000000000bf02d602262f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2e1202cf02d002cc020000000000000000be02d60227300000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2e5802d502d602ce020000000000000000bf02d902272f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2e7602d802d802d5020000000000000000be02da02262f0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2ebc02d902da02d8020000000000000000bf02db02262f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2ea406b202b202ae0200000000000000005f02d60226310000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2ec206b502b502b2020000000000000000b702d10226310000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2e0807b602b602b5020000000000000000be02cc0226310000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2e2607b702b702b6020000000000000000bf02c90226300000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2e6c07b602b702b6020000000000000000be02c80226300000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2e8a07b402b602b4020000000000000000bf02c80226300000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2ed007b402b502b3020000000000000000be02c90225300000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2eee07b402b502b3020000000000000000bf02c80225300000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2e3408b402b502b3020000000000000000be02c70225300000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2e5208b402b402b3020000000000000000be02cb0226310000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2c2e9808b502b502b4020000000000000000ba02d20226310000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2eb608b602b702b5020000000000000000bb02d9022631000a00000000000000c1ffffffffffffffff00ffffffffffffffffff2c2efc08b802b802b6020000000000000000bc02da0225310000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2c2e1a09b902b902b7020000000000000000bf02d20225300000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e0000c202c202b8020000000000000000be02d30226300000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e1e00d002d102c2020000000000000000bd02d602262e0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e6400d702d702d1020000000000000000bf02d802252e0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e8200d002d802cf020000000000000000be02d202262e0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2ec800d402d402cf020000000000000000bf02d602252d0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2ee600d802d802d4020000000000000000be02d802252d0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e2c01db02db02d7020000000000000000be02d902252d0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e4a01d902dc02d8020000000000000000bf02d802252d0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e9001da02da02d7020000000000000000be02d902252d0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2eae01da02dc02da020000000000000000bf02d802252d0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2ef401db02dc02da020000000000000000be02d902252d0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e1202d602dd02d5020000000000000000bf02d602252d0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e5802cf02d602ce020000000000000000be02d402252e0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e7602d002d002cd020000000000000000bf02d402262e0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2ebc02d802d802d0020000000000000000be02d902252d0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2eda02dc02dc02d8020000000000000000bf02db02252d0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e2003de02df02dc020000000000000000be02db02252d0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e3e03db02df02db020000000000000000bf02db02262e0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e8403db02dd02da020000000000000000be02d802262d0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2ea203dc02dc02da020000000000000000be02db02252d0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2ee803df02df02db020000000000000000bf02db02252c0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e0604df02e002de020000000000000000be02db02252c0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e4c04da02df02da020000000000000000bf02d702252d0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e6a04d102db02d1020000000000000000c002d602252d0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2eb004c702d102c7020000000000000000bb02da02252e0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2ece04c202c702c2020000000000000000b102dc02252f0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e1405c002c202bf020000000000000000bb02dd02242f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e3205be02c002bd020000000000000000be02d502242e0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e7805bd02be02bd020000000000000000bf02d202242e0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e9605bc02bd02bc020000000000000000be02cf02242e0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2edc05bb02bd02bb020000000000000000be02cd02242e0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2efa05ba02bc02ba020000000000000000bc02d702252f0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e4006b902ba02b9020000000000000000bb02d402252f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e5e06b902ba02b9020000000000000000bc02d702252f0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2ea406ba02ba02b9020000000000000000bd02d902242f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2ec206b902ba02b9020000000000000000bc02da02252f0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e0807ba02ba02b9020000000000000000bf02e002242f0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e2607bb02bb02b9020000000000000000be02d602252f0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2e6c07bb02bc02ba020000000000000000be02d202242e0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff2d2e8a07ba02bc02b9020000000000000000bf02d002232e0000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff2d2ed007b902ba02b8020000000000000000bf02ce02232e0000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff322e4006a602a60291020000000000000000a801cb021e25000804040002000000c1ffffffffffffffff00ffffffffffffffffff322e5e06b802b802a6020000000000000000b402d3021d240000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff322ea406c302c302b80200000000000000009f02df021c240000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff322e0807cd02cd02c90200000000000000009e01eb021c240000ffff0002000000c1ffffffffffffffff00ffffffffffffffffff322e2607d202d202cd020000000000000000b102ee021b230000ffff0000000000c1ffffffffffffffff00ffffffffffffffffff322e6c07d502d502d1020000000000000000a202eb021b230000ffff0002000000c1ffffffffffffffff00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
#iterationCounter = 78

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


def oldarchive():
    dinosaur = {}

    for i in range(0, iterationCounter):
        j = i * 104
        DinoDate = read2bytefordatetime(0+j)
        DinoTime = read2bytefordatetime(4+j)
        DinoKey = ConvertDateTime(DinoTime, DinoDate)
        DinoOutTemp = read2byte(8+j)
        DinoOutTemp = DinoOutTemp[:-1] + '.' + DinoOutTemp[-1:]


        dinolist = [DinoOutTemp]
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

