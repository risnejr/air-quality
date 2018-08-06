# Air quality level
User generated air quality levels in an office environment using data collected with a **RPi** and a **BME680** sensor. 
## Generate code from proto files
```
python3 -m pip install --user grpcio-tools
python3 -m grpc_tools.protoc -I ./alarm_level/proto --python_out=./alarm_level --grpc_python_out=./alarm_level ./alarm_level/proto/grpcapi.proto
```
## Run unit tests
```
python3 -m unittest discover -v
```
