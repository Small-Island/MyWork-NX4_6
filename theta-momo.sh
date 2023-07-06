#!/bin/bash
sleep 4s
cd /home/tristar/MyWork-NX4_6
./local_webrtc_momo.run
sleep 1s;
./twincam-i2c.py &
sleep 1s
/home/tristar/MyWork-NX4_6/wakeup_theta.py
sleep 1s
/home/tristar/MyWork-NX4_6/wakeup_theta.py
sleep 1s
/home/tristar/MyWork-NX4_6/THETA_Cameras/camera0/gst_loopback &
sleep 2s
#./momo-2022.2.0_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --resolution 4K --use-sdl --show-me --video-device /dev/video0 sora --signaling-url ws://192.168.11.64:5000/signaling --channel-id mobile-twincam-left --multistream 1 --role sendonly --video-codec-type H264 --video-bit-rate 15000
./momo-2022.2.0_ubuntu-18.04_armv8_jetson_xavier/momo --hw-mjpeg-decoder=false --metrics-port 8081 --resolution 4K --video-device /dev/video0 sora --signaling-url wss://sora.ikeilabsora.0am.jp/signaling --channel-id mobile-twincam-left --multistream 1 --role sendonly --video-codec-type H264 --video-bit-rate 15000
#./momo-2021.2.3_ubuntu-18.04_armv8_jetson_xavier/momo --log-level 2 --metrics-port 8081 --insecure --force-i420 --hw-mjpeg-decoder=false --resolution 3840x1920 --video-device /dev/video0 sora wss://sora.ikeilabsora.0am.jp/signaling mobile-twincam-left --multistream 1 --role sendrecv --video-codec-type VP9 --video-bit-rate 15000
