# Flask Server for Raspberry Pi Room Control

My web server to control Various lights and fans via GPIO pins on RPI.

---

## Screenshots

|  New Interface (Default)  | Old Interface |
| --- | ----------- |
| ![Default Interface](image/default_interface.png) | ![Old Interface](image/old_interface.png) |

---

## Install

### Method 1 (Automatic)

```sh
$ curl -sSL https://raw.githubusercontent.com/HritwikSinghal/room_control_server/master/install.sh | bash
```

The server will start automatically on Network connect. You can check the status of server by below command.

```
$ sudo systemctl status room_control_flask.service
```

### Method 2 (Manual)

Clone this repository using

```sh
$ cd ~
$ git clone https://github.com/HritwikSinghal/room_control_server
```

Enter the directory and install all the requirements using

```sh
$ cd room_control_server
$ pip3 install -r requirements.txt
```

(Optional) Enable Systemd service to start on network connect

```sh
$ sudo chmod +x room_control_flask.service
$ sudo cp room_control_flask.service /etc/systemd/system/
$ sudo systemctl enable room_control_flask.service
$ sudo systemctl start room_control_flask.service
```

Run the app (or don't if it was started in last step)

```sh
$ python3 __init__.py
```

---

## License

[GPLv3](/LICENSE)

Thanks to [RPi-Flask-WebServer](https://github.com/Mjrovai/RPi-Flask-WebServer) and
[NetworkChuck](https://github.com/theNetworkChuck/NetworkChuck) for providing base code.  
