#!/bin/bash
#
# script executed by crontab on reboot
# !!! DON'T forget to run this to format the file correctly:
# sed -i 's/\r//' script.sh

# Run the Python script
export USER=pi
nohup python3 /home/pi/Documents/office-station/main.py &
#
# Function to check internet connectivity
check_internet() {
    ping -q -c 1 -W 2 8.8.8.8 > /dev/null 2>&1
    return $?
}
#
# Wait until an internet connection is available
while ! check_internet; do
    echo "No internet connection. Retrying in 5 seconds..."
    sleep 5
done
#
# Start the VNC server on display :1
nohup vncserver :1 > /home/pi/Documents/vncserver.log 2>&1 &
#
# Establish an SSH tunnel so the public Ubuntu server can connect to it
ssh -i /home/pi/Documents/ubuntu_oracle.key -f -N -R 5910:localhost:5901 ubuntu@darkquarx.be