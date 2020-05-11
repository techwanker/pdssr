update etl_sale set product_id = (select product_id from
product where  product.gtin = etl_sale.case_gtin)
where product_id is null; /** todo fix  case_gtin */

/** todo should this require org */
update etl_sale set product_id = (select product_id from
product_nomen where product_nomen.descr = etl_sale.product_descr)
where product_id is null; 

