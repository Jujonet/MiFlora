# MiFlora
Python script to interpret the MiFlora values and generate simple HTML page

# Installation was done on a Raspberry Pi 2 & 3.

Optional: only required if the apt-get version of Bluez fails: Bluez Bluetooth stack
```
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.46.tar.xz
tar xvf bluez-5.46.tar.xz
sudo apt-get update
sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
./configure
make
```
Optional: Go language if the apt-get version doesn't work
```
wget https://storage.googleapis.com/golang/go1.9.linux-armv6l.tar.gz
sudo tar -C /usr/local -xzf go1.9.linux-armv6l.tar.gz
export PATH=$PATH:/usr/local/go/bin
```

Required. Could be more python dependancies that I'm missing here. install them with apt-get or pip. You'll find the errors when you run the script.
```
sudo apt-get install python-matplotlib
sudo apt-get install bluetooth bluez-utils blueman bluez python-gobject python-gobject-2
sudo pip install pandas
```

Barnybug's Miflora tool
```
go get github.com/barnybug/miflora/cmd/miflora
```

Finding the MiFlora stick and testing.
```
sudo hcitool lescan
/home/pi/go/bin/miflora C4:7C:8D:63:7E:38 hci0
```

# Settings
Read through the file, everything is hard-coded but easy to understand




Despues de meterle tantas cosas al script, las lista de soft se me quedo en:
```
sudo apt-get install python-whichcraft python-dateutil python-numpy python-matplotlib python-sh python-regex python-pandas python-path python-paramiko python-scp python-pip python-setuptools
sudo pip install python-pushover

```


