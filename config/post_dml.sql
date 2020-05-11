etl_sale_update:
    sql: >
    update etl_sale
    set product_id = (
        select  product_id
        from    product
        where   product.case_gtin = etl_sale.case_gtin
                or product.mfr_product_id = etl_sale.mfr_product_id)
    where   etl_file_id = %(ETL_FILE_ID)s
            and
            product_id is null
    descr: >
    	Assign product id based on mfr_product_id or 
        GTIT will blow up if two products match

product_nomen_insert:
    sql: >
        insert into product_nomen(
            org_id,
            product_id,
            product_ref_cd,
            descr
        ) select distinct
            ef.rpt_org_id,
            es.product_id,
            es.distrib_product_ref,
            es.product_descr
        from etl_sale es,
             etl_file ef
        where
            ef.etl_file_id = es.etl_file_id and
            org_distrib_id is not null
            and product_id is not null
            and distrib_product_ref is not null
    descr: >
        populate product nomen could be duplicate descriptions  # should point back to etl file
        # should have first occurence and other dates


vp_distributor_customer_insert:
    sql: >
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

update_sql:
	sql: >
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

validated_address_insert:
	sql: >
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
 