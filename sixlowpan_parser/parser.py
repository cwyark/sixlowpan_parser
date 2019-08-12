from scapy.all import *
import logging
from .model import *

class Parser:
    def __init__(self, _input):
        conf.dot15d4_protocol = 'sixlowpan'
        self.logger = logging.getLogger(__name__)
        self.input = _input

class PCAPParser(Parser):
    def __init__(self, _input):
        super(PCAPParser, self).__init__(_input)
        try:
            self.logger.info("extracting packets from pcap file, please wait, it might take a moments")
            self.packets = rdpcap(_input)
        except Scapy_Exception as e:
            self.logger.info("not a valid pcap file")
        except FileNotFoundError as e:
            self.logger.info("file not found")
        self.pcap_total_packets = len(self.packets)
        self.logger.info("Found {} packets in pcap file".format(self.pcap_total_packets))

    def parse(self, aggregation = 10):
        """
        parse will return a generator
        """
        counter = 0
        agmodel = AggregationModel()
        for packet in self.packets:
            if packet.haslayer(UDP):
                payload = packet.getlayer(UDP).payload.load
                model = UDPModel(payload)
                agmodel.updateUDPModel(model)
            if packet.haslayer(Dot15d4FCS):
                if packet.haslayer(LoWPANUncompressedIPv6):
                    agmodel.updateNumOfDIS()
                if packet.haslayer(LoWPAN_IPHC):
                    agmodel.updateNumOfDIO()
            counter += 1
            if counter == aggregation:
                yield agmodel
                agmodel.reset()
                counter = 0
