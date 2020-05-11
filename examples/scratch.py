from pdsutil.DbUtil import ConnectionHelper, CursorHelper
import sqlite3

sql = """
insert into org_mfr(org_id,cds_mfr_id) 
select org_id,  %(CDS_MFR_ID)s
from   org 
where org_cd = %(ORG_CD)s
"""

binds = {
    "CDS_MFR_ID": "0000000020",
    "ORG_CD": "F-L",
    "ORG_NM": "Frito-Lay"
}

connection =sqlite3.Connection("/tmp/wtf.dbf")
cursor = CursorHelper(connection.cursor())

cursor.execute(
                "insert into org (org_cd, org_nm) "
                "values (%(ORG_CD)s, %(ORG_NM)s)",
                binds)

cursor.execute(sql,binds)

sql = "select * from org_mfr"
rows = cursor.execute(sql)
for row in rows:
    print (row)