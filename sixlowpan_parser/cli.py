from .parser import *
import click
import logging

logging.basicConfig(level=logging.DEBUG)

def check_pcap_file_type(ctx, param, value):
    return value

@click.group()
def main():
    """
    main function of 6lowpan parser
    """
    return True

@main.command()
@click.option('-f', '--pcap-file', callback=check_pcap_file_type, required=True, type=str)
@click.option('-o', '--output',type=str, required=True)
def parse(pcap_file, output):
    logging.info("input file is {}".format(pcap_file))
    logging.info("output file is {}".format(output))
    parser = PCAPParser(pcap_file, output)
    parser.run()
