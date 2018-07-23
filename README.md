# Air Quality
Intent of repository is to fetch sensor data from **BME680** and ingest the data to SKF's **Enlight**. 
## Required files
```
.
├── cert
│   ├── ca.crt
│   ├── client.crt
│   └── client.key
├── grpc_client
│   ├── client.go
│   ├── glide.lock
│   └── glide.yaml
├── node_id.csv
└── read_sensor.py
```
---
P.S. The client stub is written in go since armv6 doesn't fully support gRPC communication with Python
