#!/usr/bin/env bash

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

# from https://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself
SCRIPTPATH="$(
  cd "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"
SCRIPT_PATH=$(dirname $(realpath -s $0))

echo -e "

        ██████╗░██████╗░██╗  ███████╗██╗░░░░░░█████╗░░██████╗██╗░░██╗
        ██╔══██╗██╔══██╗██║  ██╔════╝██║░░░░░██╔══██╗██╔════╝██║░██╔╝
        ██████╔╝██████╔╝██║  █████╗░░██║░░░░░███████║╚█████╗░█████═╝░
        ██╔══██╗██╔═══╝░██║  ██╔══╝░░██║░░░░░██╔══██║░╚═══██╗██╔═██╗░
        ██║░░██║██║░░░░░██║  ██║░░░░░███████╗██║░░██║██████╔╝██║░╚██╗
        ╚═╝░░╚═╝╚═╝░░░░░╚═╝  ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝

        ░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░
        ██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗
        ╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝
        ░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗
        ██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║
        ╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝

"

echo -e "
			－ Ｂｙ Ｈｒｉｔｗｉｋ Ｓｉｎｇｈａｌ
"

printf "\n ${grn} Cloning Repo ${end} "
sudo rm -rf /usr/local/sbin/room_control_server/
sudo git clone --depth 1 -b master https://github.com/HritwikSinghal/room_control_server /usr/local/sbin/room_control_server/
cd /usr/local/sbin/room_control_server/ || exit
sudo rm -rf .git/

printf "\n ${grn} Installing Requirements ${end} "
sudo pip3 install -r ./requirements.txt

printf "\n ${grn} Enabling Systemd service ${end} "
sudo chmod +x room_control_flask.service

if [ -e /etc/systemd/system/room_control_flask.service ]; then
  sudo systemctl stop room_control_flask.service
  sudo systemctl disable room_control_flask.service
  sudo rm /etc/systemd/system/room_control_flask.service
  echo "Removed old service"
fi

sudo cp room_control_flask.service /etc/systemd/system/
sudo systemctl enable room_control_flask.service
sudo systemctl start room_control_flask.service

sudo ln -sf /usr/local/sbin/room_control_server/app/static/room_control.py ~

echo -e "


			██████╗░░█████╗░███╗░░██╗███████╗
			██╔══██╗██╔══██╗████╗░██║██╔════╝
			██║░░██║██║░░██║██╔██╗██║█████╗░░
			██║░░██║██║░░██║██║╚████║██╔══╝░░
			██████╔╝╚█████╔╝██║░╚███║███████╗
			╚═════╝░░╚════╝░╚═╝░░╚══╝╚══════╝

"

printf "\n\n All done. The server will start automatically on Network connect!"
