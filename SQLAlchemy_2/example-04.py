from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Locker
from secrets import host, user, password

db = 'default'

CONNECTION_STRING = f"mysql+pymysql://{user}:{password}@{host}/{db}"
eng = create_engine(CONNECTION_STRING)

Base.metadata.create_all(eng)

Session = sessionmaker(bind=eng)

s = Session()


try:
    s.add_all([
        Locker(number=1, student=6),
        Locker(number=9, student=1),
        Locker(number=8, student=3),
        Locker(number=6, student=9),
        Locker(number=7, student=11),
        Locker(number=2, student=2),
        Locker(number=11, student=4),
        Locker(number=3, student=10),
        Locker(number=4, student=5),
        Locker(number=5, student=7)
    ])
    s.commit()
except IntegrityError:
    s.rollback()
    print('Lockers already created!')

rows = s.query(Student, Locker).join(Locker).filter(Locker.number == 4)

for row in rows:
    student, locker = row
    print(f"Student with locker #{locker.number}: {student}")
