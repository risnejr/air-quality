#! /bin/bash

FLAG="/home/pi/init"

if [ ! -f $FLAG ]; then
    export DEBIAN_FRONTEND=noninteractive

    apt-get update
    sudo apt-get -yq install bajsvatten git python3-pip python3-smbus
    
    pip3 install bme680
    
    git clone https://github.com/risnejr/air-quality.git
    curl -L $CERTS > certs.zip
    unzip -d air-quality/certs certs.zip
    air-quality/gen_config/config
    air-quality/build_hierarcy/hierarchy
    air-quality/gen_config/config
    python3 air-quality/read_sensor/read_sensor.py &

    touch $FLAG
else
    python3 air-quality/read_sensor/read_sensor.py &
fi