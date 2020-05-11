import sqlite3
from pdsutil.DbUtil import ConnectionHelper, CursorHelper
from pdsutil.SqlRunner import SqlRunner as SqlRunner
from pdssr.CdsDataloader import CdsDataloader
from pdssr.CdsReportingMetadata import CdsReportingMetadata
from pdssr.SeedSalesReportingDatabase import SeedSalesReportingDatabase
from pdssr.CdsDataloadConditions import CdsDataloadConditions
from pdssr.CdsUnload import CdsUnload
import pdsutil.dialects as  dialects
import unittest
import logging
import os

import tempfile


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILE_LIMIT = None


#DIALECT=dialects.DIALECT_SQLITE
DIALECT=dialects.DIALECT_POSTGRES

def get_file_path(file_name: str) -> str:
    fdir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(fdir, file_name)


class IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ get_some_resource() is slow, to avoid calling it for each test use setUpClass()
            and store the result as class variable
        """
        super(IntegrationTest, cls).setUpClass()
        cls.tname = None

        if DIALECT == dialects.DIALECT_SQLITE:
            cls.connection = cls.get_sqlite_connection()
        elif DIALECT == dialects.DIALECT_POSTGRES:
            cls.connection = cls.get_postgres_connection()
        else:
            raise Exception("unsupported dialect '%s'" % DIALECT)

        runner = SqlRunner(get_file_path("../config/ut_condition_tables.sr.sql"), cls.connection)
        runner.process()

        if DIALECT == dialects.DIALECT_SQLITE:
            runner = SqlRunner(get_file_path("../config/sales_reporting_ddl_sqlite.sql"), cls.connection)
        elif DIALECT == dialects.DIALECT_POSTGRES:
            runner = SqlRunner(get_file_path("../config/sales_reporting_ddl.sql"), cls.connection)
        else:
            raise Exception("unsupported dialect '%s'" % DIALECT)

        runner.process()

        SeedSalesReportingDatabase(cls.connection).process()



    @classmethod
    def get_sqlite_connection(cls):
        tfile = tempfile.NamedTemporaryFile(suffix='.dbf', dir="/tmp", delete=False)
        cls.tname = tfile.name
        tfile.close()
        logger.info("-------")
        logging.info("creating database %s" % cls.tname)

        cls.connection = sqlite3.Connection(cls.tname, detect_types = sqlite3.PARSE_DECLTYPES )
        return cls.connection


    @classmethod
    def get_postgres_connection(cls):  # TODO externalize use - test schema to initialize
        db_url = "postgres:host='localhost' dbname='sales_reporting' user='jjs' password='jjs'"  # TODO externalize
        cls.connection =  ConnectionHelper.get_connection(db_url)
        cursor = cls.connection.cursor()
        schema = "integration_test"
        cursor.execute("create schema %s" % schema)
        cursor.execute("set schema '%s'" % schema)
        return cls.connection






    def load_all(cls):
        import glob
        path = get_file_path("../../pdssr_testdata")

        loader = CdsDataloader()
        file_count = 0
        for file in sorted(glob.glob(path + "/*.cds")):
            logging.info("loading file: %s" % file)
            loader.process(file, cls.connection, "EXOTICTX", False)
            cls.connection.commit()
            file_count += 1
            if FILE_LIMIT is not None and file_count >= FILE_LIMIT:
                break
        cls.connection.commit()


    def conditions(cls):
        logger.info("running conditions")
        processor = CdsDataloadConditions()
        file_id_sql = "select etl_file_id from etl_file"
        cursor = CursorHelper(cls.connection.cursor())

        rows = cursor.execute(file_id_sql)
        for row in rows:
            etl_file_id = row[0]
            binds = {"ETL_FILE_ID" : etl_file_id}
            logger.info("conditions for %s" % etl_file_id)
            processor.process(cls.connection,binds=binds)
        cursor.close()

    def unload_all(cls):
        sql = "select etl_file_id from etl_file"

        cursor = CursorHelper(cls.connection.cursor())

        rows = cursor.execute(sql)

        for row in rows:
            unloader = CdsUnload(cls.connection)
            etl_file_id = row[0]
            unloader.process(etl_file_id, "/tmp/%s.cds" % etl_file_id, False)

    def check_customers(cls):
        sql = "select etl_file_id, count(*)from etl_file where etl_file_id = %(ETL_FILE_ID)s group by etl_file_id"
        cursor = CursorHelper(cls.connection.cursor())
        binds = {"ETL_FILE_ID" : 1}
        rows = cursor.execute(sql, binds)
        count = 0
        for row in rows:
            row_count = row[1]
            count += row_count
            print("etl_customer count: %s %s" % (row[0],row_count))
        assert(count > 1)



    def test_all(cls):
        cls.load_all()
        cls.conditions()
        #prepost
        #post
        #worksheets
        #metrics
        #ToCsv
        cls.unload_all()
        #cls.check_customers()


    def tearDown(cls):
        cls.connection.commit()
        cls.connection.close()
        if cls.tname is not None:
            logging.info("created database %s" % cls.tname)

if __name__ == '__main__':
    unittest.main()
