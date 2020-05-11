#!/usr/bin/env python
import unittest
import datetime
from pdssr.CdsReportingMetadata import CdsReportingMetadata
import pdsutil.field_metadata as field_metadata
import logging

# logging.basicConfig(level=logging.DEBUG,filename="cds_reporting_metadata_test.log")

logger = logging.getLogger(__name__)
logger.debug("First debug")


def get_rulers():
    return '          1         2         3         4         5          6         7         ' \
           '8         9         1         2         3         4         5         5         7\n' \
           '01234567890123456789012345678901234567890123456789012345678901234567890123456789' \
           '01234567890123456789012345678901234567890123456789012345678901234567890123456789' \
           '0123456789'


# TODO enforce all digits on text fields with regular expressions or just use DIGITS_TEXT
class SalesRecord:
    distributor_id = "0111111110"
    mfr_id = "2333333332"
    mfr_product_id = "81111118"
    ship_to_cust_id = "3135551212"
    invoice_nbr = "0123456789"
    invoice_dt = "20170416"
    ship_dt = "20170415"
    filler = "         "
    extended_net = "031031031"  # should be equal to 123456.78
    distrib_product_id = "ABCDEFGHIJKL"
    product_description = "This is a product description "
    cases_shipped = "000001"
    boxes_shipped = "000002"
    units_shipped = "000003"
    case_gtin = "12345678901234"
    filler12 = "            "
    record_type = "SA"

    buff = []
    buff[0:9] = distributor_id
    buff[10:19] = mfr_id
    buff[20:27] = mfr_product_id
    buff[28:37] = ship_to_cust_id
    buff[38:47] = invoice_nbr
    buff[48:55] = invoice_dt
    buff[56:63] = ship_dt
    buff[64:72] = filler
    buff[73:81] = extended_net
    buff[82:93] = distrib_product_id
    buff[94:123] = product_description
    buff[124:129] = cases_shipped
    buff[130:135] = boxes_shipped
    buff[136:141] = units_shipped
    buff[142:155] = case_gtin
    buff[156:167] = filler12
    buff[168:169] = record_type  # "SA"

    record = "".join(buff)
    # rulers.print_rulers()
    # print (record)


class SalesTotalRecord:
    record_header = "".rjust(10, "9")
    filler28 = "".rjust(28)
    period_covered_start_date = "20170315"
    period_covered_end_date = "20170322"
    file_creation_date = "20170323"
    total_record_count = "1".ljust(9, "0")
    total_amount = "100".ljust(11, "0")
    filler86 = "".rjust(86)
    record_type = "AT"

    buff = []
    buff[0:9] = record_header
    buff[10:37] = filler28
    buff[38:45] = period_covered_start_date
    buff[46:53] = period_covered_end_date
    buff[54:61] = file_creation_date
    buff[62:70] = total_record_count
    buff[71:81] = total_amount
    buff[82:167] = filler86
    buff[168:169] = record_type

    record = "".join(buff)


class CustomerRecord:
    buff = []

    filler = "999999"
    class_of_trade = "____"
    ship_to_id = "2718281828"
    cust_name = "Test Customer                 "
    addr1 = "1313 Mockingbird Lane         "
    addr2 = "Subbasement                   "
    city = "Munsterville              "
    state = "PA"
    postal_code = "987654321"
    phone = "3135551212"
    nat = "NAT1000000"
    filler_1 = " "
    flag = "Y"
    record_type = "CD"

    buff[0:5] = filler
    buff[6:9] = class_of_trade
    buff[10:19] = ship_to_id
    buff[20:49] = cust_name
    buff[50:79] = addr1
    buff[80:109] = addr2
    buff[110:134] = city
    buff[135:136] = state
    buff[137:145] = postal_code
    buff[146:155] = phone
    buff[156:165] = nat
    buff[166:166] = flag
    buff[167:167] = filler_1
    buff[168:169] = record_type
    record = "".join(buff)


class CustomerTotalRecord:
    buff = []

    header = "9999999999"
    filler127 = "".ljust(127)
    total_record_count = "000000001"
    filler22 = "".ljust(22)
    record_type = "CT"

    buff[0:9] = header
    buff[10:136] = filler127
    buff[137:145] = total_record_count
    buff[147:167] = filler22
    buff[168:169] = record_type

    record = "".join(buff)


