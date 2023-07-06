#!/bin/bash
source /home/tristar/.bashrc
systemctl --user stop theta-momo.service
gnome-terminal -- bash -c "echo globalsorarightgui.sh; source /home/tristar/.bashrc; cd /home/tristar/MyWork-NX4_6/; ./globalsoraright.py"
