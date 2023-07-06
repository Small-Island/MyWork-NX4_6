#!/usr/bin/python3
from smbus2 import SMBus
import time
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
        local_setPos = np.array(short_value, dtype='int32')*2
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
        time.sleep(10);

    except KeyboardInterrupt :
        run = False
        thread.join()
        print("end loop")
        break
    except Exception as e:
        #print("tesfsss")
        pass
