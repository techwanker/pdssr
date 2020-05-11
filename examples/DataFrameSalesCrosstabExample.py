import pandas
import datetime
import logging
import time

logging.basicConfig(level=logging.INFO)


#
# # a= ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar", "foo", "foo", "foo"]
# #
# # print (a)
# # a_array = (a,dtype=object)
# # pandas.crosstab(a, [b, c], rownames=['a'], colnames=['b', 'c'])
#
#
# # >>> b
# # array([one, one, one, two, one, one,
# #        one, two, two, two, one], dtype=object)
# # >>> c
# # array([dull, dull, shiny, dull, dull, shiny,
# #        shiny, dull, shiny, shiny, shiny], dtype=object)
#
# #https://chrisalbon.com/python/pandas_crosstabs.html
# columnar_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons',
#                          'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'],
#             'company': ['infantry', 'infantry', 'cavalry', 'cavalry', 'infantry', 'infantry', 'cavalry', 'cavalry',
#                         'infantry', 'infantry', 'cavalry', 'cavalry'],
#             'experience': ['veteran', 'rookie', 'veteran', 'rookie', 'veteran', 'rookie', 'veteran', 'rookie',
#                            'veteran', 'rookie', 'veteran', 'rookie'],
#             'name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze', 'Jacon', 'Ryaner', 'Sone', 'Sloan', 'Piger',
#                      'Riani', 'Ali'],
#             'preTestScore': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
#             'postTestScore': [25, 94, 57, 62, 70, 25, 94, 57, 62, 70, 62, 70]}
# column_names = ['regiment', 'company', 'experience', 'name', 'preTestScore', 'postTestScore']
#
# def get_row_data_list_of_lists():
#     col_index = 0
#
#     column_count = len(columnar_data["regiment"])
#     #print ("column_count %s" % column_count)
#     target_rows = []
#
#     for col in range(0,column_count):
#         target_rows.append([])
#     # assert(len(target_rows) == 12 )
#     # print ("target_rows %s len %s" % (target_rows, len(target_rows)))
#     columns = [columnar_data["regiment"], columnar_data["company"],columnar_data["experience"],
#               columnar_data["name"],columnar_data["preTestScore"],columnar_data["postTestScore"]]
#
#     # target_row_index = 0
#     # target_col_index = 0
#
#
#     for column in columns:
#         source_col_index = 0
#         for row in target_rows:
#             datum = column[source_col_index]
#             row.append(datum)
#             source_col_index += 1
#
#
#
#     # for row in target_rows:
#     #     print ("row %s" % row)
#     return target_rows
#
# def get_row_data_list_of_tuple():
#     lol = get_row_data_list_of_lists()
#     return_rows = []
#     for row in lol:
#         row_data = tuple(row)
#         return_rows.append(row_data)
#     return return_rows
#
#
#
# def example1():
#
#     df = pandas.DataFrame(columnar_data, columns=column_names)
#     print (df)
#     print ()
#
#     #Create a crosstab table by company and regiment
#
#     #Counting the number of observations by regiment and category
#
#     result = pandas.crosstab(df.regiment, df.company, margins=True)
#     print (result)
#     print ()
#
#     #Create a crosstab of the number of rookie and veteran cavalry and infantry soldiers per regiment
#
#     result = pandas.crosstab([df.company, df.experience], df.regiment,  margins=True)
#     print (result)
#
# def example2():
#     # http://pbpython.com/pandas-list-dict.html
#     print ("example2")
#     row_data = get_row_data_list_of_tuple()
#     #dump("military",row_data, column_names)
#     df = pandas.DataFrame.from_records(row_data,columns=column_names)
#     print (df)
#
# def dump(descr,obj,column_names):
#     print ("dump %s type: %s\n" % (descr, type(obj)))
#     print ("column_names %s" % column_names)
#     for row in obj:
#         print ("type %s row %s" % (type(row),row))
#
# def example3():
#     sales = [('Jones LLC', 150, 200, 50),
#          ('Alpha Co', 200, 210, 90),
#          ('Blue Inc', 140, 215, 95)]
#     labels = ['account', 'Jan', 'Feb', 'Mar']
#     #dump("sales",sales, labels)
#     df = pandas.DataFrame.from_records(sales, columns=labels)
#     print (df)
#
# def example4():
#     labels =['regiment', 'company', 'experience', 'name', 'preTestScore', 'postTestScore']
#     data = [
#         ('Nighthawks', 'infantry', 'veteran', 'Miller', 4, 25),
#         ('Nighthawks', 'infantry', 'rookie', 'Jacobson', 24, 94),
#         ('Nighthawks', 'cavalry', 'veteran', 'Ali', 31, 57),
#         ('Nighthawks', 'cavalry', 'rookie', 'Milner', 2, 62),
#         ('Dragoons', 'infantry', 'veteran', 'Cooze', 3, 70),
#         ('Dragoons', 'infantry', 'rookie', 'Jacon', 4, 25),
#         ('Dragoons', 'cavalry', 'veteran', 'Ryaner', 24, 94),
#         ('Dragoons', 'cavalry', 'rookie', 'Sone', 31, 57),
#         ('Scouts', 'infantry', 'veteran', 'Sloan', 2, 62),
#         ('Scouts', 'infantry', 'rookie', 'Piger', 3, 70),
#         ('Scouts', 'cavalry', 'veteran', 'Riani', 2, 62),
#         ('Scouts', 'cavalry', 'rookie', 'Ali', 3, 70),
#     ]
#     df = pandas.DataFrame.from_records(data, columns=labels)
#     print (df)
#
# def example5():
#         print ("example5")
#         # http://pbpython.com/pandas-list-dict.html
#         labels = ['regiment', 'company', 'experience', 'name', 'preTestScore', 'postTestScore']
#         row_data = get_row_data_list_of_tuple()
#
#         #dump("military", row_data, column_names)
#         df = pandas.DataFrame.from_records(row_data, columns=labels)
#         print(df)


