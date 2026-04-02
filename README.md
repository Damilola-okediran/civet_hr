# 🧑‍💼 Civet HR System

A full-stack HR management web application built using **Python (Flask)**, designed to manage employees, generate payslips, and handle payroll operations.

This project was built for Civet Solutions Limited.

---

## 🚀 Features

### 👥 Employee Management
- Add new employees
- View employee records
- Delete employees
- Store employee details:
  - Name
  - Email (unique)
  - Phone
  - Role
  - Department
  - Salary
  - Hire date
  - Status

---

### 💰 Payroll & Payslips
- Generate payroll records per employee
- Input:
  - Pay period
  - Basic salary
  - Bonus
  - Deductions
  - Payment date
- Automatically calculates net salary

---

### 📄 PDF Payslip Generation
- Generate downloadable **PDF payslips**
- Includes:
  - Company branding (logo)
  - Employee details
  - Salary breakdown
- Built using `reportlab`

---

### 📊 Payroll History
- View all generated payroll records
- Download payslips anytime
- Track employee salary history

---

### ⚠️ Data Validation
- Prevent duplicate employee emails
- Flash messages for user feedback
- Graceful error handling

---

## 🏗️ Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy

### Database
- SQLite (local development)

### Frontend
- HTML (Jinja Templates)
- CSS

### PDF Generation
- ReportLab

---

## 📁 Project Structure
