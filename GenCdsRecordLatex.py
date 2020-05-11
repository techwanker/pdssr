"""
Parse a CDS datafile and populate the ETL tables
"""

from pdssr.CdsReportingMetadata import CdsReportingMetadata
import pdsutil.field_metadata as field_metadata
import sys

# import logging
#
VERBOSE = False

line_nbr = 0


class GenCdsRecordLatex:
    def __init__(self):
        self.record_defs = CdsReportingMetadata().record_defs
        self.record_types = {
            "CD": self.record_defs["customer"],
            "CT": self.record_defs["customer_total"],
            "IR": self.record_defs["inventory"],
            "IT": self.record_defs["inventory_total"],
            "SA": self.record_defs["sales"],
            "AT": self.record_defs["sales_total"],
            #   "##": cds_reporting_fields.record_defs["comment"],
        }

        self.outfile = sys.stdout

    def emit(self, string):
        self.outfile.write(string)
        self.outfile.write("\n")

    def emit_table_header(self):

        self.emit("\begin{tabular}{p {5cm} | p {3cm} | c | p{6 cm}}")
        self.emit("Column Name & Data Type & Offset & Length & Format \\")
        self.emit("\hline")

    def emit_table_body(self, record_def):
        for field in record_def:
            # print field                   \\
            self.emit("%s & %s & %s & %s & %s \\\\" %
                      (field["field_name"], field["field_type"],
                       field["offset"], field["length"], field["str_format"]))

    def generate_latex(self):
        print(self.record_defs)
        for record_name, record_def in self.record_defs.iteritems():
            # self.emit_table_header()
            print(record_def)
            print("record def type %s" % type(record_def))
            # for field in record_def.itervalues:
            #     print field
            self.emit_table_body(record_def)


if __name__ == "__main__":
    genner = GenCdsRecordLatex()
    genner.generate_latex()