def get_sales_data(*, num_records, num_custs, num_products, date_from, number_of_months):
    import random
    from dateutil.relativedelta import relativedelta
    # number_days = (date_to - date_from)
    # print ("number_days %s" % number_days)
    # #number_of_months = int(number_days / 30) # Close enough, who cares, its fake data
    #
    #
    # number_of_months = relativedelta(date_to, date_from).months
    print("number of months %s" % number_of_months)
    sales = {}
    rows = []
    for cust_nbr in range(0, num_custs):
        cust_name = "cust " + str(cust_nbr)
        for month_delta in range(0, number_of_months):
            ship_date = date_from + relativedelta(months=month_delta)
            for product_nbr in (0, num_products):
                product = "product " + str(product_nbr)
                qty = random.randint(0, 20)
                if (qty > 0):
                    key = (cust_name, product, ship_date)
                    shipment = (cust_name, product, ship_date, qty)
                    sales[key] = shipment
    for shipment in sales.values():
        rows.append(shipment)
    return rows


def sales_example():
    # https://github.com/pandas-dev/pandas/issues/10947
    labels = ["cust_name", "product", "ship_date", "qty"]
    from_date = datetime.date(2015, 1, 1)
    to_date = datetime.date(2017, 7, 1)
    rows = get_sales_data(num_records=3000, num_products=3, date_from=from_date, number_of_months=30, num_custs=1000)
    df = pandas.DataFrame.from_records(rows, columns=labels)
    print(df)
    #  result = pandas.crosstab([df.cust_name, df.product],df.ship_date, margins=True)
    # result = pandas.crosstab(df.product,df.ship_date, margins=True)

    before = datetime.datetime.now()
    result = pandas.pivot_table(df, columns='ship_date', values='qty', index=['cust_name', 'product'])
    after = datetime.datetime.now()

    print(result)
    print("elapsed %s" % (after - before).microseconds)
    print(result.to_csv())


def sales_pivot_from_sql():
    from pdsutil.DbUtil import ConnectionHelper
    sql = "select * from etl_sale where etl_file_id = %(ETL_FILE_ID)s"
    parms = {"ETL_FILE_ID": 201723}
    connection = ConnectionHelper().get_named_connection("current")
    df = pandas.read_sql(sql, connection, params=parms)
    print(df)
    result = pandas.pivot_table(df, columns='ship_dt', values='cases_shipped',
                                index=['ship_to_cust_id', 'product_descr'])
    print("pivot %s\n" % result)


def set_column_widths(worksheet, dataframe):
    logger = logging.getLogger(__name__ + ":set_column_widths")
    # Given a dict of dataframes, for example:
    # dfs = {'gadgets': df_gadgets, 'widgets': df_widgets}

    # writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    # for sheetname, df in dfs.items():  # loop through `dict` of dataframes
    #     df.to_excel(writer, sheet_name=sheetname)  # send df to writer
    #     worksheet = writer.sheets[sheetname]  # pull worksheet object

    for idx, col in enumerate(dataframe):  # loop through all columns
        series = dataframe[col]
        row_idx = 0
        for v in series:
            if row_idx < 10:
                #    print ("idx %s row_idx %s val %s" % (idx,row_idx,v ))
                row_idx += 1
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
        )) + 1  # adding a little extra space
        # logger.info("setting column %s to width %s" % (idx, max_len))
        worksheet.set_column(idx, idx, max_len)  # set column width
        # writer.save()


