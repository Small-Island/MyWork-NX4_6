from smbus2 import SMBus
import time
arudino = 0x23  # i2cdetect -r -y 8
i2cbus = SMBus(8)
dataBytes = [0, 0, 0, 0]
getPos = 0
lstPos = 0
run = True
print("start")

def nothing(x):
    pass
def writeIC2(setPos):
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
