#!/usr/bin/python3
import subprocess
from subprocess import Popen, PIPE
import time
import threading
import os

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


print("Num of Cam:", len(devID))
cam0 = './THETA_Cameras/camera0/gst_loopback'
runTheta0 = True
def openTHETA0():
	print('Open THETA0')
	p0 = subprocess.Popen(cam0, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	print('theta0:', p0.stdout.readline().decode().strip())
	while runTheta0:
		if p0.poll() is None:
			print('theta0:', p0.stdout.readline().decode().strip())

	p0.terminate()
	p0.wait()
	print("end camera0")

cam1 = './THETA_Cameras/camera1/gst_loopback'
runTheta1 = True
def openTHETA1():
	print('Open THETA1')
	p1 = subprocess.Popen(cam1, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	print('theta1:', p1.stdout.readline().decode().strip())
	while runTheta1:
		if p1.poll() is None:
			print('theta1:', p1.stdout.readline().decode().strip())

	p1.terminate()
	p1.wait()

	print("end camera1")

momoP0 = './momo-2022.1.0_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video0 sora --signaling-url wss://sora.ikeilabsora.0am.jp/signaling --channel-id twincam-left --multistream 1 --role sendonly --video-codec-type H264 --video-bit-rate 15000'
# momoP0 = './momo-2021.6.0_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video0 sora --signaling-url wss://sora.ikeilabsora.0am.jp/signaling --channel-id rabbit-go@twincamleft --role sendonly --video-codec-type H264 --video-bit-rate 15000'
#momoP0 = './momo-2021.2.3_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video0 --insecure sora wss://sora.ikeilabsora.0am.jp/signaling rabbit-go@twincamleft --role sendonly --video-codec-type H264 --video-bit-rate 15000'
#momoP0 = './momo-2021.2.3_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video0 --insecure test'
runmomo0 = True
def momo0():
	pm0 = subprocess.Popen(momoP0, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	#os.set_blocking(pm0.stdout.fileno(), False)
	print('run momo0')
	while runmomo0:
		if pm0.poll() is None:
			text = pm0.stdout.readline().decode().strip()
			if text is not '':
				print('momo0:', text)
		#time.sleep(1)

	pm0.terminate()
	pm0.wait()
	print("end momo0")

momoP1 = './momo-2022.1.0_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video1 sora --signaling-url wss://sora.ikeilabsora.0am.jp/signaling --channel-id twincam-right --multistream 1 --role sendonly --video-codec-type H264 --video-bit-rate 15000'
# momoP1 = './momo-2021.6.0_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video1 sora --signaling-url wss://sora.ikeilabsora.0am.jp/signaling --channel-id rabbit-go@twincamright --role sendonly --video-codec-type H264 --video-bit-rate 15000'
#momoP1 = './momo-2021.2.3_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video1 --insecure sora wss://sora.ikeilabsora.0am.jp/signaling rabbit-go@twincamright --role sendonly --video-codec-type H264 --video-bit-rate 15000'
#momoP1 = './momo-2021.2.3_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video1 --insecure test'
runmomo1 = True
def momo1():
	pm1 = subprocess.Popen(momoP1, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	#os.set_blocking(pm1.stdout.fileno(), False)
	print('run momo1')
	while runmomo1:
		if pm1.poll() is None:
			text = pm1.stdout.readline().decode().strip()
			if text is not '':
				print('momo1:', text)
		#time.sleep(1)

	pm1.terminate()
	pm1.wait()
	print("end momo1")

#socat pty,echo=0,raw,link=./serial_out pty,raw,echo=0,link=./serial_in


if __name__ == '__main__':
	theta0_Th = threading.Thread(target = openTHETA0)
	theta0_Th.start()
	time.sleep(6)
	theta1_Th = threading.Thread(target = openTHETA1)
	theta1_Th.start()
	time.sleep(3)
	momo0_Th = threading.Thread(target = momo0)
	momo0_Th.start()
	time.sleep(2)
	momo1_Th = threading.Thread(target = momo1)
	momo1_Th.start()
	mainRun = True
	try:
		while mainRun:
			time.sleep(100)
			pass
	except KeyboardInterrupt:
		runmomo0 = False
		runmomo1 = False
		time.sleep(2)

		runTheta0 = False
		runTheta1 = False
		time.sleep(2)
		mainRun = False
		print("------END--------Press Ctrl+C again if not end")
