# Read Sensor
Fetches sensor data from a **BME680** sensor and ingest the data to SKF's **Enlight**.
## Build to Raspberry Pi Zero
```
$ env GOOS=linux GOARCH=arm GOARM=6 go build -o client
```
---
P.S. The client stub is written in go since armv6 doesn't fully support gRPC communication with Python
