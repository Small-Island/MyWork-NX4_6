#!/usr/bin/python3
import subprocess
from subprocess import Popen, PIPE
import time
import threading
import os
import requests

camDev = []
devID = []
camStatus = []
p = subprocess.Popen('lsusb', shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
output = p.communicate()[0]
usbDevices = output.decode('utf-8')
#print(usbDevices)
for usbDev in usbDevices.splitlines():
	if 'Ricoh' in usbDev:
		camDev.append(usbDev)
		devID.append(usbDev[15:18])
		camStatus.append(usbDev[28:32])
		print(usbDev[15:18])
		print(usbDev[28:32])

for cid in devID:
	print("----------" + cid + ": status-------")
	cmd = 'ptpcam --dev=' + cid + ' --show-property=0x5013'
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	output = p.communicate()[0]
	status = output.decode('utf-8')
	captureMode=False
	for s in status.splitlines():
		print(s)
		if 'ERROR' in s:
			print('Wake up')
			cmd2 = 'ptpcam --dev=' + cid + ' --set-property=0xD80E --val=0x00'
			pw = subprocess.Popen(cmd2, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
			outp = pw.communicate()[0]
			print(outp.decode('utf-8'))

			print('set live mode')
			cmd3 = 'ptpcam --dev=' + cid + ' --set-property=0x5013 --val=0x8005'
			pl = subprocess.Popen(cmd3, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
			outp = pl.communicate()[0]
			print(outp.decode('utf-8'))

		if 'Capture' in s:
			captureMode=True

	if captureMode==False:
		print('set live mode')
		cmd3 = 'ptpcam --dev=' + cid + ' --set-property=0x5013 --val=0x8005'
		pl = subprocess.Popen(cmd3, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		outp = pl.communicate()[0]
		print(outp.decode('utf-8'))

time.sleep(2)


print("Num of Cam:", len(devID))
