create or replace view etl_file_stats as
select table_name, etl_file_id, rec_count from
(
        select 'etl_customer' table_name, etl_file_id, count(*) rec_count
        from etl_customer
        union
        select 'etl_sale', etl_file_id, count(*)
        from etl_sale
        union
        select 'etl_inventory', etl_file_id, count(*)
        from etl_inventory
        union 
        select 'etl_inventory_tot', etl_file_id, count(*)
        from etl_inventory_tot
        union
        select 'etl_customer_tot', etl_file_id, count(*)
        from etl_customer_tot
) group by etl_file_id, table_name
