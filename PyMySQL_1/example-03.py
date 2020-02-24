import pymysql
from secrets import host, user, password

db = pymysql.connect(host, user, password, "default")
with db.cursor() as c:
    c._defer_warnings = True
    c.execute("CREATE TABLE IF NOT EXISTS `example3` (a integer, b varchar(255));")
    a = int(input("Please provide integer value for a: "))
    b = input("Please provide value for b: ")[:254]
    c.execute("INSERT INTO `example3` (a, b) VALUES (%s, %s);", (a, b))
    db.commit()
db.close()
