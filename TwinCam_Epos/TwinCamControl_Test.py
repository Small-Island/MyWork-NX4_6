#!/usr/bin/python3
import time
import TwinCamEpos

from socket import *
import numpy as np

IP = "0.0.0.0"
Port = 4002
Addr = (IP, Port)
BUFSIZE = 1024
udpServSock = socket(AF_INET, SOCK_DGRAM)
udpServSock.bind(Addr)



if __name__ == '__main__':
    TwinCamEpos.initTwinCam()

    # while 1:
    #     data, addr = udpServSock.recvfrom(BUFSIZE)
    #     print(np.array(data[0], dtype='int8')/127.0*180.0, addr)
    #     TwinCamEpos.setTwinCamPostionAndVelocity(np.array(data[0], dtype='int8')/127.0*180.0, 90.0, 180.0)
    #
    # TwinCamEpos.Disable()

    #TwinCamEpos.initTwinCam()
    TwinCamEpos.Enable()
    TwinCamEpos.setTwinCamPostionAndVelocity(15.0, 90.0, 180.0)
    time.sleep(2)
    TwinCamEpos.Disable()
    TwinCamEpos.closeAllDevices()
