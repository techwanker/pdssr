#!/usr/bin/python
import csv
import random

from faker import Factory

# from pdsutil.FieldMetadata import FieldMetadata
import pdsutil.field_metadata as field_metadata
from pdssr.CdsReportingMetadata import CdsReportingMetadata
from pdssr.testdata.AddressGenerator import AddressGenerator

fake = Factory.create()

address_generator = AddressGenerator()
record_defs = CdsReportingMetadata().record_defs

ruler = """#
#         1         2         3         4         5         6         7         8         9         0         1         2         3         4         5         6         7
#12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"""


def get_customer():
    ship_to_cust_id = random.randint(1, 999999999)
    cust_nm = fake.company()
    address = address_generator.get_addr()
    addr_1 = address[0]
    addr_2 = ""
    city = address[1]
    state = address[2]
    postal_cd = address[3]
    tel_nbr = random.randint(2142000000, 2149999999)
    national_acct_id = tel_nbr
    special_flg = "N"
    cust = {
        "FILLER_00_05": "     ",
        "CLASS_OF_TRADE": "____",
        "SHIP_TO_CUST_ID": str(ship_to_cust_id),
        "CUST_NM": str(cust_nm),
        "ADDR_1": addr_1,
        "ADDR_2": addr_2,
        "CITY": city,
        "STATE": state,
        "POSTAL_CD": postal_cd,
        "TEL_NBR": str(tel_nbr),
        "NATIONAL_ACCT_ID": str(national_acct_id),
        "SPECIAL_FLG": special_flg,
        "FILLER_1": " ",
        "RECORD_TYPE": "SA"
    }

    return cust


def write_customers(file, count):
    with open(file, "wb") as csvfile:
        writer = csv.writer(csvfile, dialect="excel",
                            delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_NONNUMERIC)
        for i in range(0, count):
            writer.writerow(get_customer())


def format_customers(file, count):
    outfile = open(file, "w")
    definition = record_defs["customer"]
    print(ruler)
    for i in range(0, count):
        customer = get_customer()
        formatted = field_metadata.format_line(definition, customer)
        print(formatted)
        outfile.write(formatted)
        outfile.write("\n")


if __name__ == "__main__":
    # write_customers("/tmp/customers.csv",1000)
    format_customers("/tmp/customers.cds", 6000)
