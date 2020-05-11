import logging

from pdsutil.DbUtil import ConnectionHelper
from pdsutil.Dexterity import StatementRunner, StatementHelper


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
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Post")
        self.connection = conn

    def process(self, etl_file_id):
        """

        :param etl_file_id - int the file
        :return:
        """
        assert (etl_file_id, int)
        self.logger.info("processing etl_file_id %s " % etl_file_id)
        binds = {"ETL_FILE_ID": etl_file_id}
        runner = StatementRunner(self.connection, self.statements)
        runner.process(binds)
        self.connection.commit()

    # TODO ! externalize in yaml or .sr.sql
    # check severity level
    # partial post options
    statements = [
        StatementHelper("""
    update etl_sale
    set product_id = (
        select  product_id
        from    product
        where   product.case_gtin = etl_sale.case_gtin
                or product.mfr_product_id = etl_sale.mfr_product_id)
    where   etl_file_id = %(ETL_FILE_ID)s
            and
            product_id is null
    """,
    "Assign product id based on mfr_product_id or "
    "GTIT will blow up if two products match"
    ),  # TODO should commit

        StatementHelper("""
    insert into post_sale (
        etl_sale_id, org_distrib_id, org_mfr_id,
        product_id,  distributor_customer_id,   normalized_qty
    ) select
        s.etl_sale_id, s.org_distrib_id, s.org_mfr_id,
        s.product_id, s.distributor_customer_id, 0  /* fix TODO and add hash */
    from etl_sale s
    where s.etl_sale_id is not null
        and s.org_distrib_id is not null
        and s.org_mfr_id is not null
        and s.product_id is not null
        and s.distributor_customer_id is not null
        and s.etl_file_id = %(ETL_FILE_ID)s
        and not exists (
            select 'x'
            from post_sale p
            where p.etl_sale_id = s.etl_sale_id)
        """, "insert into post"),


        # TODO externalize all of this
        StatementHelper("""
    insert into product_nomen(
        org_id,
        product_id,
        product_ref_cd,
        descr
    ) select distinct
        org_distrib_id,
        product_id,
        distrib_product_ref,
        product_descr
    from etl_sale
    where
        org_distrib_id is not null \
        and product_id is not null \
        and distrib_product_ref is not null""",
                        "populate product nomen could be duplicate descriptions"  # should point back to etl file
                        # should have first occurence and other dates
                        )
    ]


def post_customers(etl_file_id:int) -> None:
    """
    insert into 
    :param etl_file_id: 
    :return: 
    """

insert_sql = """    
insert into vp_distributor_customer
	etl_customer_id,
	ship_to_cust_id,
	address_id,
	class_of_trade,
	ship_to_cust_id,
	cust_nm,
	addr_1,
	addr_2,
	city,
	state,
	postal_cd,
	valid_addr_1,
	valid_addr_2,
	valid_city,
	valid_state,
	valid_postal_cd,
	cntry_id,
	tel_nbr,
	national_acct_id,
	special_flg,
	bank_route_transit,
	eff_dt
)
select
    etl_customer_id,
    ship_to_cust_id,
    address_id,
    class_of_trade,
    ship_to_cust_id,
    cust_nm,
    addr_1,
    addr_2,
    city,
    state,
    postal_cd,
    valid_addr_1,
    valid_addr_2,
    valid_city,
    valid_state,
    valid_postal_cd,
    cntry_id,
    tel_nbr,
    national_acct_id,
    special_flg,
    bank_route_transit
from etl_customer
where etl_file_id = $(etl_file_id) and
      not exists
      (select 'x' from vp_distributor_customer
       where ship_to_cust_cd =  %(SHIP_TO_CUST_CD) and
       org_distrib_id = %(ORG_DISTRIB_ID)
"""

update_sql = """
    update  vp_distributor_customer c
    set 
        class_of_trade = e.class_of_trade,
        cust_nm        = e.cust_nm,
        addr_1         = e.addr_1,
        addr_2         = e.addr_2,
        city           = e.city,
        state          = e.state,
        postal_cd      = e.postal_cd,
        validated_address_id = null,
        cntry_id       = e.cntry_cd,
        tel_nbr        = e.tel_nbr,
        national_acct_id = e.national_acct_id,
        special_flg = e.special_flg,
        bank_route_transit = bank_route_transit,
        eff_dt             = %(EFF_DT)s
    ) 
    from etl_customer e
    where 
        e.ship_to_cust_id = c.ship_to_cust_id and
        %(EFF_DT) > c.eff_dt 
    -- )
    """

validated_address_insert = """
    insert into  validated_address (
        addr_1              varchar(30),
        addr_2              varchar(30),
        city                varchar(25),
        state               varchar(2),
        postal_cd           varchar(9),
    ) 
    select 
        addr_1              varchar(30),
        addr_2              varchar(30),
        city                varchar(25),
        state               varchar(2),
        postal_cd           varchar(9),
    from vp_distributor_customer
    where eff_dt = %(EFF_DT) 
    minus select 
        addr_1,
        addr_2,
        city,
        state,
        postal_cd         
    from validated_address
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
    process_all()
