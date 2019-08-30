from .runner import *
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
@click.option('-i', '--data-input', callback=check_pcap_file_type, required=True, type=str)
@click.option('-o', '--output',type=str, required=True)
@click.option('-w', '--window-size', type=int, default=10)
def parse(data_input, output, window_size):
    logging.info("data input is {}".format(data_input))
    logging.info("output file is {}".format(output))
    runner = Runner(data_input, output, window_size)
    runner.run()
