
from pdsutil.DbUtil import ConnectionHelper

connection = ConnectionHelper().get_named_connection("it")
cursor = connection.cursor()
cursor.execute("select distinct ship_to_cust_id from etl_sale order by ship_to_cust_id")
sale_ship_to_ids = cursor.fetchall()
print (sale_ship_to_ids)
cursor.execute("select distinct ship_to_cust_id from etl_customer order by ship_to_cust_id")
cust_ship_to_ids = cursor.fetchall()
print (cust_ship_to_ids)
for sale_id_t, cust_id_t in zip(sale_ship_to_ids,cust_ship_to_ids):
    binds = {
        "to_id" : sale_id_t[0],
        "cust_id" : cust_id_t[0]
    }
    print ("cust_id %s to_id %s" % (sale_id_t[0],cust_id_t[0]))
    cursor.execute("update etl_customer set ship_to_cust_id = %(to_id)s where ship_to_cust_id = %(cust_id)s", binds)
connection.commit()
