#!/usr/bin/env python
import logging
import os

import yaml

from pdsutil.ConditionIdentification import ConditionIdentification
from pdsutil.DbUtil import ConnectionHelper, CursorHelper
from typing import Dict


class CdsDataloadConditions:
    """
    Invokes ConditionIdentification for an ETL load
    """

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        yaml_file_name = 'config/CdsDataloadConditions.yaml'
        yaml_dir = os.path.dirname(os.path.realpath(__file__))
        rules_file = os.path.join(yaml_dir, yaml_file_name)
        with open(rules_file, 'r') as content_file:
            yaml_rules = content_file.read()
        self.rules = yaml.load(yaml_rules)

    def process(self, conn, binds: Dict[str, object], rerun: bool = False, verbose=False) -> None:
        """

        :param conn:
        :param binds: etl_file_id numeric
        :param rerun: if True, deletes all the other runs
             
        :return:
        """

        self.logger.info("Connection is " + str(conn))
        self.logger.info("Rerun %s" % rerun)
        assert len(binds) == 1
        etl_file_id = binds["ETL_FILE_ID"]
        assert isinstance(etl_file_id, int)
        # if rerun:
        #     self.delete_run(conn, binds)

        sql = "select count(*) from etl_file where etl_file_id = %(ETL_FILE_ID)s"

        cursor = CursorHelper(conn.cursor())
        row_count = None
        rows = cursor.execute(sql, binds)
        for row in rows:
            row_count = row[0]
        if row_count == 0:
            raise Exception("No such etl_file_id %s" % etl_file_id)

        processor = ConditionIdentification(conn, self.rules)
        processor.process(binds, verbosity=3)

def main():
    #
    # parser = argparse.ArgumentParser(description='load a file')
    # parser.add_argument('--etl_file_id', dest='etl_file_id', required=True)
    # parser.add_argument('--rerun', action='store_true')
    # parser.set_defaults(rerun=False)
    #
    # args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    myconn = ConnectionHelper(None).get_named_connection("test")
    CdsDataloadConditions().process(myconn, {"ETL_FILE_ID": 20})  # TODO add args


if __name__ == "__main__":  # TODO add argument process
    main()