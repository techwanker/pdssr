;--dis
create table vp_distributor_customer (
    vp_distributor_customer_id serial primary key,
    org_nomen_id               integer references org
    etl_customer_id     integer references etl_customer,
    class_of_trade      varchar(4),
    ship_to_cust_id     varchar(10),
    cust_nm             varchar(30),
    addr_1              varchar(30),
    addr_2              varchar(30),
    city                varchar(25),
    state               varchar(2),
    postal_cd           varchar(9),
    cntry_id            varchar(3),
    tel_nbr             varchar(10),
    national_acct_id    varchar(10),
    special_flg         varchar(1),
    effective_date      date
)