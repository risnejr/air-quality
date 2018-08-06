# Air quality
This repository consists of several modules that together serves as an air quality monitoring system.

## Flow between services
![image](https://user-images.githubusercontent.com/16987380/43726032-5ef469e4-999e-11e8-8fa6-f6cd60a8c34a.png)

## The different modules
All the instructions below assumes that you've cloned this repository and standing in the root folder of the project. Certificates are also needed to establish a connection to both **Enlight Hierarchy** and **IoT**.

```
.
├── aq_level
├── certs               <---- 
│   ├── hierarchy
│   │   ├── ca.crt
│   │   ├── client.crt
│   │   └── client.key
│   └── iot
│   │   ├── ca.crt
│   │   ├── client.crt
│   │   └── client.key
├── config
├── dashboard
├── read_sensor
└── vote
```
### Air quality level (aq_level)
TODO
### Generate config file (config)
TODO
### Dashboard (dashboard)
TODO
### Read sensor (read_sensor)
This module is meant to be running on a **RPi Zero W** with a **BME680** sensor attatched. The script also supports backfilling data if the device loses internet connection.

TODO
### Vote (vote)
TODO

