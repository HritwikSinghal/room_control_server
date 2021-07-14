# Flask Server for Raspberry Pi Room Control

My web server to control Various lights and fans via GPIO pins on RPI.

## Usage

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
$ sudo systemclt enable room_control_flask.service
$ sudo systemclt start room_control_flask.service
```

Run the app (or don't if it was started in last step)

```sh
$ python3 __init__.py
```

## License

[GPLv3](/LICENSE)

Thanks to [RPi-Flask-WebServer](https://github.com/Mjrovai/RPi-Flask-WebServer) and 
[NetworkChuck](https://github.com/theNetworkChuck/NetworkChuck) for providing base code.  
