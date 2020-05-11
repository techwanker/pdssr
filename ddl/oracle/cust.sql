create table customer_nomen (
	customer_nomen_id number(9) not null,
	org_id            number(9) not null,
	org_customer_id   varchar2(16) not null
);

alter table customer_nomen add constraint cn_pk primary key 
(
	customer_nomen_id
);

create column comment on customer_nomen.customer_nomen_id 'Surrogate primary key'.

create column comment on customer_nomen.org_id 'Identifier for the org that identifies this customer with the contents of org_customer_id.'

