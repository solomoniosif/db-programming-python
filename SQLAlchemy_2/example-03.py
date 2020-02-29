from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student
from secrets import host, user, password
from sqlalchemy import func


# ! CONNECT TO THE DATABASE
db = 'default'
CONNECTION_STRING = f"mysql+pymysql://{user}:{password}@{host}/{db}"
eng = create_engine(CONNECTION_STRING)

# ! START NEW SESSION
Session = sessionmaker(bind=eng)
s = Session()

# ! QUERIES
rows = s.query(Student).all()
print('-'*40)
print('ALL STUDENTS:')
for row in rows:
    print(row)

print('-'*40)
total = s.query(Student).count()
print(f'TOTAL NUMBER OF STUDENTS: {total}')

print('-'*40)
query_result = s.query(Student).filter(Student.id >= 2,
                                       Student.first_name.like("Jo%"))
print("FOUND STUDENTS:")
for row in query_result:
    print(row)
print('-'*40)

query2 = s.query(Student).filter(Student.last_name.like('%k%'))
print('STUDENT WITH A "k" IN LAST NAME: ')
for row in query2:
    print(row)
print('-'*40)

query3 = s.query(Student).filter(
    Student.first_name.like('S%'), Student.last_name.like('%a%'))
print("ID'S AND LAST NAME OF STUDENTS WITH FIRST NAME STARTING WITH AN 'S' AND WITH AN 'A' IN LAST NAME:")
for row in query3:
    print(row.id, row.last_name)
print('-'*40)

# ! UPDATE
# query4 = s.query(Student).filter(Student.first_name.like('J%')).first()
# query4.last_name = 'Doeee'
# s.commit()

# johns = s.query(Student).filter(Student.first_name == 'Ion')
# for john in johns:
#     john.first_name = 'John'
# s.commit()
