from scapy.all import *
import logging
from sixlowpan_parser.database import csv_collector
from .parser import *
from .model import *
import csv

class Runner:
    def __init__(self, data_input, data_output, window_size=10):
        self.logger = logging.getLogger(__name__)
        self.parser = PCAPParser(data_input)
        self.data_output = data_output
        self.window_size = window_size

    def run(self):
        with open(self.data_output, "w") as f:
            w = None
            for data in self.parser.parse(aggregation=window_size):
                self.logger.info(data.to_dict)
                if w is None:
                    csv_columns = list(data.to_dict.keys())
                    w = csv.DictWriter(f, fieldnames=csv_columns)
                    w.writeheader()
                w.writerow(data.to_dict)
