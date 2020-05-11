import logging

from pdsutil.DbUtil import CursorHelper


class SeedSalesReportingDatabase:
    def __init__(self, connection, verbose=False):
        """

        :param connection: a database connection
        """
        self.connection = connection
        self.cursor = CursorHelper(self.connection.cursor())
        logger = logging.getLogger("SeedSalesReportingDatabase")
        self.verbose = verbose

    def seed_manufacturers(self):

        """
        Populates the tables org and org_mfr with CDS manufacturer identifiers
        :return: None
        """
        # TODO load from resources/cds_manufactures.csv
        mfrs = [
            ("0000000020", "F-L", "Frito-Lay"),
            ("0000000030", "GM", "General Mills"),
            ("0000000040", "HVEND", "Hershey Vending"),
            ("0000000050", "HFUND", "Hershey Fund Raising"),
            ("0000000055", "HCONC", "Hershey Concession"),
            ("0000000060", "SNYDERS", "Snyder's of Hanover"),
            ("0000000080", "KELLOGG", "Kellogg, Keebler"),
            ("0000000115", "KARS", "Kar Nut Product (Kar's)"),
            ("0000000135", "MARS", "Mars Chocolate "),
            ("0000000145", "POORE", "Inventure Group (Poore Brothers)"),
            ("0000000150", "WOW", "WOW Foods"),
            ("0000000160", "CADBURY", "Cadbury Adam USA, LLC"),
            ("0000000170", "MONOGRAM", "Monogram Food"),
            ("0000000185", "JUSTBORN", "Just Born"),
            ("0000000190", "HOSTESS", "Hostess, Dolly Madison"),
            ("0000000210", "SARALEE", "Sara Lee"),
        ]
        for mfr in mfrs:
            binds = dict(zip(("CDS_MFR_ID", "ORG_CD", "ORG_NM"), mfr))
            if self.verbose:
                logging.info("binds: %s", binds)
            self.cursor.execute(
                "insert into org (org_cd, org_nm) values (%(ORG_CD)s, %(ORG_NM)s)",
                binds)
            self.cursor.execute("""
                insert into org_mfr( 
                    org_id,cds_mfr_id
                ) 
                select org_id, %(CDS_MFR_ID)s 
                from   org 
                where org_cd = %(ORG_CD)s""",
                binds)

    def seed_distributor(self):
        self.cursor.execute("insert into org(org_cd) values ( %(ORG_CD)s)", {"ORG_CD": "EXOTICTX"})


        print('EXOTICTX inserted into org')
        verify_cursor = CursorHelper(self.connection.cursor())
        rows = verify_cursor.execute('select * from org order by org_cd')
        
        for row in rows:
            print('org_id ' + str(row[0]) + ' org_cd ' + row[1])

        

        self.cursor.execute("insert into org_distrib(org_id,distrib_id) "
                            "select org_id,'EXOTICTX' "
                            "from org "
                            "where org_cd = %(ORG_CD)s", {"ORG_CD": "EXOTICTX"})

        self.cursor.execute("insert into org_datafeed(org_id) "
                            "select org_id "
                            "from org "
                            "where org_cd = %(ORG_CD)s", {"ORG_CD": "EXOTICTX"})

    def process(self):
        """
        Populates all the prerequisite tables
        :return:
        """
        self.seed_manufacturers()
        self.seed_distributor()