def log_time(descr, begin, end):
    msg = ("descr: %s, begin %s, end %s, diff %s " %
           (descr, begin, end, end - begin))
    print(msg)


def to_excel(workbook, sheetname, dataframe):
    max_widths = None
    import math
    worksheet = workbook.add_worksheet(sheetname)
    row_index = 1
    for row in dataframe:
        max_widths = [None] * len(row)
        col_index = 0
        for datum in row:
            if datum is not None:
                if isinstance(datum, float):
                    if not math.isnan(datum):
                        worksheet.write(row_index, col_index, datum)
                else:
                    worksheet.write(row_index, col_index, datum)
                # print ("len(max_widths) %s col_index %s " % (len(max_widths),col_index))
                if max_widths[col_index] is None or len(str(datum)) > max_widths[col_index]:
                    max_widths[col_index] = len(str(datum))
            if row_index < 5:
                print("r: %s c: %s %s" % (row_index, col_index, datum))
            col_index += 1
        row_index += 1

        col_index = 0
        for width in max_widths:
            worksheet.set_column(col_index, col_index, width + 1)
            col_index += 1


def sales_pivot_from_sql_by_month():
    full_begin = time.time()

    # Given a dict of dataframes, for example:
    # dfs = {'gadgets': df_gadgets, 'widgets': df_widgets}

    # writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    # for sheetname, df in dfs.items():  # loop through `dict` of dataframes
    #     df.to_excel(writer, sheet_name=sheetname)  # send df to writer
    #     worksheet = writer.sheets[sheetname]  # pull worksheet object
    #     for idx, col in enumerate(df):  # loop through all columns
    #         series = df[col]
    #         max_len = max((
    #             series.astype(str).map(len).max(),  # len of largest item
    #             len(str(series.name))  # len of column name/header
    #         )) + 1  # adding a little extra space
    #         worksheet.set_column(idx, idx, max_len)  # set column width
    # writer.save()


    from pdsutil.DbUtil import ConnectionHelper
    sql = "select * from etl_cust_product_month_mv where sum_cases_shipped > 0"
    parms = {"ETL_FILE_ID": 201723}
    connection = ConnectionHelper().get_named_connection("current")
    before_query = time.time()
    df = pandas.read_sql(sql, connection, params=parms)
    after_query = time.time()

    # print (df)
    pivot_df = pandas.pivot_table(df, columns='ship_month', values='sum_cases_shipped',
                                  index=['ship_to_cust_id', 'product_descr'])
    print("pivot_df index %s" % pivot_df.index.name)
    after_pivot = time.time()
    # print("pivot %s\n" % pivot_df)

    row_count = 0
    # for row in pivot_df.iterrows():
    #     row_length = len(row)
    #     print ("row len %s data %s" % (row_length, str(row)))
    #     row_count += 1
    #     if row_count > 9:
    #         break;

    #  TODO http://stackoverflow.com/questions/17241004/pandas-how-to-get-the-data-frame-index-as-an-array set index_columns


    before_to_excel = time.time()
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pandas.ExcelWriter('/tmp/all_sales_pivot.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    sheet_name = "All Sales"
    pivot_df.to_excel(writer, sheet_name=sheet_name)
    worksheet = writer.sheets[sheet_name]
    # set_columnm_widths(worksheet,pivot_df)
    to_csv_begin = time.time()

    import io
    output = io.StringIO()
    pivot_df.to_csv(output)
    to_csv_end = time.time()

    to_record_begin = time.time()
    records = pivot_df.to_records()
    to_record_end = time.time()
    ###

    to_excel_internal_start = time.time()
    import xlsxwriter
    output = open("/tmp/crosstab.xslx", "wb")
    workbook = xlsxwriter.Workbook(output)
    to_excel(workbook, "wank", records)
    workbook.close()
    to_excel_internal_end = time.time()

    writer.save()
    after_excel = time.time()
    full_end = time.time()
    log_time("query", before_query, after_query)
    log_time("pivot", after_query, after_pivot)
    log_time("to_excel", before_to_excel, after_excel)
    log_time("to_csv", to_csv_begin, to_csv_end)
    log_time("to_records", to_record_begin, to_record_end)
    log_time("internal to_excel", to_excel_internal_start, to_excel_internal_end)
    log_time("full time", full_begin, full_end)


# example1()
# example3()
# example2()
# example4()
# example5()
# sales_example()
# sales_pivot_from_sql()
sales_pivot_from_sql_by_month()
