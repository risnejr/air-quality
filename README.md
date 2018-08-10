# Air quality
This repository consists of several modules that together serves as an air quality monitoring system.

## Flow between services
![image](https://user-images.githubusercontent.com/16987380/43758634-0a058560-9a1d-11e8-8c8e-7110207c8e62.png)

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
│       ├── ca.crt
│       ├── client.crt
│       └── client.key
├── config
├── dashboard
├── read_sensor
└── vote
```
### `aq-level`
The air quality level module predicts the air quality into three different different categories which are either `Good`, `Ok` or `Bad`. This is done by listening to the **gRPC** stream from **Enlight IoT** and letting a *Deep Neural Network* (DNN) making a prediction every time all of the desired inspection points (values the **BME680** sensor reads) are updated.

The DNN is trained by manual labels which is a continuous process and these labels are fetched from the `vote` module.
```
$ cd aq-level
$ python3 main.py &
```
```
$ cd aq-level
$ python3 -m unittest discover -v
```
### `config`
Config is meant to generate the required `config.json` file which is required by all of the other modules (see "flowchart" above).
```
$ cd config
$ python3 config.py --id <node_id from functional location>
```
### `dashboard`
The dashboard consists of a flask server in the backend which reads the **gRPC** stream connected to **Enlight IoT**. It filters down and send *server-sent events* (sse) based on the given functional location and asset. The client side is built upon react which gets this data from the flask app using an EventSource.
```
$ cd dashboard/server
$ go run sse.go &
```
```
$ cd dashboard/client
$ yarn run &
```
### `read_sensor`
This module is meant to be running on a **RPi Zero W** with a **BME680** sensor attached. The script also supports backfilling data if the device loses internet connection.

Choosing host name on the **RPi** must follow the naming convention `functional_location-asset`, for an example, `install_team_room-cabinet`.
```
$ cd read_sensor
$ python3 read_sensor.py &
```
### `vote`
Vote module consists of a client which is setup to send HTTP POST requests to an **AWS Lambda** which ingests the node data, generated by the user, to **Enlight IoT**. Voting on a specific asset is done by using the URL parameters `func_loc` and `asset`.
```
$ cd vote
$ yarn deploy
```
