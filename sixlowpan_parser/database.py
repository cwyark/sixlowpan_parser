import logging
import csv

def csv_collector(input_list, output_path):
    logger = logging.getLogger("database.vcs")
    if type(input_list) is not list:
        logger.info("input is not a list, do nothing and return")
        return
    if type(output_path) is not str:
        logger.info("output_path is not a valid path, do nothing and return")
    csv_columns = list(input_list[0].keys())
    logger.info("keys are {}".format(csv_columns))
    with open(output_path, "w") as f:
        w = csv.DictWriter(f, fieldnames=csv_columns)
        w.writeheader()
        for item in input_list:
            w.writerow(item)
