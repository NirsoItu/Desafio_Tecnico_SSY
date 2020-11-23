from sqlalchemy import create_engine, Column, String, Float, Integer, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


# Employees class
class Employees(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    department = Column(String)
    salary = Column(Float, index=True)
    birth_date = Column(String, index=True)

    def __repr__(self):
        return '| Id: {} | Name: {} | Email: {} | Department: {} |' \
               'Salary: {} | Birth Date: {} |\n'.format(self.id, self.name, self.email, self.department, self.salary, self.birth_date)

    # Method to confirm the record of data
    def save(self):
        db_session.add(self)
        db_session.commit()

    # Method to confirm the delete of data
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    # Method to get the average of salary
    def average_salary(self):
        average = Employees.query.with_entities(func.avg(Employees.salary)).all()
        average = str(average).strip('[]').strip('()').strip(',')
        average = float(average)
        average = format(average, '.2f')
        print(average)
        return average

    # Method to get the highest salary
    def highest(self):
        average = Employees.query.with_entities(func.avg(Employees.salary)).all()
        average = str(average).strip('[]').strip('()').strip(',')
        qry = (Employees.query.filter(Employees.salary > average).all())
        print(average, qry)
        return qry

    # Method to get the lowest salary
    def lowest(self):
        average = Employees.query.with_entities(func.avg(Employees.salary)).all()
        average = str(average).strip('[]').strip('()').strip(',')
        qry = (Employees.query.filter(Employees.salary < average).all())
        print(average, qry)
        return qry

    # Method to get the younger
    def younger(self):
        qry = Employees.query.with_entities(Employees.id, Employees.name,
                                            Employees.email, Employees.department,
                                            Employees.salary, Employees.birth_date,
                                            func.max(Employees.birth_date)).all()
        print(qry, type(qry))
        return qry

    # Method to get the older
    def older(self):
        qry = Employees.query.with_entities(Employees.id, Employees.name,
                                            Employees.email, Employees.department,
                                            Employees.salary, Employees.birth_date,
                                            func.min(Employees.birth_date)).all()

        print(qry)
        return qry


# User class for access to app
class Login(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(String(30))

    def __repr__(self):
        return '| Id: {} | Username: {} | Password: {} '.format(self.id, self.username, self.password)

    # Method to confirm the record of data
    def save(self):
        db_session.add(self)
        db_session.commit()

    # Method to confirm the delete of data
    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()