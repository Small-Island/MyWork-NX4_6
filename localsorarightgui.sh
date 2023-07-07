#!/bin/bash
source /home/tristar/.bashrc
systemctl --user stop twincam-theta.service
gnome-terminal -- bash -c "echo localsorarightgui.sh; source /home/tristar/.bashrc; cd /home/tristar/MyWork-NX4_6/; ./localsoraright.py"
