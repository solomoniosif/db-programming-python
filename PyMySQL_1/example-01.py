import pymysql
from secrets import host, user, password

db = pymysql.connect(host, user, password, "")

with db.cursor() as c:
    c.execute("SELECT VERSION()")
    version = c.fetchone()
    print(f'Database version: {version[0]}')
db.close()
