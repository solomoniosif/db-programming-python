import pymysql
import datetime
from secrets import host, user, password
from tabulate import tabulate

db = pymysql.connect(host, user, password, "default")
with db.cursor() as c:
    c.execute(
        "SELECT tstamp,cnt FROM bikesharing WHERE tstamp BETWEEN %s AND %s",
        (datetime.datetime(2016, 1, 1, 0), datetime.datetime(2016, 1, 1, 5)),
    )
    print(f"Column names: {[d[0] for d in c.description]}")
    # print(c.fetchone())  # first row
    print('-'*26)
    rows = c.fetchall()  # remaining rows
    headers = [d[0] for d in c.description]
    print(tabulate(rows, headers))
    print('-'*26)
    print(f"Got {c.rowcount} rows")
    for d in c.description:
        print(d)
db.close()
