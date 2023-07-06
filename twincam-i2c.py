#!/usr/bin/python3
from smbus2 import SMBus
import time
arudino = 0x23  # i2cdetect -r -y 8
i2cbus = SMBus(8)
import cv2
import numpy as np

setPos = 0
dataBytes = [0, 0, 0, 0]
getPos = 0
lstPos = 0

run = True


import serial
def momo_serial_read_loop():
    global setPos
    global run
    open_serial = False
    while not open_serial:
        try:
            readSerial = serial.Serial("./serial_out", 9600)
            open_serial = True
            print('success to open /home/tristar/MyWork-NX4_6/serial_out');
        except serial.serialutil.SerialException:
            time.sleep(2)
            print('try to open /home/tristar/MyWork-NX4_6/serial_out');
    while run:
        # data = readSerial.read(3)
        # short_value = np.array((np.array(data[1], dtype='uint16') << 8) + np.array(data[2], dtype='uint16'), dtype='int16')
        # setPos = np.array(short_value, dtype='int32')*2
        # print('read:', setPos)
        # time.sleep(0)
        
        data = readSerial.read(3)
        if data[0] == 0xe0:
            print('header 0xe0 ', end='')
        elif data[1] == 0xe0:
            print('header 0xe0 at index 1')
            readSerial.read(1)
            continue
        elif data[2] == 0xe0:
            print('header 0xe0 at index 2')
            readSerial.read(2)
            continue
        short_value = np.array((np.array(data[1], dtype='uint16') << 8) + np.array(data[2], dtype='uint16'), dtype='int16')
        local_setPos = np.array(short_value, dtype='int32')
        readSerial.write(data[1]);
        readSerial.write(data[2]);
        readSerial.write('\n');
        if local_setPos > 1400:
            local_setPos = 1400
        if local_setPos < -1400:
            local_setPos = -1400
        setPos = local_setPos
        print('read:', setPos)
        time.sleep(0)


# thread = threading.Thread(target=udp_loop)
# thread = threading.Thread(target=stdin_loop)
import threading
thread = threading.Thread(target=momo_serial_read_loop)
thread.start()

while 1:
    try:
        time.sleep(0.05)
        dataBytes[3] = setPos & 0xff
        dataBytes[2] = (setPos >> 8) & 0xff
        dataBytes[1] = (setPos >> 16) & 0xff
        dataBytes[0] = (setPos >> 24) & 0xff
        print('write')
        i2cbus.write_i2c_block_data(arudino, 0, dataBytes) # Write a byte to address "arudino" from offset 0
        rdata = i2cbus.read_i2c_block_data(arudino, 1, 4)  # Returned value is a list of 4 bytes
        getPos = int.from_bytes(rdata, byteorder = 'big', signed = 'true')
        print('getPos', getPos)
        if getPos != lstPos:
            print("actual position" , getPos, "set position", setPos)
            lstPos = getPos

    except KeyboardInterrupt :
        i2cbus.close()
        run = False
        thread.join()
        print("end loop")
        break
    except Exception as e:
        #print("tesfsss")
        pass
