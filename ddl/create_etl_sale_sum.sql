create table etl_sale_sum as
select 
       org_mfr_id,
       ship_to_cust_id,
       mfr_product_id,
       extract (month from ship_dt) ship_dt_month,
       extract (year from ship_dt) ship_dt_year,
       sum(extended_net_amt) sum_ext_net_amt,
       sum(cases_shipped) cases_shipped
from etl_sale
group by
      org_mfr_id, 
      ship_to_cust_id, 
      mfr_product_id,
      extract (month from ship_dt),
      extract (year from ship_dt) ;
