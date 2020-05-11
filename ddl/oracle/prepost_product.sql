update etl_sale set product_id = (select product_id from
product where  product.gtin = etl_product.product_id)
where product_id is null;

update etl_sale set product_id = (select product_id from
product_nomen where product_nomen.descr = etl_sale.product_descr)
where product_id is null; 

