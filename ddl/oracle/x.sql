create table product 
(
	product_id       number(9) not null,
	org_id           number(9) not null,
	product_descr	 varchar2(64) not null,
	product_short_descr varchar2(32) not null
);

alter table product add constraint product_pk primary key (product_id);

create table product_nomen
(
	product_nomen_id number(9) not null,
	org_id           number(9),
	product_id       number(9),
	product_nomen    varchar2(50),
	descr            varchar2(60) 
) ;

alter table product_nomen add constraint pn_pk primary_key(product_nomen_id);
