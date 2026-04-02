from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from config import Config
from models import db, Employee, Payroll
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_db')
def create_db():
    with app.app_context():
        db.create_all()
    return "Database and tables created successfully"


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        role_title = request.form['role_title']
        department = request.form['department']
        salary = request.form['salary']
        hire_date = request.form['hire_date']
        status = request.form['status']

        existing_employee = Employee.query.filter_by(email=email).first()

        if existing_employee:
            flash('An employee with this email already exists.')
            return redirect(url_for('add_employee'))

        employee = Employee(
            full_name=full_name,
            email=email,
            phone=phone,
            role_title=role_title,
            department=department,
            salary=float(salary),
            hire_date=hire_date,
            status=status
        )

        db.session.add(employee)
        db.session.commit()

        flash('Employee added successfully.')
        return redirect(url_for('employees'))

    return render_template('add_employee.html')

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    # Delete related payroll records first
    for payroll in employee.payrolls:
        db.session.delete(payroll)

    db.session.delete(employee)
    db.session.commit()

    flash(f'{employee.full_name} was deleted successfully.')
    return redirect(url_for('employees'))

@app.route('/employees')
def employees():
    all_employees = Employee.query.all()
    return render_template('employees.html', employees=all_employees)

@app.route('/create_paystub/<int:employee_id>', methods=['GET', 'POST'])
def create_paystub(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if request.method == 'POST':
        pay_period = request.form['pay_period']
        basic_salary = float(request.form['basic_salary'])
        bonus = float(request.form['bonus'])
        deductions = float(request.form['deductions'])
        payment_date = request.form['payment_date']

        net_salary = basic_salary + bonus - deductions

        payroll = Payroll(
            employee_id=employee.id,
            pay_period=pay_period,
            basic_salary=basic_salary,
            bonus=bonus,
            deductions=deductions,
            net_salary=net_salary,
            payment_date=payment_date
        )

        db.session.add(payroll)
        db.session.commit()

        return redirect(url_for('view_paystub', payroll_id=payroll.id))

    return render_template('create_payroll.html', employee=employee)

@app.route('/paystub/<int:payroll_id>')
def view_paystub(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    return render_template('paystub.html', payroll=payroll)


@app.route('/download_paystub/<int:payroll_id>')
def download_paystub(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Logo path
    logo_path = os.path.join(app.root_path, 'static', 'logo.png')

    # Draw logo if it exists
    if os.path.exists(logo_path):
        pdf.drawImage(logo_path, 40, height - 100, width=60, height=60, preserveAspectRatio=True, mask='auto')

    # Company title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(120, height - 60, "CIVET SOLUTIONS LIMITED")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(120, height - 80, "Employee Payslip")

    # Line separator
    pdf.line(40, height - 110, width - 40, height - 110)

    y = height - 150
    line_gap = 22

    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, y, f"Employee Name: {payroll.employee.full_name}")
    y -= line_gap
    pdf.drawString(40, y, f"Email: {payroll.employee.email}")
    y -= line_gap
    pdf.drawString(40, y, f"Role: {payroll.employee.role_title}")
    y -= line_gap
    pdf.drawString(40, y, f"Department: {payroll.employee.department}")
    y -= line_gap
    pdf.drawString(40, y, f"Pay Period: {payroll.pay_period}")
    y -= line_gap
    pdf.drawString(40, y, f"Basic Salary: N{payroll.basic_salary:,.2f}")
    y -= line_gap
    pdf.drawString(40, y, f"Bonus: N{payroll.bonus:,.2f}")
    y -= line_gap
    pdf.drawString(40, y, f"Deductions: N{payroll.deductions:,.2f}")
    y -= line_gap
    pdf.drawString(40, y, f"Net Salary: N{payroll.net_salary:,.2f}")
    y -= line_gap
    pdf.drawString(40, y, f"Payment Date: {payroll.payment_date}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=payslip_{payroll.id}.pdf'

    return response

@app.route('/payroll_history')
def payroll_history():
    payrolls = Payroll.query.order_by(Payroll.id.desc()).all()
    return render_template('payroll_history.html', payrolls=payrolls)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
