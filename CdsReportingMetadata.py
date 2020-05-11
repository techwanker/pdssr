import json
import os
import yaml



class CdsReportingMetadata:
    """
    Reads a yaml file, loads it and retains a dict reference with key literals
    """
    record_defs = {}
    # Constants for code completion
    FIELD_NAME = "field_name"
    FIELD_TYPE = "field_type"
    PARSE_FORMAT = "parse_format"
    STR_FORMAT = "str_format"
    LITERAL    = "literal"
    LENGTH = "length"
    OFFSET = "offset"

    def __init__(self):
        """

        """
        fdir = os.path.dirname(os.path.realpath(__file__))
        meta_file = os.path.join(fdir, 'config/cds_reporting_metadata.yaml')

        with open(meta_file, 'r') as content_file:
            yaml_rules = content_file.read()

        self.record_defs = yaml.load(yaml_rules)
