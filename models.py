from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role_title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    salary = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default='Active')

    def __repr__(self):
        return f'<Employee {self.full_name}>'

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    pay_period = db.Column(db.String(50), nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    deductions = db.Column(db.Float, nullable=False, default=0.0)
    bonus = db.Column(db.Float, nullable=False, default=0.0)
    net_salary = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.String(50), nullable=False)

    employee = db.relationship('Employee', backref='payrolls')

    def __repr__(self):
        return f'<Payroll {self.id} - Employee {self.employee_id}>'
