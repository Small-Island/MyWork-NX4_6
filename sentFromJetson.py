#!/usr/bin/python3
from smbus2 import SMBus
import numpy
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
print("start")

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')
# create trackbars for value change
cv2.createTrackbar('Value','image', -1400, 1400, nothing)
cv2.setTrackbarMin('Value', 'image', -1400)
lv = 0
while run :
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    v = cv2.getTrackbarPos('Value','image')
    if lv != v:
        print(v)
        lv = v
        setPos = v
    try:
        dataBytes[3] = setPos & 0xff
        dataBytes[2] = (setPos >> 8) & 0xff
        dataBytes[1] = (setPos >> 16) & 0xff
        dataBytes[0] = (setPos >> 24) & 0xff
        i2cbus.write_i2c_block_data(arudino, 0, dataBytes) # Write a byte to address "arudino" from offset 0
        rdata = i2cbus.read_i2c_block_data(arudino,1,4)  # Returned value is a list of 4 bytes
        getPos = int.from_bytes(rdata, byteorder = 'big', signed = 'true')
        if getPos != lstPos:
            print("actual position" ,getPos)
            lstPos = getPos

    except KeyboardInterrupt :
        i2cbus.close()
        print("end loop")
        run = False
    except Exception as e:
        #print("tesfsss")
        pass

cv2.destroyAllWindows()
