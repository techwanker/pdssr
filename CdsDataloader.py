#!/usr/bin/python

import argparse
import logging
import os
import time

from pdssr.CdsFileReader import CdsFileReader
from pdsutil.DbUtil import ConnectionHelper
from pdsutil.DbUtil import SqlStatements, Cursors


def get_file_path(file_name):
    fdir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(fdir, file_name)


class CdsDataloader:
    """
    Loads a CDS format file into ETL tables
    
    """

    def __init__(self):

        self.logger = logging.getLogger("__name__")
        yaml_file_name = get_file_path("config/etl_persistence_sql.yaml")
        self.statements = SqlStatements.from_yaml(yaml_file_name).statements
        self.cursors = None
        self.sql_statements = {
            "CD": self.statements["etl_customer_insert"],
            "CT": self.statements["etl_customer_tot_insert"],
            "IR": self.statements["etl_inventory_insert"],
            "IT": self.statements["etl_inventory_tot_insert"],
            "SA": self.statements["etl_sale_insert"],
            "AT": self.statements["etl_sale_tot_insert"],
        }


    def process(self, filename: str, conn, distributor_cd: str, validate: bool) -> None:
        """
            :param filename: name of CDS formatted data file
            :param conn: A database connection
            :param distributor_cd - The reporting organization, must be in org
            :param validate: True - run validations # TODO should
            
            :return:
            
        """
        start_time = time.time()
        self.cursors = Cursors(conn)

        reader = CdsFileReader(filename)
        # Initialize run
        file_id = self.initial_insert({"ORG_CD": distributor_cd})

        line_count = 0
        for line_nbr, record_type, record, binds in reader.read_line():
            binds["ETL_FILE_ID"] = file_id
            binds["LINE_NUMBER"] = line_nbr
            if "EXTENDED_NET_AMT" in binds:
                binds["EXTENDED_NET_AMT"] = binds["EXTENDED_NET_AMT"] / 100
            sql = self.sql_statements[record_type]["sql"]
            self.cursors.get_cursor(sql).execute(sql, binds)

            line_count += 1
        reader.close()
        conn.commit()
        self.cursors.close()
        elapsed_time = time.time() - start_time
        self.logger.info("loaded '%s' file id: %s record count %s in %s seconds" %
                         (filename, file_id, line_count, elapsed_time))

    def initial_insert(self, binds):
        logger = logging.getLogger(__name__ + ":initial_insert")
        etl_file_initial_insert = self.statements["etl_file_initial_insert"]["sql"]
        returning = self.statements["etl_file_initial_insert"]["returning"]

        org_sql = "select org_id from org where org_cd = %(ORG_CD)s"
        cursor = self.cursors.get_cursor(org_sql)
        rows = cursor.execute(org_sql, binds)
        row_found = False
        for row in rows:
            row_found = True
        if not row_found:
            raise Exception("no data found for " + str(binds) + " in " + org_sql)

        cursor = self.cursors.get_cursor(etl_file_initial_insert)
        etl_file_id = cursor.execute(etl_file_initial_insert, binds,
                                     returning=returning)

        logger.info("returning etl_file_id " + str(etl_file_id))
        return etl_file_id


def main():
    logging.basicConfig(level=logging.INFO)
    # parser = argparse.ArgumentParser(description='load a file')
    # parser.add_argument('--inputfile', dest='inputfile')
    # parser.add_argument("--connection", required=True)
    # parser.add_argument("--distributor")
    # parser.set_defaults(test=False)
    # args = parser.parse_args()
    #
    # mainconn = ConnectionHelper().get_named_connection(args.connections)
    # CdsDataloader().process(args.inputfile, mainconn, args.distributor, False)
    #
    # import sqlite3

    mainconn = ConnectionHelper().get_named_connection("it")
   # mainconn = sqlite3.Connection("/tmp/scratch.dbf")

    CdsDataloader().process("/tmp/customers.cds", mainconn, "EXOTICTX", False)
    # TODO get from arguments or env


if __name__ == '__main__':
    main()
