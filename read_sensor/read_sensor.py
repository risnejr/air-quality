from threading import Thread

import bme680
import time
import os
import socket
import json
import os.path


def internet(host='8.8.8.8', port=53, timeout=3):
    global recover

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        recover = True
        return False


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
    global my_path

    cmd = os.path.join(my_path,
                       ('client/client --time={} --data={} --unit={} --id={} &'
                       .format(t, data, unit, node_id)))
    os.system(cmd)


def buffer_data(t):
    backfill[node_ids['temperature']]['data'].append((t, sensor.data.temperature))
    backfill[node_ids['pressure']]['data'].append((t, sensor.data.pressure))
    backfill[node_ids['humidity']]['data'].append((t, sensor.data.humidity))
    if sensor.data.heat_stable:
        backfill[node_ids['gas']]['data'].append((t, sensor.data.gas_resistance))


def backfill_data(backfill):
    for node_id in backfill.keys():
        for t, value in backfill[node_id]['data']:
            ingest_node(t, value, backfill[node_id]['unit'], node_id)


def reset_backfill():
    global backfill

    backfill = {node_ids['temperature']: {'unit': 'C', 'data': []},
                node_ids['pressure']: {'unit': 'hPa', 'data': []},
                node_ids['humidity']: {'unit': '%', 'data': []},
                node_ids['gas']: {'unit': 'Ohm', 'data': []}}


def read_data(node_ids, sampling_interval):
    global recover

    while True:
        if sensor.get_sensor_data():
            t = int(round(time.time() * 1000))
            if not internet():
                buffer_data(t)
            elif recover:
                Thread(target=backfill_data, args=(backfill,)).start()
                reset_backfill()
                recover = False
            else:
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
    my_path = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(my_path, "../config.json")

    with open(config_file, 'r') as f:
        node_ids = json.load(f)[func_loc][asset]

    recover = False
    reset_backfill()
    sensor = init_sensor()
    read_data(node_ids, 30)
