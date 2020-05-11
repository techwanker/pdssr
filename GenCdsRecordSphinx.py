"""
Parse a CDS datafile and populate the ETL tables
"""

from pdssr.CdsReportingMetadata import CdsReportingMetadata
import pdsutil.field_metadata as field_metadata
import sys
import logging

VERBOSE = False

#line_nbr = 0

logger = logging.getLogger(__name__)

class GenCdsRecordSphinx:
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
        ruler = ("%s %s %s %s %s") % \
                ("".ljust(30,"="), "".ljust(8,"="), "".ljust(6,"="), "".ljust(6,"=") ,"".ljust(8,"="))
        self.emit("")
        self.emit(ruler)
        self.emit("%s %s %s %s %s" %
                  ("field_name".ljust(30),
                   "type".ljust(8),
                   "offset".ljust(6),
                   "length".ljust(6),
                    "format".ljust(6)
                   )
                  )
        self.emit(ruler)

        for field in record_def:
            # print field                   \\
            self.emit("%s %s %s %s %s" %
                      (field["field_name"].ljust(30),
                       field["field_type"].ljust(8),
                       str(field["fixed_offset"]).rjust(6),
                       str(field["fixed_length"]).rjust(6),
                       field["str_format"].ljust(6)
                       )
                      )
        self.emit(ruler)

    def process(self):
        logger.debug(self.record_defs)
        for record_name, record_def in self.record_defs.items():
            self.emit_table_body(record_def)


if __name__ == "__main__":
    genner = GenCdsRecordSphinx()
    genner.process()
