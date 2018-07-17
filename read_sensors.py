import bme680
import time
import os
import sys
import socket

if socket.gethostname() == 'desk':
	TEMP_ID = "3ae5f21e-e1de-49b6-8455-cf78af5f52bb"
	PRES_ID = "3ec3bcc1-1f10-414e-878d-5ba4e9f16e60"
	HUM_ID = "f1b3f822-e6fd-467c-9170-2ad06265d108"
	GAS_ID = "d27e7540-5f6c-472c-9f8d-cc0e2623a5ff"

elif socket.gethostname() == 'cabinet':
	TEMP_ID = "1c4595b8-c174-4336-bb5f-83a5a7f41e0c"
	PRES_ID = "8c0bc306-2b7e-4367-852d-159b88059302"
	HUM_ID = "b6a9114b-7f92-4827-98dc-87f723ac1a5d"
	GAS_ID = "de249370-5358-4cfb-a89d-d9a0da80b6b0"

sensor = bme680.BME680()

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)
sensor.set_temp_offset(-4)

start_time = time.time()
curr_time = time.time()
burn_in_time = 420

def ingest_node(t, data, unit, node_id):
	cmd = ('./grpc_client/client --datetime={} --data={} --unit={} --id={}'
			.format(t, data, unit, node_id))
	os.popen(cmd).read()

try:
	while curr_time - start_time < burn_in_time:
		curr_time = time.time()
		if sensor.get_sensor_data() and sensor.data.heat_stable:
			sensor.data.gas_resistance
			time.sleep(5)

	while True:
		if sensor.get_sensor_data():
			t = int(round(time.time() * 1000))
			ingest_node(t, sensor.data.temperature, 'C', TEMP_ID)
			ingest_node(t, sensor.data.pressure, 'hPa', PRES_ID)
			ingest_node(t, sensor.data.humidity, '%', HUM_ID)
			if sensor.data.heat_stable:
				ingest_node(t, sensor.data.gas_resistance, "Ohm", GAS_ID)
		time.sleep(5)

except KeyboardInterrupt:
	pass
