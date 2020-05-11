.echo on 

PRAGMA foreign_keys = ON;

create table org
(
	org_id integer primary key,
	org_cd varchar2(16),
	org_nm varchar2(32)
);

create unique index org_uq on org(org_cd);

create table org_datafeed
(
	org_id integer references org(org_id)
);

create unique index org_datafeed on org(org_cd) ;

create table etl_file
(
	etl_file_id  integer primary key,
	rpt_org_id	number(9) not null,
        datafeed_org_id integer references org_datafeed(org_id),
	cust_cnt_rpt 	number(9),
	cust_cnt_act    number(9),
	inventory_dt	date,
	inventory_file_create_dt date,
	inventory_rec_cnt_act number(9),
	inventory_rec_cnt_rpt number(9),
	sale_prd_cover_start_dt    date,
	sale_prd_cover_end_dt      date,
	sale_min_dt_act            date,
        sale_max_dt_act            date,
	sale_file_create_dt  date,
	sale_rec_cnt_rpt    number(9),
	sale_rec_cnt_act    number(9),
        sale_net_extend_rpt   number(11,2),
        sale_net_extend_act   number(11,2)
);


create table etl_customer
( 
	etl_customer_id  integer primary key,
	etl_file_id      integer references etl_file(etl_file_id),
        class_of_trade   varchar(4),
	ship_to_cust_id  varchar(10),
	cust_nm          varchar2(30),
	addr_1           varchar2(30),
	addr_2           varchar2(30),
	city             varchar2(25),
	state            varchar2(2),
	postal_cd        varchar2(9),
	cntry_id         varchar2(3),
	tel_nbr 	 varchar2(10),
	national_acct_id varchar2(10),
	special_flg	 varchar2(1)
);



create table etl_inventory
(
	etl_inventory_id integer primary key,
	etl_file_id      integer references etl_file(etl_file_id),
	distributor_id varchar2(10),
	mfr_id		varchar2(10),
	mfr_product_id  number(8),
	comments  	varchar2(96),
	cases		number(6),
	boxes		number(6),
	units		number(6),
        case_gtin       varchar2(14),
	inventory_qty   number(9,3),
	inventory_unit_meas_id varchar2(3)
);



/* */
create table etl_inventory_tot
(
	etl_file_id      integer references etl_file(etl_file_id),
	inventory_dt     date,
	file_creation_dt date,
	record_cnt_reported  number(8),
	record_cnt_actual  number(8)
);

create unique index on etl_inventory_tot (etl_file_id);


/* */
create table etl_sale (
	etl_sale_id number(9) integer primary key,
	etl_file_id number(9) integer references etl_file(etl_file_id),
	distrib_id varchar2(10) not null,
	mfr_id          varchar2(10) not null,
        mfr_product_id  varchar2(10),	
	ship_to_cust_id varchar2(10) not null,
	invoice_cd      varchar2(10),	
	invoice_dt date,
       	ship_dt  date,	
	/* should have a currency */
	extended_Net_Amt number(9,2),
	curr_cd varchar2(3),
	distrib_prod_ref varchar2(12),	
	product_descr varchar(32),
	cases_shipped number(9),	
	boxes_shipped number(9),	
	units_shipped number(9),	
	case_gtin     varchar2(14),
	product_id    number(9),
	customer_id   number(9)
);



create table etl_sale_tot (
	etl_file_id integer references etl_file(etl_file_id),
	sales_start_dt date not null,
	sales_end_dt date  not null,
	file_create_dt date  not null,
        sales_rec_cnt  number(9),	
	sum_ext_net_amt number(11,2) not null
);

/*

create table product 
(
	product_id      integer primary key,
	mfr_id          number(9) not null,
	product_descr   varchar2(60),
	gtin            varchar2(14),
 	stat_cd         char(1),
 	eff_dt          date,
 	end_dt          date,
 	track_invt_flg  varchar2(1),
 	upc14           varchar2(14),
 	product_grp_id  number(9),
 	product_cat_id  number(9)
);


create table product_pkg
(
	product_pkg_id integer primary key,
        product_id     number(9) not null,
        pkg_id         number(9) not null,
        pkg_qty_numerator number(5) not null,
        pkg_qty_divisor   number(5) not null
);





create table product_nomen
(
	product_nomen_id number(9) not null,
	org_id           number(9) not null,
	product_id       number(9) not null,
	product_nomen    varchar2(50),
	descr            varchar2(60) 
);

alter table product_nomen add constraint pn_pk 
primary key (product_nomen_id);

create table customer
(
	customer_id number(9) not null
);

alter table customer add constraint customer_pk primary key (customer_id);

alter table customer add constraint c_no_fk 
foreign key (customer_id) references org (org_id);

create table product_suspect_hdr
(
 	product_suspect_hdr_id number(9) not null,
	descr                  varchar2(60)
);

alter table product_suspect_hdr add constraint  psh_pk 
primary key (product_suspect_hdr_id);

create table product_suspect_dtl
(
	product_suspect_dtl_id number(9) not null,
	product_id             number(9) not null,
	product_suspect_hdr_id number(9) not null
);

create table etl_customer_tot
(
        etl_file_id            number(9) not null,
        customer_count         number(9) not null
);

alter table etl_customer_tot add constraint etl_customer_total_pk
primary key (etl_file_id);

alter table etl_customer_tot add constraint ect_ef_fk 
foreign key (etl_file_id) references etl_file (etl_file_id);

create table org_mfr
(
    org_id number(9) not null,
    cds_id varchar2(10)
);   

alter table org_mfr add constraint org_mfr_pk 
primary key (org_id);

alter table org_mfr add constraint om_uq 
unique (cds_id);

exit 

*/
