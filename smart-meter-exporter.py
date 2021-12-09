#!/usr/bin/env python
import signal
import sys
from prometheus_client import start_http_server, Enum, Gauge
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4
import logging
import argparse

# prometheus metrics
current_elec_usage = Gauge('current_elec_usage', 'Current electricity usage (kW)')
instant_voltage = Gauge('instant_voltage', 'Instantaneous voltage L1 (V)')
instant_current = Gauge('instant_current', 'Instantaneous current L1 (A)')
tariff_1_elec = Gauge('tariff_1_elec', 'Electicity usage for tarrif 1 (kWh)')
tariff_2_elec = Gauge('tariff_2_elec', 'Electicity usage for tarrif 2 (kWh)')
active_tariff = Enum('active_tariff', 'Current tariff', states=['tarrif_1', 'tarrif_2'])
pwr_fail = Gauge('pwr_fail_cnt', 'Number of power failures (short or long)')
v_sag = Gauge('voltage_sag_cnt', 'Number of voltage sags')
v_swell = Gauge('voltage_swell_cnt', 'Number of voltage swell')

def signal_handler(sig, frame):
    logging.info('Stopping smart meter exporter')
    sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser(description='Monitoring process for reading Dutch smart meters and exposing data for Prometheus to scrape')
    parser.add_argument('port', type=int, help='Prometheus endpoint port')
    parser.add_argument('device', type=str, help='P1 USB device (i.e. "/dev/ttyUSB0")')
    args = parser.parse_args()

    return (args.port, args.device)

if __name__ == '__main__':
    port, usb_dev = parse_args()

    # trap SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    logging.basicConfig(level=logging.DEBUG)
    logging.info('Smart meter monitoring started')

    # Start up the server to expose the metrics.
    start_http_server(port)
    logging.info(f"Prometheus client started on port {port}")

    # dsmr stuff
    serial_reader = SerialReader(
        device=usb_dev,
        serial_settings=SERIAL_SETTINGS_V4,
        telegram_specification=telegram_specifications.V5
    )
    logging.info(f"Reading smart meter on {usb_dev}")

    tariff_states = {
        1 : 'tarrif_1',
        2 : 'tarrif_2',
    }

    # start reading smart meter
    for telegram in serial_reader.read_as_object():
        current_elec_usage.set(telegram.CURRENT_ELECTRICITY_USAGE.value)
        instant_voltage.set(telegram.INSTANTANEOUS_VOLTAGE_L1.value)
        instant_current.set(telegram.INSTANTANEOUS_CURRENT_L1.value)
        tariff_1_elec.set(telegram.ELECTRICITY_USED_TARIFF_1.value)
        tariff_2_elec.set(telegram.ELECTRICITY_USED_TARIFF_2.value)
        v_sag.set(telegram.VOLTAGE_SAG_L1_COUNT.value)
        v_swell.set(telegram.VOLTAGE_SWELL_L1_COUNT.value)
        current_tariff = int(telegram.ELECTRICITY_ACTIVE_TARIFF.value)
        active_tariff.set(tariff_states[current_tariff])
