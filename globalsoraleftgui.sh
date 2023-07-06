#!/bin/bash
source /home/tristar/.bashrc
systemctl --user stop theta-momo.service
gnome-terminal -- bash -c "echo globalsoraleftgui.sh; source /home/tristar/.bashrc; cd /home/tristar/MyWork-NX4_6/; ./globalsoraleft.py"
