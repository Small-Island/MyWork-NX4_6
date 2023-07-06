#!/bin/bash
source /home/tristar/.bashrc
systemctl --user stop theta-momo.service
gnome-terminal -- bash -c "echo localsoraleftgui.sh; source /home/tristar/.bashrc; cd /home/tristar/MyWork-NX4_6/; ./localsoraleft.py"
