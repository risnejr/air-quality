import bme680
import time
import os
import sys
import socket

if socket.gethostname() == 'desk':
    TEMP_ID = "59959859-2dc6-4689-bf24-fda966cb4012"
    QUALITY_ID = "8b7b50e4-6be3-4f4e-8abe-6efc0c1063b1"

elif socket.gethostname() == 'cabinet':
    TEMP_ID = "c52fcf61-3599-404a-9492-0b720a469f22"
    QUALITY_ID = "e8e1e003-ae83-4a7e-8190-c08c36811415"

sensor = bme680.BME680()

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)
sensor.set_temp_offset(-4)

start_time = time.time()
curr_time = time.time()
burn_in_time = 420

burn_in_data = []

def ingest_node(t, data, unit, node_id):
    cmd = ('./grpc_client/client --datetime={} --data={} --unit={} --id={}'
            .format(t, data, unit, node_id))
    os.popen(cmd).read()

def get_air_quality():
    gas = sensor.data.gas_resistance
    gas_offset = gas_baseline - gas

    hum = sensor.data.humidity
    hum_offset = hum - hum_baseline

    # Calculate hum_score as the distance from the hum_baseline.
    if hum_offset > 0:
        hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)

    else:
        hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

    # Calculate gas_score as the distance from the gas_baseline.
    if gas_offset > 0:
        gas_score = (gas / gas_baseline) * (100 - (hum_weighting * 100))

    else:
        gas_score = 100 - (hum_weighting * 100)

    # Calculate air_quality_score.
    air_quality_score = hum_score + gas_score

    return air_quality_score

try:
    # Collect gas resistance burn-in values, then use the average
    # of the last 50 values to set the upper limit for calculating
    # gas_baseline.
    # print("Collecting gas resistance burn-in data for 7 mins\n")
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            burn_in_data.append(gas)
            # sys.stdout.write("Gas: {0:.2f} Ohms".format(gas))
            # sys.stdout.flush()
            # sys.stdout.write('\r')
            # sys.stdout.flush()
            time.sleep(5)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0

    # Set the humidity baseline to 40%, an optimal indoor humidity.
    hum_baseline = 40.0

    # This sets the balance between humidity and gas reading in the
    # calculation of air_quality_score (25:75, humidity:gas)
    hum_weighting = 0.25

    while True:
        if sensor.get_sensor_data():
            t = int(round(time.time() * 1000))
            ingest_node(t, sensor.data.temperature, "Celsius", TEMP_ID)
            if sensor.data.heat_stable:
                ingest_node(t, get_air_quality(), "%", QUALITY_ID)
        time.sleep(5)

except KeyboardInterrupt:
    pass
