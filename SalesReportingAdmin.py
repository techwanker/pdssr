#!/usr/bin/env python

import logging

from pdsutil.DbUtil import ConnectionHelper



from pdsutil.SqlRunner import SqlRunner
import os


class SalesReportingAdmin:
    """
    Source of calls to other classes for use in web services and command line
    """

    def __init__(self, connection_name, logging_level=logging.INFO):
        """
        :param connection_name: the name of a database connection
        """
        self.connection_name = connection_name
        self.connection = ConnectionHelper().get_named_connection(self.connection_name)
        logging.basicConfig(level=logging_level)
        self.logger = logging.getLogger(__name__)

    def create_schema(self):
        """
        Creates the database objects, tables, views etc
        :return:
        """
        dir = os.path.dirname(os.path.realpath(__file__))
        runner_file = os.path.join(dir, 'config/sales_reporting_ddl.sql')
        runner = SqlRunner(runner_file,self.connection, continue_on_error=False)
        runner.process()
        self.logger.info("schema created")

    def seed_database(self):
        from pdssr.SeedSalesReportingDatabase import SeedSalesReportingDatabase
        """
        Initializes mandatory data
        :return:
        """
        SeedSalesReportingDatabase(self.connection).process()
        self.connection.commit()
        self.logger.info("seeding complete")

    def load_file(self, file_name, distributor_cd):

        """
        Loads a CDS format reporting file into ETL tables
        :param file_name: name of file in CDS reporting format to be loaded
        :param distributor_cd: an organizition identifier that is allowed to report
        :return:
        """
        from pdssr.CdsDataloader import CdsDataloader
        loader = CdsDataloader()
        loader.process(file_name, self.connection, distributor_cd, False)

    def initialize(self, connection_name):
        """
        Creates the database schema and populates with
        :param connection_name:
        :return:
        """
        admin = SalesReportingAdmin(connection_name)
        admin.create_schema()
        admin.seed_database()
        self.logger.info("initialization and seeding complete")

    def dataload_conditions(self, etl_file_id, rerun=False):
        from pdssr.CdsDataloadConditions import CdsDataloadConditions
        """
        Checks a load for data integrity and rational data
        :param etl_file_id int
        :param rerun (delete all previous run output and rerun
        :return:
        """
        assert isinstance(etl_file_id, int)


        processor = CdsDataloadConditions()
        processor.process(self.connection, {"ETL_FILE_ID": etl_file_id},rerun)
        #self.connection.commit()
        self.logger.info("dataload_conditions complete")

    def post(self, etl_file_id):
        """
        posts a file
        :param etl_file_id:
        :return:
        """
        from pdssr.Post import Post
        poster = Post(self.connection)
        poster.process(etl_file_id)
        self.connection.commit()
        self.logger.info("post of etl_file_id: %s is complete" % etl_file_id)

    def to_csv(self,input_file,output_dir):
        from pdssr.CdsDataloadToCSV import CdsDataloadToCSV
        splitter = CdsDataloadToCSV(input_file, output_dir)
        splitter.process()

    def unload(self, etl_file_id, file_name):
        """
        posts a file
        :param etl_file_id:
        :return:
        """
        from pdssr.CdsUnload import CdsUnload
        unloader = CdsUnload(self.connection)
        unloader.process(etl_file_id,file_name,by_line_number=True)
        self.connection.commit()
        self.logger.info("unload of etl_file_id: %s is complete" % etl_file_id)


    def web_services(self, port=8091):
        """
        provides json_rpc services services to website
        see RequestHandler
        :param port:
        :return:
        """
        import pyjsonrpc
        from pdssr.WebServices import WebServices
        http_server = pyjsonrpc.ThreadingHttpServer(
            server_address=('localhost', port),
            RequestHandlerClass=WebServices
        )
        self.logger.info("Starting HTTP server ...")
        self.logger("URL: http://localhost:%s" % port)  # TODO  get from settings
        http_server.serve_forever()
        self.logger.info("web services started")

