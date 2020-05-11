import pandas
import datetime

# a= ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar", "foo", "foo", "foo"]
#
# print (a)
# a_array = (a,dtype=object)
# pandas.crosstab(a, [b, c], rownames=['a'], colnames=['b', 'c'])


# >>> b
# array([one, one, one, two, one, one,
#        one, two, two, two, one], dtype=object)
# >>> c
# array([dull, dull, shiny, dull, dull, shiny,
#        shiny, dull, shiny, shiny, shiny], dtype=object)

#https://chrisalbon.com/python/pandas_crosstabs.html
columnar_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons',
                         'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'],
            'company': ['infantry', 'infantry', 'cavalry', 'cavalry', 'infantry', 'infantry', 'cavalry', 'cavalry',
                        'infantry', 'infantry', 'cavalry', 'cavalry'],
            'experience': ['veteran', 'rookie', 'veteran', 'rookie', 'veteran', 'rookie', 'veteran', 'rookie',
                           'veteran', 'rookie', 'veteran', 'rookie'],
            'name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze', 'Jacon', 'Ryaner', 'Sone', 'Sloan', 'Piger',
                     'Riani', 'Ali'],
            'preTestScore': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
            'postTestScore': [25, 94, 57, 62, 70, 25, 94, 57, 62, 70, 62, 70]}
column_names = ['regiment', 'company', 'experience', 'name', 'preTestScore', 'postTestScore']

def get_row_data_list_of_lists():
    col_index = 0

    column_count = len(columnar_data["regiment"])
    #print ("column_count %s" % column_count)
    target_rows = []

    for col in range(0,column_count):
        target_rows.append([])
    # assert(len(target_rows) == 12 )
    # print ("target_rows %s len %s" % (target_rows, len(target_rows)))
    columns = [columnar_data["regiment"], columnar_data["company"],columnar_data["experience"],
              columnar_data["name"],columnar_data["preTestScore"],columnar_data["postTestScore"]]

    # target_row_index = 0
    # target_col_index = 0


    for column in columns:
        source_col_index = 0
        for row in target_rows:
            datum = column[source_col_index]
            row.append(datum)
            source_col_index += 1



    # for row in target_rows:
    #     print ("row %s" % row)
    return target_rows

def get_row_data_list_of_tuple():
    lol = get_row_data_list_of_lists()
    return_rows = []
    for row in lol:
        row_data = tuple(row)
        return_rows.append(row_data)
    return return_rows



def example1():

    df = pandas.DataFrame(columnar_data, columns=column_names)
    print (df)
    print ()

    #Create a crosstab table by company and regiment

    #Counting the number of observations by regiment and category

    result = pandas.crosstab(df.regiment, df.company, margins=True)
    print (result)
    print ()

    #Create a crosstab of the number of rookie and veteran cavalry and infantry soldiers per regiment

    result = pandas.crosstab([df.company, df.experience], df.regiment,  margins=True)
    print (result)

def example2():
    # http://pbpython.com/pandas-list-dict.html
    print ("example2")
    row_data = get_row_data_list_of_tuple()
    #dump("military",row_data, column_names)
    df = pandas.DataFrame.from_records(row_data,columns=column_names)
    print (df)

def dump(descr,obj,column_names):
    print ("dump %s type: %s\n" % (descr, type(obj)))
    print ("column_names %s" % column_names)
    for row in obj:
        print ("type %s row %s" % (type(row),row))

def example3():
    sales = [('Jones LLC', 150, 200, 50),
         ('Alpha Co', 200, 210, 90),
         ('Blue Inc', 140, 215, 95)]
    labels = ['account', 'Jan', 'Feb', 'Mar']
    #dump("sales",sales, labels)
    df = pandas.DataFrame.from_records(sales, columns=labels)
    print (df)

def example4():
    labels =['regiment', 'company', 'experience', 'name', 'preTestScore', 'postTestScore']
    data = [
        ('Nighthawks', 'infantry', 'veteran', 'Miller', 4, 25),
        ('Nighthawks', 'infantry', 'rookie', 'Jacobson', 24, 94),
        ('Nighthawks', 'cavalry', 'veteran', 'Ali', 31, 57),
        ('Nighthawks', 'cavalry', 'rookie', 'Milner', 2, 62),
        ('Dragoons', 'infantry', 'veteran', 'Cooze', 3, 70),
        ('Dragoons', 'infantry', 'rookie', 'Jacon', 4, 25),
        ('Dragoons', 'cavalry', 'veteran', 'Ryaner', 24, 94),
        ('Dragoons', 'cavalry', 'rookie', 'Sone', 31, 57),
        ('Scouts', 'infantry', 'veteran', 'Sloan', 2, 62),
        ('Scouts', 'infantry', 'rookie', 'Piger', 3, 70),
        ('Scouts', 'cavalry', 'veteran', 'Riani', 2, 62),
        ('Scouts', 'cavalry', 'rookie', 'Ali', 3, 70),
    ]
    df = pandas.DataFrame.from_records(data, columns=labels)
    print (df)

def example5():
        print ("example5")
        # http://pbpython.com/pandas-list-dict.html
        labels = ['regiment', 'company', 'experience', 'name', 'preTestScore', 'postTestScore']
        row_data = get_row_data_list_of_tuple()

        #dump("military", row_data, column_names)
        df = pandas.DataFrame.from_records(row_data, columns=labels)
        print(df)


def get_sales_data(*,num_records, num_custs, num_products, date_from, number_of_months):
    import random
    from dateutil.relativedelta import relativedelta
    # number_days = (date_to - date_from)
    # print ("number_days %s" % number_days)
    # #number_of_months = int(number_days / 30) # Close enough, who cares, its fake data
    #
    #
    # number_of_months = relativedelta(date_to, date_from).months
    print ("number of months %s" % number_of_months)
    sales = {}
    rows = []
    for cust_nbr in range(0,num_custs):
        cust_name = "cust " + str(cust_nbr)
        for month_delta in range(0, number_of_months):
            ship_date =  date_from + relativedelta(months=month_delta)
            for product_nbr in (0, num_products):
                product = "product " + str(product_nbr)
                qty = random.randint(0,20)
                if (qty > 0):
                    key = (cust_name,product,ship_date)
                    shipment = (cust_name,product,ship_date,qty)
                    sales[key] = shipment
    for shipment in sales.values():
        rows.append(shipment)
    return rows




def sales_example():
    # https://github.com/pandas-dev/pandas/issues/10947
    labels = ["cust_name","product", "ship_date", "qty" ]
    from_date = datetime.date(2015,1,1)
    to_date = datetime.date(2017,7,1)
    rows = get_sales_data(num_records=3000,num_products=3,date_from=from_date,number_of_months=30, num_custs=1000)
    df =  pandas.DataFrame.from_records(rows, columns=labels)
    print (df)

  #  result = pandas.crosstab([df.cust_name, df.product],df.ship_date, margins=True)
    #result = pandas.crosstab(df.product,df.ship_date, margins=True)

    before =  datetime.datetime.now()
    pivot_table = pandas.pivot_table(df, columns='ship_date', values='qty', index=['cust_name','product'])
    after  = datetime.datetime.now()

    pivoted_records = pivot_table.to_records()


    print (result)
    print("elapsed %s" % (after - before).microseconds)

# example1()
# example3()
# example2()
# example4()
# example5()
sales_example()