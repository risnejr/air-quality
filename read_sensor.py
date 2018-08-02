import bme680
import time
import os
import socket
import json


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

    return sensor


def ingest_node(t, data, unit, node_id):
    cmd = ('./client/client --time={} --data={} --unit={} --id={}'
           .format(t, data, unit, node_id))
    os.popen(cmd).read()


def read_data(node_ids, sampling_interval):
    while True:
        if sensor.get_sensor_data():
            t = int(round(time.time() * 1000))
            try:
                ingest_node(t, sensor.data.temperature, 'C', node_ids['temperature'])
                ingest_node(t, sensor.data.pressure, 'hPa', node_ids['pressure'])
                ingest_node(t, sensor.data.humidity, '%', node_ids['humidity'])
                if sensor.data.heat_stable:
                    ingest_node(t, sensor.data.gas_resistance, "Ohm", node_ids['gas'])
            except KeyError as e:
                print('Asset {} not present in .csv file'.format(e))
                raise
        time.sleep(sampling_interval)


if __name__ == '__main__':
    func_loc, asset = socket.gethostname().split('-')

    with open('../config.json', 'r') as f:
        node_ids = json.load(f)[func_loc][asset]

    sensor = init_sensor()
    read_data(node_ids, 30)
