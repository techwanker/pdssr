set echo on
spool sales_reporting 
create table org
(
	org_id number(9) not null,
	org_cd varchar2(16),
	org_nm varchar2(32)
);

alter table org add constraint org_pk primary key (org_id);

alter table org add constraint org_uq unique(org_cd);

create sequence org_id_seq;

create table org_datafeed
(
	org_id number(9) not null
);

alter table org_datafeed add constraint org_datafeed 
primary key (org_id);

alter table org_datafeed add constraint od_o_fk 
foreign key (org_id) references org(org_id);

create table etl_file
(
	etl_file_id number(9) not null,
	rpt_org_id	number(9) not null,
        datafeed_org_id number(9) not null,
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


alter table etl_file add constraint etl_file_pk
 primary key (etl_file_id);


alter table etl_file add constraint ef_od_fk 
foreign key (datafeed_org_id) references org_datafeed(org_id);



create sequence etl_file_id_seq;
/* */
create table etl_customer
(
	etl_customer_id  number(9) not null,
	etl_file_id      number(9) not null,
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

comment on column etl_customer.etl_customer_id is 'Surrogate primary key.';

alter table etl_customer 
add constraint etl_customer_pk 
primary key (etl_customer_id);

alter table etl_customer add constraint ec_ef_fk 
foreign key (etl_file_id) references etl_file(etl_file_id);

create sequence etl_customer_id_seq;
/* */
create table etl_inventory
(
	etl_inventory_id number(9) not null,
	etl_file_id      number(9) not null,
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

alter table etl_inventory add constraint etl_inventory_pk
primary key (etl_inventory_id);

alter table etl_inventory add constraint ei_ef_fk 
foreign key (etl_file_id) references etl_file(etl_file_id);

create sequence etl_inventory_id_seq;

/* */
create table etl_inventory_tot
(
	etl_file_id      number(9) not null,
	inventory_dt     date,
	file_creation_dt date,
	record_cnt_reported  number(8),
	record_cnt_actual  number(8)
);


alter table etl_inventory_tot add constraint etl_inventory_tot_pk
primary key (etl_file_id);

alter table etl_inventory_tot add constraint eit_ef_fk foreign key
(etl_file_id) references etl_file(etl_file_id);

/* */
create table etl_sale (
	etl_sale_id number(9) not null,
	etl_file_id number(9) not null,
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

alter table etl_sale add constraint etl_sale_pk 
primary key (etl_sale_id);

alter table etl_sale add constraint es_ef_fk 
foreign key (etl_file_id) references etl_file(etl_file_id);

create sequence etl_sale_id_seq;

create table etl_sale_tot (
	etl_sale_tot_id number(9) not null,
	etl_file_id number(9) not null,
	sales_start_dt date not null,
	sales_end_dt date  not null,
	file_create_dt date  not null,
        sales_rec_cnt  number(9),	
	sum_ext_net_amt number(11,2) not null
);

alter table etl_sale_tot add constraint etl_sale_tot_pk 
primary key (etl_sale_tot_id);

alter table etl_sale_tot add constraint est_ef_fk
foreign key (etl_file_id) references etl_file(etl_file_id);

create table product 
(
	product_id      number(9) not null,
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

create sequence product_id_seq;

create table product_pkg
(
	product_pkg_id number(9) not null,
        product_id     number(9) not null,
        pkg_id         number(9) not null,
        pkg_qty_numerator number(5) not null,
        pkg_qty_divisor   number(5) not null
);



alter table product_pkg add constraint pp_pk 
primary key (product_pkg_id);

create sequence product_pkg_id_seq;

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
