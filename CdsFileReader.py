"""
Parse a CDS datafile and populate the ETL tables
"""

import logging
from typing import Dict, List

import pdsutil.field_metadata as field_metadata
from pdssr.CdsReportingMetadata import CdsReportingMetadata

#
VERBOSE = False

# line_nbr = 0

logger = logging.getLogger(__name__)


class CdsFileReader:
    def __init__(self, filename):
        self.filename = filename
        self.infile = open(self.filename)
        self.file_open = True
        self.line_nbr = 0
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

    @staticmethod
    def get_binds(field_defs, inrec, record_number) -> Dict[str, object]:
        binds = {}

        for field_def in field_defs:
            try:
                binds[field_def["field_name"]] = field_metadata.get_field_obj(field_def, inrec)
            except Exception as e:
                text = "While processing record {}\n {}\n {}\n {}\n". \
                    format(record_number, inrec, field_def, e)
                raise Exception(text)
        return binds

    @staticmethod
    def get_field_obj_list(field_defs: Dict[str, str], inrec: str, record_number: int, skip_literals: bool):
        """
        Returns the fields a list of objects in order of occurence
        :param field_defs: 
        :param inrec: a cds reporting format string of one of the six record types
        :param record_number: 
        :param skip_literals:  True - don't emit invariant data
        :return: 
        """

        fields = []

        for field_def in field_defs:
            if not (skip_literals and field_def["field_type"] == "LITERAL"):
                try:
                    fields.append(field_metadata.get_field_obj(field_def, inrec))
                except Exception as e:
                    text = "While processing record %s\n %s\n %s\n %s\n" % \
                           (record_number, inrec, field_def, e)
                    raise Exception(text)
        return fields

    def read_line_as_obj_list(self, skip_literals=False) -> (int, str, List[object]):
        return self._read_line(False, skip_literals=skip_literals)

    def read_line(self) -> (int, str, Dict[str, object]):
        return self._read_line(True)

    def _read_line(self, as_dict: bool, skip_literals: bool = True) -> (int, str, Dict[str, object]):
        for line in self.infile:
            self.line_nbr += 1
            if line[0] == "#":
                continue
            record_type = line[168:170]
            if not record_type in self.record_types:
                raise Exception("on line %s unknown record type '%s'" % (self.line_nbr, record_type))
            field_defs = self.record_types[record_type]
            if as_dict:
                binds = self.get_binds(field_defs, line, self.line_nbr)
                yield self.line_nbr, record_type, line, binds
            else:
                field_defs = self.record_types[record_type]
                fields = self.get_field_obj_list(field_defs, line, self.line_nbr, skip_literals)
                yield self.line_nbr, record_type, line, fields

    def close(self):
        self.infile.close()
