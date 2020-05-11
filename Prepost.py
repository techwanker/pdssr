import pdsutil.DbUtil as Dbutil
from pdsutil.DbUtil import SqlStatements, ConnectionHelper, CursorHelper
import datetime
import psycopg2
import yaml
import os
import logging
from collections import namedtuple


logger = logging.getLogger(__name__)

class Prepost:
    """
    Pre-post
    
      * Attempt to identify the product_id based on 
    
    """

    def __init__(self, connection):

        self.connection = connection
        self.cursor = CursorHelper(connection.cursor())
        self.binds = {}

        fdir = os.path.dirname(os.path.realpath(__file__))
        logger.debug("fdir %s" % fdir)
        meta_file = os.path.join(fdir, 'config/post_dml.yaml')
        logger.debug("using meta_file %s" % meta_file)
        self.statements = SqlStatements.from_yaml(meta_file).statements

    def process(self,etl_file_id:int):
        self.binds = {"ETL_FILE_ID" : etl_file_id}
        self.update_etl_sale_by_gtin()
        self.product_nomen_insert()
        effective_date = self.get_max_effective_date()
        self.binds["EFFECTIVE_DATE"] =  effective_date
        self.vp_distributor_customer_insert()

        self.connection.commit()

    def run_statement(self,statement_name):
        stmt = self.statements[statement_name]
        rows = self.cursor.execute(stmt['sql'], self.binds)
        for row in rows:
            count = row[0];
        logger.debug("%s updated %s" % (statement_name, count))

    def run_query(self,statement_name):
        stmt = self.statements[statement_name]
        rows = self.cursor.execute(stmt['sql'], self.binds)
        nt = namedtuple(statement_name, [i[0] for i in self.cursor.description])
        rows = []
        for row in map(nt._make, self.cursor.fetchall()):
            print(row)
            rows.append(row)
        return rows


    def update_etl_sale_by_gtin(self):
        self.run_statement("etl_sale_update")

    def product_nomen_insert(self):
        self.run_statement("product_nomen_insert")

    def get_max_effective_date(self):
        rows = self.run_query("effective_date_select")
        row = rows[0]
        print (row)
        return rows[0].max_invoice_dt

    def vp_distributor_customer_insert(self):
        self.run_statement("vp_distributor_customer_insert")



if __name__ ==  "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    conn = ConnectionHelper().get_named_connection("it")
    prepost = Prepost(conn)
    prepost.process(1)