class InventoryRecord:
    buff = []

    distributor_id = "1234567890"
    mfr_id = "2222222222"
    mfr_product_id = "88888888"
    comments = "Comment".ljust(96, "-")
    cases = "111111"
    boxes = "222222"
    units = "333333"
    case_gtin = "14444444444441"
    filler = " ".ljust(12)
    record_type = "IR"

    buff[0:9] = distributor_id
    buff[10:19] = mfr_id
    buff[20:27] = mfr_product_id
    buff[28:123] = comments
    buff[124:129] = cases
    buff[130:135] = boxes
    buff[136:141] = units
    buff[142:155] = case_gtin
    buff[156:167] = filler
    buff[168:169] = record_type

    record = "".join(buff)


class InventoryTotalRecord:
    buff = []

    header = "9999999999"
    filler36 = "".ljust(36)
    inventory_date = "20170213"
    file_creation_date = "20170214"
    total_record_count = "000000001"
    filler97 = "".ljust(97)
    record_type = "IT"

    buff[0:9] = header
    buff[10:45] = filler36
    buff[46:53] = inventory_date
    buff[54:61] = file_creation_date
    buff[62:70] = total_record_count
    buff[71:167] = filler97
    buff[168:169] = record_type

    record = "".join(buff)


class TestCdsReportingMetadata(unittest.TestCase):
    logger = logging.getLogger(__name__)
    meta = CdsReportingMetadata()

    cust_rec = None
    customer_total_rec = None
    sales_rec = None
    sales_total_rec = None
    inventory_rec = None
    inventory_total_rec = None

    record_types = {
        "CD": meta.record_defs["customer"],
        "CT": meta.record_defs["customer_total"],
        "IR": meta.record_defs["inventory"],
        "IT": meta.record_defs["inventory_total"],
        "SA": meta.record_defs["sales"],
        "AT": meta.record_defs["sales_total"],
        # "##": meta.record_defs["comment"],
    }

    def test_customer(self):
        logger.info("begin test_customer")
        fields_by_name = {}
        for field in self.meta.record_defs["customer"]:
            fields_by_name[field["field_name"]] = field
        crc = CustomerRecord()
        record = crc.record

        key_value = field_metadata.get_bind_map(self.record_types["CD"], record)
        self.assertEqual(key_value["SHIP_TO_CUST_ID"], crc.ship_to_id)

        self.assertEqual(key_value["CUST_NM"], crc.cust_name.rstrip())
        self.assertEqual(key_value["ADDR_1"], crc.addr1.rstrip())
        self.assertEqual(key_value["ADDR_2"], crc.addr2.rstrip())
        self.assertEqual(key_value["CITY"], crc.city.rstrip())
        self.assertEqual(key_value["STATE"], crc.state.rstrip())
        self.assertEqual(key_value["POSTAL_CD"], crc.postal_code.rstrip())
        self.assertEqual(key_value["TEL_NBR"], crc.phone.rstrip())
        self.assertEqual(key_value["NATIONAL_ACCT_ID"], crc.nat.rstrip())
        self.assertEqual(key_value["SPECIAL_FLG"], crc.flag.rstrip())
        self.assertEqual(key_value["FILLER_1"].rstrip(), crc.filler_1.rstrip())
        self.assertEqual(key_value["RECORD_TYPE"], crc.record_type.rstrip())

        # x = FieldMetadata("SA", field_metadata.NUMERIC, length=2)

        # print x

        outrec = field_metadata.format_line(self.record_types["CD"], key_value)
        # rulers.print_rulers()
        # print (record)
        # print (outrec)
        logger.info(record)
        logger.info(outrec)
        self.assertEqual(record, outrec)
        logger.info("end test_customer")

    def test_sale(self):
        fields_by_name = {}
        for field in self.meta.record_defs["customer"]:
            fields_by_name[field["field_name"]] = field

        sr = SalesRecord()
        record = sr.record
        # rulers.print_rulers()
        # print (record)
        record_def = self.record_types["SA"]
        # for field_def in record_def:
        #    print (field_def)


        key_value = field_metadata.get_bind_map(record_def, record)

        self.assertEqual(key_value["DISTRIB_ID"], sr.distributor_id)
        self.assertEqual(key_value["MFR_ID"], sr.mfr_id)
        self.assertEqual(key_value["MFR_PRODUCT_ID"], sr.mfr_product_id)
        self.assertEqual(key_value["SHIP_TO_CUST_ID"], sr.ship_to_cust_id)
        self.assertEqual(key_value["INVOICE_CD"], sr.invoice_nbr)

        self.assertEqual(key_value["INVOICE_DT"], datetime.datetime.strptime(sr.invoice_dt, "%Y%m%d"))

        self.assertEqual(
            key_value["SHIP_DT"], datetime.datetime.strptime(sr.ship_dt, "%Y%m%d")
        )
        self.assertEqual(key_value["EXTENDED_NET_AMT"], int(sr.extended_net))  # TODO need to divide by 100
        self.assertEqual(key_value["DISTRIB_PRODUCT_REF"], sr.distrib_product_id)
        self.assertEqual(key_value["PRODUCT_DESCR"], sr.product_description.rstrip())
        self.assertEqual(key_value["CASES_SHIPPED"], int(sr.cases_shipped))
        self.assertEqual(key_value["BOXES_SHIPPED"], int(sr.boxes_shipped))
        self.assertEqual(key_value["UNITS_SHIPPED"], int(sr.units_shipped))
        self.assertEqual(key_value["CASE_GTIN"], sr.case_gtin)
        self.assertEqual(key_value["RECORD_TYPE"], sr.record_type)

        outrec = field_metadata.format_line(self.record_types["SA"], key_value)
        # rulers.print_rulers()

        self.sales_rec = outrec
        logger.info(record)
        logger.info(outrec)
        self.assertEqual(record, outrec)

    def test_inventory(self):
        logger.info("begin test_inventory")
        ir = InventoryRecord()
        record = ir.record
        key_value = field_metadata.get_bind_map(self.record_types["IR"], record)

        self.assertEqual(key_value["DISTRIBUTOR_ID"], ir.distributor_id)
        self.assertEqual(key_value["MFR_PRODUCT_ID"], ir.mfr_product_id)
        self.assertEqual(key_value["COMMENTS"], ir.comments)
        self.assertEqual(key_value["CASES"], int(ir.cases))
        self.assertEqual(key_value["BOXES"], int(ir.boxes))
        self.assertEqual(key_value["UNITS"], int(ir.units))
        self.assertEqual(key_value["CASE_GTIN"], ir.case_gtin)
        self.assertEqual(key_value["RECORD_TYPE"], ir.record_type)

        outrec = field_metadata.format_line(self.record_types["IR"], key_value)
        self.inventory_rec = outrec

        logger.info("about to print records")
        logger.info(record)
        logger.info(outrec)
        self.assertEqual(record, outrec)
        logger.info("end test_inventory")

    def test_inventory2(self):
        logger.info("begin test_inventory")

        MFR_PRODUCT_ID = '00001957'
        LINE_NUMBER = None
        BOXES = 0
        ETL_FILE_ID = 201723
        UNITS = -76
        CASES = 84
        CASE_GTIN = '00012345019572'
        FILLER = None
        DISTRIBUTOR_ID = '0000000001'
        ETL_INVENTORY_ID = 8215
        COMMENTS = None
        RECORD_TYPE = 'IR'
        MFR_ID = '0000000005'
        INVENTORY_UNIT_MEAS_ID = None
        INVENTORY_QTY = None

        data_map = {
            'MFR_PRODUCT_ID': MFR_PRODUCT_ID,
            'LINE_NUMBER': LINE_NUMBER,
            'BOXES': BOXES,
            'ETL_FILE_ID': ETL_FILE_ID,
            'UNITS': UNITS,
            'CASES': CASES,
            'CASE_GTIN': CASE_GTIN,
            'FILLER': FILLER,
            'DISTRIBUTOR_ID': DISTRIBUTOR_ID,
            'ETL_INVENTORY_ID': ETL_INVENTORY_ID,
            'COMMENTS': COMMENTS,
            'RECORD_TYPE': RECORD_TYPE,
            'MFR_ID': MFR_ID,
            'INVENTORY_UNIT_MEAS_ID': None,
            'INVENTORY_QTY': 'IR'
        }

        outrec = field_metadata.format_line(self.record_types["IR"], data_map)
        print(outrec)
        self.assertEqual(outrec[0:10], DISTRIBUTOR_ID)
        self.assertEqual(outrec[10:20], MFR_ID)
        self.assertEqual(outrec[20:28], MFR_PRODUCT_ID)

        self.assertEqual(outrec[28:124], "".ljust(96))
        self.assertEqual(outrec[124:130], "000084")
        self.assertEqual(outrec[130:136], "000000")
        self.assertEqual(outrec[136:142], "-00076")
        self.assertEqual(outrec[142:156], CASE_GTIN)
        self.assertEqual(outrec[156:168], "".ljust(12))
        self.assertEqual(outrec[168:170], RECORD_TYPE)

    def test_inventory_total(self):
        logger.info("begin test_inventory_total")
        itr = InventoryTotalRecord()
        record = itr.record
        key_value = field_metadata.get_bind_map(self.record_types["IT"], record)

        self.assertEqual(key_value["HEADER"], itr.header)
        self.assertEqual(len(key_value["FILLER36"]), 36)
        self.assertEqual(key_value["FILLER36"], itr.filler36)
        self.assertEqual(key_value["INVENTORY_DT"], datetime.datetime.strptime(itr.inventory_date, '%Y%m%d'))
        self.assertEqual(key_value["FILE_CREATION_DT"], datetime.datetime.strptime(itr.file_creation_date, '%Y%m%d'))
        self.assertEqual(key_value["RECORD_CNT_REPORTED"], int(itr.total_record_count))
        self.assertEqual(key_value["FILLER97"], itr.filler97)
        self.assertEqual(key_value["RECORD_TYPE"], itr.record_type)
        outrec = field_metadata.format_line(self.record_types["IT"], key_value)
        self.inventory_total_rec = outrec

        # rulers.print_rulers()
        logger.info(record)
        logger.info(outrec)
        self.assertEqual(record, outrec)
        logger.info("end test_inventory_total")

    def test_customer_total(self):
        logger.info("begin test_customer_total")
        # field_dictionary = field_metadata.get_field_dictionary(self.meta.record_defs["inventory"])
        ct = CustomerTotalRecord()
        record = ct.record
        key_value = field_metadata.get_bind_map(self.record_types["CT"], record)

        self.assertEqual(key_value["HEADER"], ct.header)
        self.assertEqual(key_value["FILLER_127"], ct.filler127)
        self.assertEqual(key_value["CUSTOMER_COUNT"], int(ct.total_record_count))
        self.assertEqual(key_value["FILLER_22"], ct.filler22)
        self.assertEqual(key_value["RECORD_TYPE"], ct.record_type)

        outrec = field_metadata.format_line(self.record_types["CT"], key_value)
        self.customer_total_rec = outrec
        logger.info(record)
        logger.info(outrec)

        # rulers.print_rulers()

        self.assertEqual(record, outrec)
        logger.info("end test_customer_total")

    def test_sales_total(self):
        logger.info("begin test_sales_total")
        sales_tot = SalesTotalRecord()
        record = sales_tot.record
        key_value = field_metadata.get_bind_map(self.record_types["AT"], record)

        self.assertEqual(key_value["HEADER"], sales_tot.record_header)
        self.assertEqual(key_value["FILLER_28"], sales_tot.filler28)
        self.assertEqual(key_value["SALES_START_DT"], datetime.datetime.strptime(sales_tot.period_covered_start_date, '%Y%m%d'))
        self.assertEqual(key_value["SALES_END_DT"], datetime.datetime.strptime(sales_tot.period_covered_end_date, '%Y%m%d'))
        self.assertEqual(key_value["FILE_CREATE_DT"], datetime.datetime.strptime(sales_tot.file_creation_date, '%Y%m%d'))
        self.assertEqual(key_value["SALES_REC_CNT"], int(sales_tot.total_record_count))
        self.assertEqual(key_value["SUM_EXT_NET_AMT"], int(sales_tot.total_amount))
        self.assertEqual(key_value["RECORD_TYPE"], sales_tot.record_type)
        outrec = field_metadata.format_line(self.record_types["AT"], key_value)
        # rulers.print_rulers()
        self.sales_total_rec = outrec
        logger.info(record)
        logger.info(outrec)
        self.assertEqual(record, outrec)
        logger.info("end test_sales_total")

    def test_customer_total(self):
        logger.info("begin test_customer_total")
        # field_dictionary = field_metadata.get_field_dictionary(self.meta.record_defs["inventory"])
        ct = CustomerTotalRecord()
        record = ct.record
        key_value = field_metadata.get_bind_map(self.record_types["CT"], record)

        self.assertEqual(key_value["HEADER"], ct.header)
        self.assertEqual(key_value["FILLER_127"], ct.filler127)
        self.assertEqual(key_value["CUSTOMER_COUNT"], int(ct.total_record_count))
        self.assertEqual(key_value["FILLER_22"], ct.filler22)
        self.assertEqual(key_value["RECORD_TYPE"], ct.record_type)

        outrec = field_metadata.format_line(self.record_types["CT"], key_value)
        self.customer_total_rec = outrec

        # rulers.print_rulers()
        logger.info(record)
        logger.info(outrec)
        self.assertEqual(record, outrec)
        logger.info("end test_customer_total")

    # def test_sale(self):  #TODO complete

    def test_inventory(self):
        data_map = {
            'MFR_PRODUCT_ID': '00001957',
            'LINE_NUMBER': None,
            'BOXES': 0,
            'ETL_FILE_ID': 201723,
            'UNITS': -76,
            'CASES': 84,
            'CASE_GTIN': '00012345019572',
            'FILLER': ' ',
            'DISTRIBUTOR_ID': '1',
            'ETL_INVENTORY_ID': 8215,
            'COMMENTS': None,
            'RECORD_TYPE': 'IR',
            'MFR_ID': '5',
            'INVENTORY_UNIT_MEAS_ID': None,
            'INVENTORY_QTY': None}

        buff = field_metadata.format_line(self.meta.record_defs["inventory"], data_map)

        self.assertEqual(buff[0:10], "0000000001")  # Distributor identification DISTRIBUTOR_ID
        self.assertEqual(buff[10:20], "0000000005")  # Manufacturer ID
        self.assertEqual(buff[20:28], "00001957")  # Manufacturer Product Id MFR_PRODUCT_ID
        self.assertEqual(buff[28:124], "".ljust(96))
        self.assertEqual(buff[124:130], "000084")  # cases
        self.assertEqual(buff[130:136], "000000")  # boxes
        self.assertEqual(buff[136:142], "-00076")  # units
        self.assertEqual(buff[142:156], "00012345019572")
        self.assertEqual(buff[156:168], "".ljust(12))
        self.assertEqual(buff[168:170], 'IR')



    def test_inventory_total(self):


        data_map = {
            'INVENTORY_DT': datetime.date(2017,7,4),
            'FILE_CREATION_DT': datetime.date(2017,7,5),
            'RECORD_CNT_REPORTED': 3,
            "HEADER" : "9999999999",
            "FILLER36" : "".ljust(36),
            "RECORD_TYPE" : "IT",
            "FILLER97" : "".ljust(97)
        }

        buff = field_metadata.format_line(self.meta.record_defs["inventory_total"], data_map)

        self.assertEqual(buff[0:10], "9999999999")
        self.assertEqual(buff[10:46], "".ljust(36))
        self.assertEqual(buff[46:54], "20170704")
        self.assertEqual(buff[54:62], "20170705")
        self.assertEqual(buff[62:71], "000000003")
        self.assertEqual(buff[71:168], "".ljust(97))
        self.assertEqual(buff[168:170], "IT")

    def test_it(self):
        data_map = {
         'RECORD_TYPE': 'IT',
         'RECORD_CNT_ACTUAL': None,
         'FILLER97': '                                                                                                 ',
         'ETL_FILE_ID': 1, 'FILLER36': '                                    ',
         'RECORD_CNT_REPORTED': 608064,
         'FILE_CREATION_DT': datetime.date(2016,8,28),
         'LINE_NUMBER': 9630,
         'INVENTORY_DT': datetime.date(2016,8,28),
         'HEADER': '9999999999'
         }

        buff = field_metadata.format_line(self.meta.record_defs["inventory_total"], data_map)

        print(get_rulers())
        print(buff)

    def test_etl_inventory_tot(self):
        import sqlite3
        import datetime
        create_table_sql = """
        CREATE TABLE etl_inventory_tot (
            etl_file_id         integer primary key,
            line_number         integer,
            inventory_dt        timestamp,
            file_creation_dt    timestamp,
            record_cnt_reported numeric(8),
            record_cnt_actual   numeric(8)
        );

        """
        connection = sqlite3.Connection(":memory:")
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        binds = {
            "LINE_NUMBER" : 1,
            "INVENTORY_DT" : datetime.datetime(2017,7,4),
            "FILE_CREATION_DT" : datetime.datetime(2017,7,4),
            "RECORD_CNT_REPORTED" : 1,
            "RECORD_CNT_ACTUAL"   : 1
        }

        insert_sql = """
        insert into etl_inventory_tot (
            line_number,
            inventory_dt,
            file_creation_dt,
            record_cnt_reported,
            record_cnt_actual
        )
        values (
            :LINE_NUMBER, 
            :INVENTORY_DT,
            :FILE_CREATION_DT,
            :RECORD_CNT_REPORTED,
            :RECORD_CNT_ACTUAL
        )
        """
        cursor.execute(insert_sql,binds)
        rows = cursor.execute("select * from etl_inventory_tot")
        for col in cursor.description:
            print (col)
        print ("select * ")
        for row in rows:
            col_index = 0
            for col in row:
                print ("col_index %s value '%s' type %s", (col_index, col, str(type(col))))
        print ("cast to date")

        rows  = cursor.execute("select line_number, date(inventory_dt), date(file_creation_dt) from etl_inventory_tot")
        for row in rows:
            col_index = 0
            for col in row:
                print ("col_index %s value '%s' type %s" % (col_index, col, str(type(col))))


if __name__ == '__main__':
    unittest.main()
