from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student
from secrets import host, user, password

db = 'default'

CONNECTION_STRING = f"mysql+pymysql://{user}:{password}@{host}/{db}"

eng = create_engine(CONNECTION_STRING)

# Base.metadata.create_all(eng)

Session = sessionmaker(bind=eng)

s = Session()

s.add_all([
    Student(first_name='Viktor', last_name='Frankl'),
    Student(first_name='Ellie', last_name='Wiesel'),
    Student(first_name='Stan', last_name='Wawrinka'),
    Student(first_name='Tennys', last_name='Sandgren'),
]
)

s.commit()
