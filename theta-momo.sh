#!/bin/bash
sleep 3s
cd /home/tristar/MyWork-NX4_6
./local_webrtc_momo.run
sleep 2s;
./twincam-i2c.py &
sleep 2s;
./twincam-i2c.py &
sleep 6s
/home/tristar/MyWork-NX4_6/wakeup_theta.py
sleep 1s
/home/tristar/MyWork-NX4_6/THETA_Cameras/camera0/gst_loopback &
sleep 2s
./momo-2022.2.0_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --video-device /dev/video0 sora --signaling-url wss://sora.ikeilabsora.0am.jp/signaling --channel-id mobile-twincam-right --multistream 1 --role sendrecv --video-codec-type H264 --video-bit-rate 15000
