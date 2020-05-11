#!/usr/bin/python3


import argparse
import csv
import logging

from pdssr.CdsFileReader import CdsFileReader

logging.basicConfig(level=logging.INFO)  # TODO use configuration file
logger = logging.getLogger(__name__)
import datetime




def get_writer(open_file):
    return csv.writer(open_file, dialect="excel",
                      delimiter=',', quotechar='"',
                      quoting=csv.QUOTE_NONNUMERIC)


class CdsDataloadToCSV:
    def __init__(self, input_file_name, output_dir, skip_literals=True, verbose:bool=False):
        self.reader = CdsFileReader(input_file_name)

        self.input_file_name = input_file_name
        self.output_dir = output_dir
        self.skip_literals = skip_literals

        self.customer_csv_name = output_dir + "/customer.csv"
        self.customer_csv = open(self.customer_csv_name, 'w')
        self.customer_writer = get_writer(self.customer_csv)
        self.customer_count = 0
        self.customer_record_def = self.reader.record_defs["customer"]

        self.sales_csv_name = output_dir + "/sales.csv"
        self.sales_csv = open(self.sales_csv_name, "w")
        self.sales_writer = get_writer(self.sales_csv)
        self.sales_count = 0
        self.sales_record_def = self.reader.record_defs["sales"]

        self.inventory_csv_name = output_dir + "/inventory.csv"
        self.inventory_csv = open(self.inventory_csv_name, "w")
        self.inventory_writer = get_writer(self.inventory_csv)
        self.inventory_count = 0
        self.inventory_record_def = self.reader.record_defs["inventory"]
        self.date_format = "%m/%d/%Y"
        self.verbose = verbose
        if verbose:
            logger.info("writing to %s %s %s" %
                    (self.inventory_csv_name, self.customer_csv_name, self.sales_csv_name))

    def emit_header(self, record_def, writer):
        headers = []
        for col_meta in record_def:
            if self.verbose:
                logger.info("skip_literals %s field_type %s" %
                        (self.skip_literals, col_meta["field_type"]))
            if not (self.skip_literals and col_meta["field_type"] == "LITERAL"):
                headers.append(col_meta["field_name"])
        logger.debug("writing headers %s " % headers)
        writer.writerow(headers)

    def format_date(self,obj):
        return obj.strftime(self.date_format)


    def process(self, verbose:bool=True) -> None:
        """
        Unload the file to CSV format
        :param verbose: 
        :return: Noan
        """
        try:
            for line_nbr, record_type, record, list in self.reader.read_line_as_obj_list(skip_literals=self.skip_literals):
                # print "Info: " + str(line_nbr) + " " +  record_type + " "  + record + "\n" + str(list)
                converted_list = []
                for datum in list:
                    logger.debug("datum %s type %s" % (datum, type(datum)))
                    if type(datum) is datetime.datetime:
                        datum = self.format_date(datum)
                        logger.debug("datum is now %s" % datum)
                    converted_list.append(datum)
                if record_type == 'SA':
                    if self.sales_count == 0:
                        self.emit_header(self.sales_record_def, self.sales_writer)
                    self.sales_writer.writerow(converted_list)
                    self.sales_count += 1
                elif record_type == 'IR':
                    if self.inventory_count == 0:
                        self.emit_header(self.inventory_record_def, self.inventory_writer)
                    self.inventory_writer.writerow(converted_list)
                    self.inventory_count += 1
                elif record_type == "CD":
                    if self.customer_count == 0:
                        self.emit_header(self.customer_record_def, self.customer_writer)
                    self.customer_writer.writerow(converted_list)
                    self.customer_count += 1
        finally:
            self.inventory_csv.close()
            self.customer_csv.close()
            self.sales_csv.close()
            if verbose:
                logger.info("Sales %s Customers %s Inventory %s" %
                            (self.sales_count, self.customer_count, self.inventory_count))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_directory", required=False, default=".",
                        help="output directory")
    parser.add_argument("--infile_name", required=True, help="input file")
    args = parser.parse_args()
    splitter = CdsDataloadToCSV(args.infile_name, args.output_directory)
    splitter.process()

if __name__ == "__main__":
    main()

