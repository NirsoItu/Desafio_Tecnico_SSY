from flask import Flask, request
from flask_restful import Resource, Api
from models import Employees, Users
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


# Method to confirm the access permission to app
@auth.verify_password
def verify_password(username, password):
    print('User validating')
    print(Users.query.filter_by(username=username, password=password).first())
    if not (username, password):
        return False
    return Users.query.filter_by(username=username, password=password).first()

# Methods from Employee class
class Employee(Resource):
    @auth.login_required
    # Method GET that return employee by ID
    def get(self, id):
        employee = Employees.query.filter_by(id=id).first()
        try:
            response = {
                'id':employee.id,
                'name':employee.name,
                'email': employee.email,
                'department': employee.department,
                'salary': employee.salary,
                'birth_date': employee.birth_date
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Employee not found'
            }
        return response

    @auth.login_required
    # Method PUT that allows modify the employee by ID
    def put(self, id):
        employee = Employees.query.filter_by(id=id).first()
        try:
            data = request.json
            if 'name' in data:
                employee.name = data['name']
            if 'email' in data:
                employee.email = data['email']
            if 'department' in data:
                employee.department = data['department']
            if 'salary' in data:
                employee.salary = data['salary']
            if 'birth_date' in data:
                employee.birth_date = data['birth_date']
                employee.save()
                response = {'message':'Employee {} successfully modified!'.format(employee.id),
                    'id':employee.id,
                    'name': employee.name,
                    'email': employee.email,
                    'department': employee.department,
                    'salary': employee.salary,
                    'birth_date': employee.birth_date
                }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Employee not found'
            }

        return response

    @auth.login_required
    # Method DELETE that delete the employee by ID
    def delete(self, id):
        employee = Employees.query.filter_by(id=id).first()
        verify = bool(Employees.query.filter_by(id=id).first())
        if not(verify):
            return {'message':'Employee not found !'}
        else:
            employee.delete()
            return {'message':'Employee was deleted'}


class ListEmployees(Resource):
    @auth.login_required
    # Method GET that return all employees
    def get(self):
        employees = Employees.query.all()
        response = [{'id':i.id, 'name':i.name,'email':i.email,
                     'department':i.department,'salary':format(i.salary, '.2f'),'birth_date':(i.birth_date)
                     }for i in employees]
        return response

    @auth.login_required
    # Method POST to create a new employee
    def post(self):
        try:
            data = request.json
            employee = Employees(name=data['name'], email=data['email'],
                                 department=data['department'], salary=data['salary'],
                                 birth_date=data['birth_date'])
            employee.save()
            response = {'message':'Employee {} was created successfully'.format(employee.id),
                    'id':employee.id,
                    'name': employee.name,
                    'email': employee.email,
                    'department': employee.department,
                    'salary': employee.salary,
                    'birth_date': employee.birth_date
                }
        except KeyError:
            response = {
                'status': 'error',
                'message': 'API error, consult the administrator'
            }
        return response

class ReportSalary(Resource):
    @auth.login_required
    # Method GET that return salary report
    def get(self):
        employees_highest = Employees.highest(Employees.salary)
        employees_lowest = Employees.lowest(Employees.salary)
        average = Employees.average_salary(Employees.salary)
        response = {"lowest":[{
            'id': i.id,
            'name': i.name,
            'email': i.email,
            'department': i.department,
            'salary': format(i.salary,'.2f'),
            'birth_date': i.birth_date} for i in employees_lowest],
            "highest": [{
                'id': i.id,
                'name': i.name,
                'email': i.email,
                'department': i.department,
                'salary': format(i.salary, '.2f'),
                'birth_date': i.birth_date} for i in employees_highest],
            "average": [{'average': average}]
        }
        return response

class ReportAge(Resource):
    @auth.login_required
    # Method GET that return age report
    def get(self):
        employees_younger = Employees.younger(Employees.birth_date)
        employees_older = Employees.older(Employees.birth_date)
        response = {"younger":[{
            'id': i.id,
            'name': i.name,
            'email': i.email,
            'department': i.department,
            'salary': format(i.salary,'.2f'),
            'birth_date': i.birth_date
            } for i in employees_younger],
            "older": [{
                'id': i.id,
                'name': i.name,
                'email': i.email,
                'department': i.department,
                'salary': format(i.salary, '.2f'),
                'birth_date': i.birth_date
                } for i in employees_older],
            "average": {'average': '40'}
        }
        return response

api.add_resource(Employee,'/employees/<int:id>')
api.add_resource(ListEmployees,'/employees/')
api.add_resource(ReportSalary,'/employees/salary/')
api.add_resource(ReportAge,'/employees/age/')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)