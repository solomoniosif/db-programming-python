from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Locker, Address, Grades
from secrets import host, user, password
from datetime import datetime
from sqlalchemy import func

db = 'default'

CONNECTION_STRING = f"mysql+pymysql://{user}:{password}@{host}/{db}"
eng = create_engine(CONNECTION_STRING)
Base.metadata.create_all(eng)
Session = sessionmaker(bind=eng)

s = Session()

######################################
# ADD ADDRESSES TO STUDENTS
######################################

try:
    s.add_all([
        Address(student=1, street_name='Eroilor 68',
                number=1, city='Floresti'),
        Address(student=2, street_name='Long Beach 38',
                number=2, city='Florida'),
        Address(student=3, street_name='W. Gheote 4', number=3, city='Miami'),
        Address(student=4, street_name='Long Street 54',
                number=5, city='Oagadougou'),
        Address(student=5, street_name='Queen Mary 3',
                number=7, city='Mohadishu'),
        Address(student=6, street_name='No street 37',
                number=4, city='Kinshasa'),
        Address(student=7, street_name='Muda Max 332', number=6, city='Paris'),
        Address(student=8, street_name='Eisenhower 68',
                number=9, city='London'),
        Address(student=9, street_name='Wienner Strasse 34',
                number=8, city='Stutgart'),
        Address(student=10, street_name='Karl Straus 68',
                number=10, city='Berlin'),
        Address(student=11, street_name='Street fdjvbid 34',
                number=12, city='Budapest'),
        Address(student=12, street_name='Kalimera 18',
                number=11, city='Athens'),
        Address(student=13, street_name='Coloseum Street 628',
                number=13, city='Rome')
    ])
    s.commit()
except IntegrityError:
    s.rollback()
    print('Addresses already added!')


######################################
# ADD GRADES TO STUDENTS
######################################

# s.add_all([
#     Grades(student=1, grade=9, date_created=datetime.now()),
#     Grades(student=2, grade=1, date_created=datetime.now()),
#     Grades(student=3, grade=4, date_created=datetime.now()),
#     Grades(student=4, grade=9, date_created=datetime.now()),
#     Grades(student=5, grade=9, date_created=datetime.now()),
#     Grades(student=6, grade=2, date_created=datetime.now()),
#     Grades(student=7, grade=1, date_created=datetime.now()),
#     Grades(student=8, grade=2, date_created=datetime.now()),
#     Grades(student=9, grade=1, date_created=datetime.now()),
#     Grades(student=10, grade=1, date_created=datetime.now()),
#     Grades(student=11, grade=1, date_created=datetime.now()),
#     Grades(student=12, grade=2, date_created=datetime.now()),
#     Grades(student=13, grade=7, date_created=datetime.now()),
#     Grades(student=14, grade=1, date_created=datetime.now()),
#     Grades(student=15, grade=5, date_created=datetime.now()),
#     Grades(student=16, grade=3, date_created=datetime.now())
# ])
# s.commit()


# ! QUERY 1
rows = s.query(Student, Address).join(Address).all()

print('-----------------\n   QUERY 1 : \n-----------------')
for row in rows:
    student, address = row
    print(f"Student {student.first_name} {student.last_name} lives at address: {address.street_name} in {address.city}")


# ! QUERY 2
rows2 = s.query(Student, Locker, Address).join(Locker).join(Address).all()

print('-----------------\n   QUERY 2 : \n-----------------')
for row in rows2:
    student, locker, address = row
    print(
        f'Student {student.first_name} with locker #{locker.number} living in {address.city}')


# ! QUERY 3
q3 = s.query(Student, Locker, Address).join(Locker).join(Address).filter(
    Student.id > 3, Locker.number > 3, Address.number > 3)

print('-----------------\n   QUERY 3 : \n-----------------')
for row in q3:
    student, locker, address = row
    print(
        f"Student #{student.id} with locker #{locker.number} living at address #{address.number}")


# ! QUERY 4
q4 = s.query(Student, Locker, Address).join(Locker).join(Address).filter(
    Student.first_name.like('J%')).order_by(Locker.number.desc()).limit(2)

print('-----------------\n   QUERY 4 : \n-----------------')
for row in q4:
    student, locker, address = row
    print(
        f"Student {student.first_name} living in {address.city} with locker #{locker.number}")


# ! UPDATE 1
# student, address = s.query(Student, Address).join(
#     Address).filter(Student.first_name == 'Jordan').first()


# print(student.first_name, address.city)
# address.city = 'Toronto'
# print(student.first_name, address.city)
# s.commit()

# ! UPDATE 2
# student, address = s.query(Student, Address).join(
#     Address).filter(Student.first_name == 'Jordan').first()

# print(address.street_name)
# address.street_name = 'Saskatchewan 12'
# print(address.street_name)
# s.commit()

# ! QUERY 5
q5 = s.query(Student, Grades).join(Grades).all()

print('-----------------\n   QUERY 5 : \n-----------------')
for row in q5:
    student, grade = row
    print(f"{student.first_name} {student.last_name} with grade {grade.id}: {grade.grade}")


# ! DELETE 1
# q6 = s.query(Grades).filter(Grades.id > 16).all()

# print('-----------------\n   QUERY 6 : \n-----------------')
# for row in q6:
#     s.delete(row)
# s.commit()

# ! QUERY 7
sq = s.query(func.avg(Grades.grade), Student).filter(
    func.avg(Grades.grade) > 5).label('medie')
q7 = s.query(Student, func.avg(Grades.grade)).join(
    Grades).group_by(Grades.student).order_by(func.avg(Grades.grade).desc())

print('-----------------\n   QUERY 7 : \n-----------------')
for row in q7:
    student, avg_grade = row
    avg_grade = round(avg_grade, 1)
    if avg_grade > 3:
        print(
            f'{student.first_name} {student.last_name} with grade average of {avg_grade}')
