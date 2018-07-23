from collections import defaultdict
import bme680
import time
import os
import csv
import sys
import socket

SAMPLE_INT = 60

def get_nodes(csv_file):
	node_id = defaultdict(dict)

	with open(csv_file, 'r') as f:
		for row in csv.reader(f, delimiter=','):
			node_id[row[0]].update({row[1]: row[2]})

	return node_id

def init_sensor():
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
	burn_in_time = 300

	while curr_time - start_time < burn_in_time:
		curr_time = time.time()
		if sensor.get_sensor_data() and sensor.data.heat_stable:
			sensor.data.gas_resistance
			time.sleep(SAMPLE_INT)

	return sensor

def ingest_node(t, data, unit, node_id):
	cmd = ('./grpc_client/client --datetime={} --data={} --unit={} --id={}'
			.format(t, data, unit, node_id))
	os.popen(cmd).read()

try:
	loc = socket.gethostname()
	sensor = init_sensor()
	node_id = get_nodes('node_id.csv')

	while True:
		if sensor.get_sensor_data():
			t = int(round(time.time() * 1000))
			ingest_node(t, sensor.data.temperature, 'C', node_id[loc]['temp'])
			ingest_node(t, sensor.data.pressure, 'hPa', node_id[loc]['pres'])
			ingest_node(t, sensor.data.humidity, '%', node_id[loc]['hum'])
			if sensor.data.heat_stable:
				ingest_node(t, sensor.data.gas_resistance, "Ohm", node_id[loc]['gas'])
		time.sleep(SAMPLE_INT)

except KeyboardInterrupt:
	pass
