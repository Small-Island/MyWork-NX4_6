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
        short_value = np.array((np.array(data[1], dtype='uint16') << 8) + np.array(data[2], dtype='uint16'), dtype='int16')
        setPos = np.array(short_value, dtype='int32')*5
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
        i2cbus.close()
        run = False
        thread.join()
        print("end loop")
        break
    except Exception as e:
        #print("tesfsss")
        pass
