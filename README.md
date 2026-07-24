# 🏢 HR Management System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.x-green?logo=django)
![Django REST Framework](https://img.shields.io/badge/Django_REST-Framework-red)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF?logo=vite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap)
![Axios](https://img.shields.io/badge/Axios-HTTP-5A29E4?logo=axios)
![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens&logoColor=white)
![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

# 📖 Overview

The **HR Management System** is a secure, full-stack web application developed using **React**, **Django REST Framework**, **JWT Authentication**, and **MySQL** to automate and simplify daily Human Resource operations.

The application provides separate dashboards for **HR Administrators** and **Employees**, ensuring secure role-based access to employee information, attendance management, leave management, payroll processing, reports, calendars, and profile management.

The system minimizes manual paperwork, improves data accuracy, and provides a centralized platform for managing organizational HR activities.

---

# ✨ Features

## 🔐 Authentication

- Secure Login
- JWT Authentication
- Role-Based Authorization
- Protected REST APIs
- Secure Logout

---

## 👨‍💼 Employee Management (HR)

- Add Employee
- Update Employee
- Delete Employee
- Employee Directory
- Employee Details
- Employee Reports

---

## 🕒 Attendance Management

### HR

- Mark Attendance
- Update Attendance
- Attendance List
- Attendance Report

### Employee

- Mark Daily Attendance
- View Attendance History

---

## 📝 Leave Management

### HR

- View Leave Requests
- Approve Leave
- Reject Leave
- Leave Reports

### Employee

- Apply Leave
- Update Leave Request
- Leave History

---

## 💰 Payroll Management

### HR

- Generate Payroll
- Update Payroll
- Payroll List
- Payroll Reports
- Generate Payslip

### Employee

- View Payroll History
- View Payslip
- Download Payslip

---

## 📊 Dashboards

### HR Dashboard

- Employee Statistics
- Attendance Summary
- Leave Summary
- Payroll Summary

### Employee Dashboard

- Attendance Overview
- Leave Overview
- Payroll Overview
- Quick Access Modules

---

## 📄 Reports

- Employee Report
- Attendance Report
- Leave Report
- Payroll Report

---

## 📅 Calendar

- Attendance Calendar
- Leave Calendar

---

## 👤 Profile

- View Profile
- Update Profile

---

## 🌙 User Interface

- Responsive Design
- Modern UI
- Bootstrap Components
- Dark Theme
- Mobile Friendly

---

# 🖼️ Application Screenshots

## Login

<p align="center">
<img src="images/Login.png" width="700">
</p>

---

## HR Dashboard

<p align="center">
<img src="images/HR Dashboard.png" width="700">
</p>

---

## Employee Dashboard

<p align="center">
<img src="images/Employee Dashboard.png" width="700">
</p>

---

## Employee Management

<p align="center">
<img src="images/Employee Form.png" width="700">
</p>

<p align="center">
<img src="images/Employee List.png" width="700">
</p>

<p align="center">
<img src="images/Employee Report.png" width="700">
</p>

---

## Attendance Management

<p align="center">
<img src="images/Attendance Form.png" width="700">
</p>

<p align="center">
<img src="images/Attendance List.png" width="700">
</p>

<p align="center">
<img src="images/Attendance Report.png" width="700">
</p>

---

## Leave Management

<p align="center">
<img src="images/Leave Request Form.png" width="700">
</p>

<p align="center">
<img src="images/Leave Req Report.png" width="700">
</p>

---

## Payroll Management

<p align="center">
<img src="images/Payroll Form.png" width="700">
</p>

<p align="center">
<img src="images/Payroll List.png" width="700">
</p>

<p align="center">
<img src="images/Payroll Report.png" width="700">
</p>

<p align="center">
<img src="images/Payslip.png" width="700">
</p>

---

## Calendar

<p align="center">
<img src="images/Calendar.png" width="700">
</p>

---

## Request Dashboard

<p align="center">
<img src="images/Request Dashboard.png" width="700">
</p>

<p align="center">
<img src="images/Request List.png" width="700">
</p>

---

## Profile

<p align="center">
<img src="images/Profile.png" width="700">
</p>

---

## Dark Theme

<p align="center">
<img src="images/Dark theme.png" width="700">
</p>

---

# ⚙️ Technology Stack

## Frontend

- React 18
- Vite
- Bootstrap 5
- Axios
- React Router
- HTML5
- CSS3
- JavaScript (ES6+)

## Backend

- Python 3.12+
- Django 6.x
- Django REST Framework
- JWT Authentication
- WhiteNoise
- Gunicorn

## Database

- MySQL

## Development Tools

- Git
- GitHub
- VS Code
- Postman

---

# 🔄 System Workflow

```text
                     START
                       │
                       ▼
              User Opens Application
                       │
                       ▼
                  Login Page
                       │
                       ▼
            Username & Password
                       │
                       ▼
             JWT Authentication
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
   HR Administrator             Employee
         │                           │
         ▼                           ▼
   HR Dashboard             Employee Dashboard
         │                           │
         ├── Employee Management     ├── Attendance
         ├── Attendance              ├── Leave
         ├── Leave                   ├── Payroll
         ├── Payroll                 ├── Calendar
         ├── Reports                 ├── Profile
         ├── Calendar                │
         └── Profile                 │
                       │
                       ▼
                    Logout
                       │
                       ▼
                      END
```

---

# 🏗️ System Architecture

```text
               React Frontend
                      │
                      ▼
           Axios HTTP Requests
                      │
                      ▼
          JWT Authentication Layer
                      │
                      ▼
        Django REST Framework APIs
                      │
                      ▼
              Business Logic Layer
                      │
        ├── Accounts Module
        ├── Dashboard Module
        ├── Employees Module
        ├── Attendance Module
        ├── Leave Module
        ├── Payroll Module
        └── Reports Module
                      │
                      ▼
               MySQL Database
```

---

# 📂 Project Structure

```text
HR-Management-System/
│
├── backend/
│   ├── accounts/
│   ├── attendance/
│   ├── dashboard/
│   ├── employees/
│   ├── leave/
│   ├── payroll/
│   ├── reports/
│   ├── config/
│   ├── media/
│   ├── static/
│   ├── templates/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── .env.example
│   └── .gitignore
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── images/
├── README.md
└── .gitignore
```

---
# ⚙️ Installation

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.12+
- Node.js 18+
- npm
- MySQL 8+
- Git

---

## Clone Repository

```bash
git clone https://github.com/sudhakaran1401/HR-Management-System.git

cd HR-Management-System
```

---

# 🐍 Backend Setup

Navigate to the backend folder.

```bash
cd backend
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Copy the example environment file.

### Windows

```cmd
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Open `.env` and configure the following values.

```env
SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.mysql
DB_NAME=HRMS
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173

SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

---

## Apply Database Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## Run Backend

```bash
python manage.py runserver
```

Backend URL

```
http://127.0.0.1:8000/
```

---

# ⚛️ Frontend Setup

Open another terminal.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Run the development server.

```bash
npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

# 🚀 Production Deployment

## Backend

Start Gunicorn.

```bash
gunicorn config.wsgi:application
```

Or using the Procfile.

```text
web: gunicorn config.wsgi:application
```

---

## Environment Variables

Set the following variables on your hosting platform.

```env
DEBUG=False

ALLOWED_HOSTS=your-domain.com

CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com

SESSION_COOKIE_SECURE=True

CSRF_COOKIE_SECURE=True

SECURE_SSL_REDIRECT=True

SECURE_HSTS_SECONDS=31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS=True

SECURE_HSTS_PRELOAD=True
```

---

## Supported Platforms

- Railway
- Render
- Koyeb
- AWS
- Azure
- DigitalOcean
- Hostinger VPS
- Ubuntu VPS (Nginx + Gunicorn)

---

# 📖 API Documentation

After running the backend, the API documentation is available at:

### Swagger UI

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

### ReDoc

```
http://127.0.0.1:8000/api/schema/redoc/
```

### OpenAPI Schema

```
http://127.0.0.1:8000/api/schema/
```

---

# 📦 Core Modules

## 👨‍💼 Employee Management

- Add Employee
- Update Employee
- Delete Employee
- Employee Directory
- Employee Reports

---

## 🕒 Attendance Management

### HR

- Mark Attendance
- Attendance Reports
- Attendance History

### Employee

- Daily Attendance
- Attendance History

---

## 📝 Leave Management

### HR

- View Leave Requests
- Approve Leave
- Reject Leave
- Leave Reports

### Employee

- Apply Leave
- Update Leave
- Leave History

---

## 💰 Payroll Management

### HR

- Generate Payroll
- Update Payroll
- Payroll Reports
- Generate Payslip

### Employee

- Payroll History
- View Payslip
- Download Payslip

---

## 📊 Dashboard

- HR Dashboard
- Employee Dashboard
- Request Dashboard

---

## 📅 Calendar

- Attendance Calendar
- Leave Calendar

---

## 👤 Profile

- View Profile
- Update Profile

---

## 📄 Reports

- Employee Reports
- Attendance Reports
- Leave Reports
- Payroll Reports

---

# 🔐 Security

The application implements multiple security mechanisms.

- JWT Authentication
- Role-Based Authorization
- Protected REST APIs
- Password Hashing
- CSRF Protection
- CORS Protection
- Secure Cookies
- WhiteNoise Static File Serving
- Environment Variable Configuration

---

# 📈 Future Enhancements

- Email Notifications
- Real-Time Notifications
- Biometric Attendance Integration
- Docker Support
- Kubernetes Deployment
- AWS Deployment
- Azure Deployment
- Mobile Application
- AI-powered HR Analytics

---

# 👨‍💻 Author

## Sudha Karan

**Python Full Stack Developer**

GitHub

```
https://github.com/sudhakaran1401
```

---

# 📄 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this project in accordance with the terms of the MIT License.

---

# ⭐ Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork the repository
- 🐛 Report issues
- 💡 Submit feature requests
- 🤝 Contribute improvements

Your support helps improve the project and makes it more discoverable.

---

# 🙏 Acknowledgements

Special thanks to the open-source community and the developers behind:

- Django
- Django REST Framework
- React
- Vite
- Bootstrap
- MySQL
- Gunicorn
- WhiteNoise

---

**Thank you for checking out the HR Management System!**