from scapy.all import *
import logging
from sixlowpan_parser.database import csv_collector

def custom_payload_parser(payload):
    """
    custom_payload_parser is a callback for a custom payload parser.
    This parse's  payload format is like ..
    3,150,17941,293098,3208,311025,307817,615,65535,483,8,65427,37,134
    """
    logger = logging.getLogger("parser.custom_payload_parser")
    voltage = 3
    tick_per_seconds = 4096
    power_cpu = 1.8 * voltage
    power_lpm = 0.0545 * voltage
    power_transmit = 17.7 * voltage
    power_listen = 20.0 * voltage

    if type(payload) is bytes:
        payload = payload.decode('UTF-8')

    strip_payload = list(map(int, payload.split(",")))

    data = dict()
    data['number_of_neighbour'] = strip_payload[0]
    data['ETX'] = strip_payload[1] / 8.0
    data['CPUPower'] = (strip_payload[2] * power_cpu) / (strip_payload[2] + strip_payload[3])
    data['LPMPower'] = (strip_payload[3] * power_lpm) / (strip_payload[2] + strip_payload[3])
    data['TransmitPower'] = (strip_payload[4] * power_transmit) / (strip_payload[2] + strip_payload[3])
    data['ListenRadioPower'] = (strip_payload[6] * power_listen) * (strip_payload[2] + strip_payload[3])
    data['Temperature'] = strip_payload[7]
    data['Humidity'] = (strip_payload[8] * 405.0 / 10000.0) - 4.0
    data['BeaconInterval'] = strip_payload[9]
    data['RSSI'] = strip_payload[10]
    data['LQI'] = strip_payload[11]
    data['battery_voltage'] = strip_payload[12]
    logger.debug(data)
    return data

class PCAPParser:
    def __init__(self, pcap_path, output):
        conf.dot15d4_protocol = "sixlowpan"
        self.pcap_path = pcap_path
        self.result = dict()
        self.output = output
        self.logger = logging.getLogger("parser.PCAPParser")
        try:
            self.logger.info("extracing packages from pcap files, please wait.. it might take a moment.")
            self.packets = rdpcap(self.pcap_path)
        except Scapy_Exception as e:
            self.logger.info("not a valid pcap file")
        except FileNotFoundError as e:
            self.logger.info("file not found")
        self.pcap_total_packets = len(self.packets)
        self.logger.info("Found {} packets in pcap file".format(self.pcap_total_packets))
        self.packet_info_list = list()

    def report_summry(self, info_list):
        self.logger.info("Number of UDP packets: {}".format(len(info_list)))

    def run(self, parser_callback = custom_payload_parser, collect_callback = csv_collector):
        if parser_callback is None:
            self.logger.info("Invalid parser callback, skip running")
            return
        for packet in self.packets:
            if packet.haslayer(UDP):
             udp_meta_info = packet.getlayer(UDP)
             udp_payload = udp_meta_info.payload.load
             payload_info = parser_callback(udp_payload)
             self.packet_info_list.append(payload_info)

        if collect_callback is not None:
            self.logger.info("Finising parsing packets. Calculating packets..")
            collect_callback(self.paself.output)
