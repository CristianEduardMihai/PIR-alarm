sudo apt update
sudo apt -y install \
ffmpeg \
python3-pip \
fswebcam

pip3 install -r requirements.txt

#alarm service

printf "Description=Running the alarm on boot
[Service]
Environment=XDG_RUNTIME_DIR=/run/user/1000
ExecStart=/bin/bash -c 'python3 -u /home/$USER/PIR-alarm/alarm.py'
WorkingDirectory=/home/$USER/PIR-alarm
Restart=always
User=$USER
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/alarm.service

sudo systemctl enable alarm.service
sudo systemctl start alarm.service