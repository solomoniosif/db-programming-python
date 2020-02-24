import time
from datetime import datetime
from secrets import host, password, user
import pymysql


def convert_str_to_tmstmp(values):
    values[0] = datetime.strptime(values[0], "%Y-%m-%d %H:%M:%S")
    return values


db = pymysql.connect(host, user, password, "default")

insert_statement = """
INSERT INTO bikesharing(tstamp, cnt, temperature, temperature_feels, humidity, wind_speed, weather_code, is_holiday, is_weekend, season) 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""


def from_csv_to_db(csv_file, cursor):
    with open(csv_file, 'r') as f:
        lines = f.readlines()
        i = 0
        for line in lines[1:]:
            values = convert_str_to_tmstmp(line.split(','))
            cursor.execute(insert_statement, values)
            i += 1
            if i % 100 == 0:
                db.commit()


with db.cursor() as c:
    c._defer_warnings = True
    from_csv_to_db("london-bikes.csv", c)
    db.commit()
db.close()
