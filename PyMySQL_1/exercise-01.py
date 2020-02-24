import pymysql
from secrets import host, user, password
import time
import datetime

db = pymysql.connect(host, user, password, "default")

create_table_statement = """
    CREATE TABLE IF NOT EXISTS `bikesharing`(
        `tstamp` TIMESTAMP,
        `cnt` INT,
        `temperature` DECIMAL(5,2),
        `temperature_feels` DECIMAL(5,2),
        `humidity` DECIMAL(4,1),
        `wind_speed` DECIMAL(5,2),
        `weather_code` INT,
        `is_holiday` TINYINT,
        `is_weekend` TINYINT,
        `season` INT
    );
"""

with db.cursor() as c:
    c._defer_warnings = True
    c.execute(create_table_statement)
    db.commit()
db.close()

# import time
# import datetime
# ts = time.time()
# timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# insert_statement = """INSERT INTO bikesharing(tstamp, cnt, temperature, temperature_feels, humidity, wind_speed, weather_code, is_holiday, is_weekend, season) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""


# with db.cursor() as c:
#     c._defer_warnings = True
#     c.execute(insert_statement, (timestamp, )
