# Air quality 😷
This repository consists of several modules that together serves as an air quality monitoring system.

## Prerequisites
To use the different modules in this repository you're required to use the softwares listed below.

### Raspberry Pi sensor collection
If your only plan is to set up a Raspberry Pi (**RPi**) you'll only need the following:
*   [PiBakery](http://www.pibakery.org/)
*   `pibakery.xml` file from this repository

### Dashboard to visualize live data
However if you plan on using the dashboard you'll need the following:
*   [yarn](https://yarnpkg.com/en/)
*   [go](https://golang.org/)
*   [dep](https://github.com/golang/dep)

And the project can be installed via `go get`:
```
$ go get -u github.com/risnejr/air-quality
```

## Installation (setup a new **RPi**)
To configure a new **RPi** to automatically read the sensor values on boot you'll need to use [PiBakery](http://www.pibakery.org/). There's currently a `pibakery.xml` located in the root of the repository, this is the recipe used to automatically install the **RPi**. Start by importing the `pibakery.xml` into PiBakery and follow the instructions below. 

Also, choosing hostname on the **RPi** must follow the naming convention `functional_location-asset`, for an example, `install_team_room-desk`. **Functional Location** can be a room or a specific area within your office location while **Asset** is a specific point where you choose to locate your device. Configuration steps follows below.

All the configuration is done within PiBakery. An example, setting the hostname requires you to modify the field *Set host name to `functional_location-asset`* inside PiBakery. The image below highlights the fields which needs to be manually configured.

1.  [Import](http://www.pibakery.org/docs/importexport.html) the `pibakery.xml` file.
2.  Configure the highlighted sections to match your setup.
3.  [Write](http://www.pibakery.org/docs/create.html) configuration to your SD-card (don't forget to insert it into your computer).

![image](https://user-images.githubusercontent.com/16987380/44849251-d1662800-ac59-11e8-9ceb-6b2c91f5ebd9.png)

Once the image is burnt, insert the micro SD card into your **RPi** and plug it into the power supply. Make sure that your device is within range of chosen WiFi. If you aren't, the required packages such as git and pip won't be installed and nothing will happen. 

Depending on your internet connection the first and every other boot will vary in time. However, first boot is time consuming and it's not weird if it takes 15 minutes from plugging your device into the power outlet until you can see your data in **Analyze**.

## Flow between services

![image](https://user-images.githubusercontent.com/16987380/44774916-a8b83280-ab74-11e8-93f0-cfcbc296805d.png)

## The different modules
Remember, certificates are needed to establish a connection to **Enlight Hierarchy**, **IoT** and **PAS**.

```
.
├── aq_level
├── build_hierarchy
├── certs               <----
│   ├── hierarchy
│   │   ├── ca.crt
│   │   ├── client.crt
│   │   └── client.key
│   ├── pas
│   │   ├── ca.crt
│   │   ├── client.crt
│   │   └── client.key
│   └── iot
│       ├── ca.crt
│       ├── client.crt
│       └── client.key
├── dashboard
├── gen_config
├── read_sensor
└── vote
```
### `aq_level`
```
This module is NOT up to date and requires some further improvements to play nicely with the other modules.
```

The air quality level module predicts the air quality into three different different categories which are either `Good`, `Ok` or `Bad`. This is done by listening to the **gRPC** stream from **Enlight IoT** and letting a *Deep Neural Network* (DNN) making a prediction every time all of the desired inspection points (values the **BME680** sensor reads) are updated.

The DNN is trained by manual labels which is a continuous process and these labels are fetched from the `vote` module.

### `build_hierarchy`
Generates an **Enlight hierarchy** based on the **RPi's** hostname. The generated inspection points are based on the data which is collectable from the **BME680** sensor. Thus temperature, humidity, pressure and volatile gases.  

### `dashboard`
The dashboard's backend reads the **gRPC** stream connected to **Enlight IoT**. It filters down and send *server-sent events* (sse) based on the given functional location and asset. The client side is built with react which gets this data from the go server using an EventSource.

Viewing live data from a specific asset requires you to enter the URL parameters `func_loc` and `asset` while using the client. These parameters reflect the hierarchies functional location and asset i.e. the hostname given to your device. Below is an image depicting the hierarchy view inside Enlight. 

![image](https://user-images.githubusercontent.com/16987380/44843289-4466a300-ac48-11e8-83e7-e1f7e56ff608.png)

To visualize these inspection points in your browser you need to append `?func_loc=install_team&asset=desk` to your client side URL i.e. if your using it locally the entire URL would be `localhost:3000/?func_loc=install_team&asset=desk`.

#### Update your configuration file (requires go and dep)
Make sure to change directory to `air-quality/gen_config` and run the following
```
$ dep ensure
$ go build -o config
$ ./config
```

#### Start the client on your computer (requires yarn)
Make sure to change directory to `air-quality/dashboard/client` and run the following
```
$ yarn
$ yarn start
```
#### Start the server on your computer (requires go and dep)
Make sure to change directory to `air-quality/dashboard/server` and run the following
```
$ dep ensure
$ go build -o sse
$ ./sse
```
### `gen_config`
Generates the required `config.json` file which is required by all of the other modules (see "flowchart" above).

### `read_sensor`
This module is meant to be running on a **RPi Zero W** with a **BME680** sensor attached. The script also supports backfilling data if the device loses internet connection.

### `vote`
```
This module is NOT up to date and requires some further improvements to play nicely with the other modules.
```

Vote module consists of a client which is setup to send HTTP POST requests to an **AWS Lambda** which ingests the node data, generated by the user, to **Enlight IoT**. Voting on a specific asset is done by using the URL parameters `func_loc` and `asset`.
