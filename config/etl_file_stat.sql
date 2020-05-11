create view etl_file_stat as
select etl_file_id,
    count(*)        record_count,
    min(invoice_dt) min_invoice_dt,
    max(invoice_dt) max_invoice_dt,
    count(distinct(mfr_product_id)) count_distinct_mfr_product_id,
    count(distinct(distrib_prod_ref)) count_distinct_distrib_prod_ref
from etl_sale
group by etl_file_id;

