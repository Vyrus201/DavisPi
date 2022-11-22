import serial

ser = serial.Serial(
    port='COM3',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None,
)

hexData = 0
ser.write(str.encode("LPS 2 1\n"))

#print(ser.read(99))
hexData = bytes.hex(ser.read(99))
print(hexData)

curtemphibyte = hexData[22:24]
curtemplobyte = hexData[20:22]

#print(curtemphibyte)
#print(curtemplobyte)

curtemp = curtemphibyte + curtemplobyte
curtempconv = str(int(curtemp, 16))

curtempconv = curtempconv[:-1] + '.' + curtempconv[-1:]
print(f'The current indoor temperature is: {curtempconv}\u00b0F')