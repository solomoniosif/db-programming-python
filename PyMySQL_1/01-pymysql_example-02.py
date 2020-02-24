import pymysql
from password import password

db = pymysql.connect("127.0.0.1", "root", password, "")
with db.cursor() as c:
    c.execute("CREATE SCHEMA IF NOT EXISTS `default` DEFAULT CHARACTER SET utf8;")
db.close()

db = pymysql.connect("127.0.0.1", "root", password, "default")
db.close()
