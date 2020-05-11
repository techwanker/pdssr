import logging

import os
from pdsutil.DbUtil import ConnectionHelper
from pdsutil.Dexterity import StatementRunner, StatementHelper, CursorHelper
import yaml


def get_file_path(file_name):
    fdir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(fdir, file_name)

class Post:
    """
    Populates post_sale record from qualifying etl_sale records
    
    Updates the etl_sale.product_id based on case_gtin
    
    Upserts product_nomen with distributor identifier for authoritative manufacturer information
    """

    def __init__(self, conn):
        """

        :param conn: database connection
        """

        self.logger = logging.getLogger("__name__")
        self.connection = conn
        yaml_file = (get_file_path("config/post_dml.yaml"))
        with open(yaml_file, 'r') as content_file:
            yaml_statements = content_file.read()
        self.statements = yaml.load(yaml_statements)
        self.logger.warn("loading %s" % yaml_file)
        print (self.statements)

    def process(self, etl_file_id):
        """

        :param etl_file_id - int the file
        :return:
        """
        #assert (etl_file_id, int)
        self.logger.info("processing etl_file_id %s " % etl_file_id)
        binds = {"ETL_FILE_ID": etl_file_id}

        cursor = CursorHelper(self.connection.cursor())
        print (self.statements)
        ss = self.statements["etl_sale_update"]
        sql = ss["sql"]
        cursor.execute(sql,binds)



def post_customers(etl_file_id:int) -> None:
    """
    insert into 
    :param etl_file_id: 
    :return: 
    """

# TODO check if there are Conditions that disallow posting,
# this should be done in prepost
# TODO check if org is wrong for product
def process(etl_file_id):
    myconn = ConnectionHelper().get_named_connection("current")
    Post(myconn).process(etl_file_id)


def process_all():
    myconn = ConnectionHelper().get_named_connection("current")
    cursor = myconn.cursor()
    cursor.execute("select etl_file_id from etl_file order by etl_file_id")
    for row in cursor:
        etl_file_id = row[0]
        logging.info("about to process %s", etl_file_id)
        process(etl_file_id)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='prepost a load a file')
    # parser.add_argument('--etl_file_id', dest='etl_file_id', required=True)

    # args = parser.parse_args()
    # process(201723)
    pass
