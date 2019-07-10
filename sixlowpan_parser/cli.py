from .parser import *
import click
import logging

logging.basicConfig(level=logging.INFO)

def check_pcap_file_type(ctx, param, value):
    return value

@click.group()
def main():
    """
    main function of 6lowpan parser
    """
    return True

@main.command()
@click.option('-f', '--pcap-file', callback=check_pcap_file_type, type=str)
def parse(pcap_file):
    logging.info("input file is {}".format(pcap_file))
    parser = PCAPParser(pcap_file)
    parser.run()
