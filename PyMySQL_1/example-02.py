import pymysql
from secrets import host, user, password
from tabulate import tabulate

# db = pymysql.connect(host, user, password, "")
# with db.cursor() as c:
#     c._defer_warnings = True
#     c.execute("CREATE SCHEMA IF NOT EXISTS `hr` DEFAULT CHARACTER SET utf8;")
# db.close()

db = pymysql.connect(host, user, password, "default")
with db.cursor() as c:
    c._defer_warnings = True
    c.execute("SELECT * FROM default.bikesharing;")
    rows = c.fetchmany(30)

    hdrs = [d[0] for d in c.description]
    print(tabulate(rows, headers=hdrs))

db.close()
