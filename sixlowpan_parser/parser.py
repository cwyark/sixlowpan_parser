from scapy.all import *
import logging

class PCAPParser:
    def __init__(self, pcap_path):
        conf.dot15d4_protocol = "sixlowpan"
        self.pcap_path = pcap_path
        self.result = dict()
        try:
            self.packets = rdpcap(self.pcap_path)
        except Scapy_Exception as e:
            logging.info("not a valid pcap file")
        except FileNotFoundError as e:
            logging.info("file not found")

    def run(self):
        for packet in packets:
            if packet.has_layer()
