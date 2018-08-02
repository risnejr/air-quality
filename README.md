# Read Sensor
Intent of repository is to fetch sensor data from **BME680** and ingest the data to SKF's **Enlight**.
## Required files
```
.
├── client
│   └── client
└── read_sensor.py
```
## Build to Raspberry Pi Zero
```
$ cd client
$ env GOOS=linux GOARCH=arm GOARM=6 go build -o client
```
---
P.S. The client stub is written in go since armv6 doesn't fully support gRPC communication with Python
