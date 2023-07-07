#!/bin/bash
source /home/tristar/.bashrc
systemctl --user stop twincam-motor.service
gnome-terminal -- bash -c "echo twincam-motor.sh; source /home/tristar/.bashrc; cd /home/tristar/MyWork-NX4_6/; /home/tristar/MyWork-NX4_6/twincam-i2c.py"
