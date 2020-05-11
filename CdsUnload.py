from pdsutil.DbUtil import ConnectionHelper, CursorHelper
import pdsutil.field_metadata as field_metadata
from pdssr.CdsReportingMetadata import CdsReportingMetadata
import logging
from typing import Dict, Union
import datetime


class CdsUnload:
    """
    Extracts the data from the following tables:
       etl_customer
       etl_customer_tot
       etl_sale
       etl_sale_tot
       etl_inventory
       etl_inventory_tot

       The records are retrieved by the original order and the output file should be
       identical to the input file.

       Extracting without preserving line number order is 3 to 4 times as fast.
    """

    def __init__(self, connection, calc_totals: bool = False):
        """
        
        :param connection: 
        :param calc_totals: 
        """

        # """
        # Creates a CDS load format file
        #
        # :param connection:
        # :param file_name:
        # :param etl_file_id:
        # :param by_line_number boolean
        #        True emit in the original sequence from which this was loaded
        #        False emit customers, customer_total, sales, sales_total, inventory, inventory_total
        # :param calc_totals - True - compute from the associated records False - emit what is stored in the tables
        #
        # """

        self.connection = connection
        print ("connection %s " % connection)
        self.record_defs = CdsReportingMetadata().record_defs
        #

        self.logger = logging.getLogger(__name__)
        # cursors
        self.line_number_cursor = None
        self.customer_cursor = None
        self.customer_total_cursor = None
        self.inventory_cursor = None
        self.inventory_total_cursor = None
        self.sale_cursor = None
        self.sale_total_cursor = None

        #
        self.customer_column_names = None
        self.customer_total_column_names = None
        self.sale_column_names = None
        self.sale_total_column_names = None
        self.inventory_column_names = None
        self.inventory_total_column_names = None

        self.outfile = None  # An open file to be written to

    def get_line_numbers(self, etl_file_id: int):
        """
        retrieve all the records in the load from the origina
        :param etl_file_id:

        :return:
        """

        if self.line_number_cursor is None:
            self.line_number_cursor = CursorHelper(self.connection.cursor())
        rows = self.line_number_cursor.execute("""
        select table_name, id, line_number
        from
        (
        select 'etl_customer' table_name, etl_customer_id id, line_number
        from etl_customer
        where etl_file_id = %(ETL_FILE_ID)s
        union
        select 'etl_sale', etl_sale_Id, line_number
        from etl_sale
        where etl_file_id = %(ETL_FILE_ID)s
        union
        select 'etl_inventory', etl_inventory_id, line_number
        from etl_inventory
        where etl_file_id = %(ETL_FILE_ID)s
        union
        select 'etl_inventory_tot', etl_file_id, line_number
        from etl_inventory_tot
        where etl_file_id = %(ETL_FILE_ID)s
        union
        select 'etl_customer_tot', etl_file_id, line_number
        from etl_customer_tot
        where etl_file_id = %(ETL_FILE_ID)s
        )  as by_line_number
        order by line_number
        """,
                                               {"ETL_FILE_ID": etl_file_id})
        return rows

    def emit(self, string: str) -> None:
        """
        writes the string to outfile
        :param string:

        :return:
        """
        REQUIRED_LEN = 170
        if len(string) != REQUIRED_LEN:
            raise Exception("required len %s actual %s\n%s" % (REQUIRED_LEN, len(string), string))
        self.outfile.write(string)
        self.outfile.write("\n")
        # print(string)

    def emit_sale(self, data_map: Dict[str, object]):
        # Union(str, int, datetime.datetime)]):
        """
        Defines filler bind variables not return from the database and
        converts Decimal values to int where appropriate so that int formats will work
        The writes to the output file

        :param data_map: Bind parameters

        :return:
        """

        data_map["FILLER_12"] = "            "
        data_map["FILLER"] = "         "
        data_map["RECORD_TYPE"] = "SA"
        data_map["EXTENDED_NET_AMT"] = int(data_map["EXTENDED_NET_AMT"] * 100)
        data_map["CASES_SHIPPED"] = int(data_map["CASES_SHIPPED"])
        data_map["BOXES_SHIPPED"] = int(data_map["BOXES_SHIPPED"])
        data_map["UNITS_SHIPPED"] = int(data_map["UNITS_SHIPPED"])

        record = field_metadata.format_line(self.record_defs["sales"], data_map)
        try:
            self.emit(record)
        except Exception as e:
            msg = ("binds %s\n, record: %s exception: %s" % (data_map, record, e))

    def unload_sale(self, id, by_etl_sale_id=True):
        if self.sale_cursor is None:
            self.sale_cursor = CursorHelper(self.connection.cursor())

        if by_etl_sale_id:
            sql = "select * from etl_sale where etl_sale_id = %(ETL_SALE_ID)s"
            rows = self.sale_cursor.execute(sql, {"ETL_SALE_ID": id})
        else:
            sql = "select * from etl_sale where etl_file_id = %(ETL_FILE_ID)s"
            rows = self.sale_cursor.execute(sql, {"ETL_FILE_ID": id})

        if self.sale_column_names is None:
            self.sale_column_names = [i[0].upper() for i in self.sale_cursor.description]
            # print ("cursor columns: %s" % self.sale_column_names) #TODO
        for row in rows:
            data_map = dict(zip(self.sale_column_names, row))
            self.emit_sale(data_map)

    def emit_inventory(self, data_map: Dict[str, object]) -> None:
        # Union(str, int, datetime.datetime)]) -> None:
        data_map["RECORD_TYPE"] = "IT"
        data_map["CASES"] = int(data_map["CASES"])
        data_map["BOXES"] = int(data_map["BOXES"])
        data_map["UNITS"] = int(data_map["UNITS"])
        data_map["FILLER"] = " "
        if data_map["CASE_GTIN"] is None:
            data_map["CASE_GTIN"] = "000000000000000"
        outrec = field_metadata.format_line(self.record_defs["inventory"], data_map)
        try:
            self.emit(outrec)
        except Exception as e:
            msg = "binds: %s\n outrec: %s %s" % (data_map, outrec, e)
            raise Exception(msg)

    def unload_inventory(self, id: int, by_etl_inventory_id: bool = True) -> None:
        """
        :param id: int - if by_etl_inventory_id is True, then etl_inventory_id else etl_file_id
        :param by_etl_inventory_id: True - unload one record False - unload all records

        :return:

        """

        if self.inventory_cursor is None:
            self.inventory_cursor = CursorHelper(self.connection.cursor())
        sql = None
        if (by_etl_inventory_id):
            sql = "select * from etl_inventory where etl_inventory_id = %(ETL_INVENTORY_ID)s"
            rows = self.inventory_cursor.execute(sql, {"ETL_INVENTORY_ID": id})
        else:
            sql = "select * from etl_inventory where etl_file_id = %(ETL_FILE_ID)s"
            rows = self.inventory_cursor.execute(sql, {"ETL_FILE_ID": id})

        if self.inventory_column_names is None:
            self.inventory_column_names = [i[0].upper() for i in self.inventory_cursor.description]

        for row in rows:
            data_map = dict(zip(self.inventory_column_names, row))
            self.emit_inventory(data_map)

    def unload_customer_total(self, etl_file_id: int, compute: bool = False) -> None:
        """
        Unload Customer Total
        :param etl_file_id:
        :param compute: True - compute from etl_customer records False - extract only if the record exists

        :return: None
        """

        if self.customer_total_cursor is None:
            self.customer_total_cursor = CursorHelper(self.connection.cursor())
        sql = "select * from etl_customer_tot where etl_file_id = %(ETL_FILE_ID)s"
        rows = self.customer_total_cursor.execute(sql, {"ETL_FILE_ID": etl_file_id})
        if self.customer_total_column_names is None:
            self.customer_total_column_names = [i[0].upper() for i in self.customer_total_cursor.description]
            # print ("cursor columns: %s" % self.customer_column_names)
        for row in rows:
            data_map = dict(zip(self.customer_total_column_names, row))
            data_map["HEADER"] = "9999999999"
            data_map["RECORD_TYPE"] = "CT"
            data_map["FILLER_127"] = "".ljust(127)
            data_map["CUSTOMER_COUNT"] = int(data_map["CUSTOMER_COUNT"])
            data_map["FILLER_22"] = "".ljust(22)
            outrec = field_metadata.format_line(self.record_defs["customer_total"], data_map)
            self.emit(outrec)

    def unload_sale_tot(self, etl_file_id: int, compute: bool = False) -> None:
        """
        fetch etl_inventory
        :param etl_file_id: the primary key of etl_file being unloaded
        :param compute: True - compute from actual values False - extract only if record exists

        :return: None
        """

        # TODO Compute
        if self.sale_total_cursor is None:
            self.sale_total_cursor = CursorHelper(self.connection.cursor())
        sql = "select * from etl_sale_tot where etl_file_id = %(ETL_FILE_ID)s"
        rows = self.sale_total_cursor.execute(sql, {"ETL_FILE_ID": etl_file_id})
        if self.sale_total_column_names is None:
            self.sale_total_column_names = [i[0].upper() for i in self.sale_total_cursor.description]
        for row in rows:
            data_map = dict(zip(self.sale_total_column_names, row))
            data_map["HEADER"] = "9999999999"
            data_map["FILLER_28"] = "".ljust(28)
            data_map["SALES_REC_CNT"] = int(data_map["SALES_REC_CNT"])
            data_map["SUM_EXT_NET_AMT"] = int(data_map["SUM_EXT_NET_AMT"]) * 100
            data_map["FILLER_86"] = "".ljust(86)
            data_map["RECORD_TYPE"] = "ST"
            outrec = field_metadata.format_line(self.record_defs["sales_total"], data_map)
            self.emit(outrec)

    def unload_inventory_tot(self, etl_file_id: int, compute: bool = False) -> None:

        """
        Unload Customer Total
        :param etl_file_id:
        :param compute: boolean True -compute the totals rather than extract False - extract if exist else ignore
            
        :return: None
            
        """
        logger = logging.getLogger("unload_inventory_tot")
        logger.setLevel(logging.DEBUG)
        if self.inventory_total_cursor is None:
            self.inventory_total_cursor = CursorHelper(self.connection.cursor())
        sql = "select * from etl_inventory_tot where etl_file_id = %(ETL_FILE_ID)s"
        rows = self.inventory_total_cursor.execute(sql, {"ETL_FILE_ID": etl_file_id})
        if self.inventory_total_column_names is None:
            self.inventory_total_column_names = [i[0].upper() for i in self.inventory_total_cursor.description]
        for row in rows:
            data_map = dict(zip(self.inventory_total_column_names, row))
            for k, v in data_map.items():
                print("inventory_tot k %s v %s type(v) %s" % (k, v, type(v)))
            data_map["HEADER"] = "9999999999"
            data_map["FILLER36"] = "".ljust(36)
            data_map["RECORD_TYPE"] = "IT"
            data_map["RECORD_CNT_REPORTED"] = int(data_map["RECORD_CNT_REPORTED"])
            data_map["FILLER97"] = "".ljust(97)

            logger.debug("record definition %s" % self.record_defs["inventory_total"])
            logger.debug("data_map = %s" % data_map)
            outrec = field_metadata.format_line(self.record_defs["inventory_total"], data_map, trace=True)
            self.emit(outrec)

    def emit_customer(self, data_map):
        data_map["FILLER_00_05"] = "     "  # TODO should work in FieldMeta and not be required
        data_map["CLASS_OF_TRADE"] = "    "
        data_map["FILLER_1"] = " "
        data_map["RECORD_TYPE"] = "SA"
        outrec = field_metadata.format_line(self.record_defs["customer"], data_map)
        self.emit(outrec)

    def unload_customer(self, id: int, by_etl_customer_id: bool) -> None:
        if self.customer_cursor is None:
            self.customer_cursor = CursorHelper(self.connection.cursor())
        if by_etl_customer_id:
            sql = "select * from etl_customer where etl_customer_id = %(ETL_CUSTOMER_ID)s"
            rows = self.customer_cursor.execute(sql, {"ETL_CUSTOMER_ID": id})
        else:
            sql = "select * from etl_customer where etl_file_id = %(ETL_FILE_ID)s"
            rows = self.customer_cursor.execute(sql, {"ETL_FILE_ID": id})
        if self.customer_column_names is None:
            self.customer_column_names = [i[0].upper() for i in self.customer_cursor.description]
            # print ("cursor columns: %s" % self.customer_column_names)
        for row in rows:
            data_map = dict(zip(self.customer_column_names, row))
            self.emit_customer(data_map)

    def process_by_line_number(self, etl_file_id: int, file_name: str) -> None:
        self.outfile = open(file_name, "w")  # TODO use using
        for table_name, id, line_number in self.get_line_numbers(etl_file_id):
            # print ("table_name %s id: %s line_number: %s" % (table_name, id, line_number))
            if table_name == 'etl_customer':
                self.unload_customer(id, True)
            elif table_name == "etl_sale":
                self.unload_sale(id, True)
            elif table_name == "etl_inventory":
                self.unload_inventory(id, True)
            elif table_name == "etl_customer_tot":
                self.unload_customer_total(etl_file_id)
            elif table_name == "etl_inventory_tot":
                self.unload_inventory_tot(etl_file_id)
            elif table_name == "etl_sale_tot":
                self.unload_sale_tot(etl_file_id)
            else:
                raise Exception("unsupported record %s" % table_name)
        self.outfile.close()

    def process_by_table(self, etl_file_id: int, file_name: str) -> None:
        self.outfile = open(file_name, "w")  # TODO use using

        self.unload_customer(etl_file_id, False)
        self.unload_sale(etl_file_id, False)
        self.unload_inventory(etl_file_id, False)
        self.unload_customer_total(etl_file_id, False)
        self.unload_inventory_tot(etl_file_id, False)
        self.unload_sale_tot(etl_file_id, False)
        self.outfile.close()

    def process(self, etl_file_id: int, file_name: str, by_line_number: bool) -> None:

        """

        :param etl_file_id: the etl_file.etl_file_id to extract
        :param file_name: output file name
        :param by_line_number: boolean - much slower but records in original order

        :return: None
        """

        if by_line_number:
            self.process_by_line_number(etl_file_id, file_name)
        else:
            self.process_by_table(etl_file_id, file_name)

    def unload_all(self):

        cursor = CursorHelper(self.connection.cursor())
        sql = "select etl_file_id from etl_file"
        rows = cursor.execute(sql)

        for row in rows:
            etl_file_id = row[0]
        #    self.process(etl_file_id, "../pdssr_testdata/%s.cds" % etl_file_id, False)
            self.process(etl_file_id, "/tmp/python/%s.cds" % etl_file_id, False)


if __name__ == "__main__":
     myconn = ConnectionHelper().get_named_connection("it")
     unloader = CdsUnload(myconn)
     #unloader.process(30, "/tmp/201502.cds", False)  # TODO
     unloader.unload_all()
