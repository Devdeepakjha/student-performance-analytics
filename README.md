# 🎓 Student Performance Analytics System

A cloud-powered analytics platform that helps educators analyze student performance, generate reports, predict outcomes using Machine Learning, and securely store uploaded datasets using AWS services.

## 🌐 Live Demo

**Application URL**

http://98.91.23.229:5000

---

## 📌 Project Overview

Student Performance Analytics is an end-to-end cloud application built using:

* Flask
* Pandas
* Scikit-Learn
* AWS EC2
* AWS S3
* ReportLab
* HTML/CSS/JavaScript

The platform allows users to upload student datasets, perform automated analysis, generate PDF reports, search individual students, and obtain machine-learning-based performance insights.

---
## 📸 Screenshots

### 🏠 Homepage
<img width="1600" height="900" alt="homepage" src="https://github.com/user-attachments/assets/b6990922-b901-4abf-89ab-efcf9b826125" />

### 📊 Analytics Dashboard
<img width="1600" height="900" alt="dashboard" src="https://github.com/user-attachments/assets/2a9949db-749a-4f64-8d91-66aa55a85cc9" />

### ☁️ AWS EC2 Deployment
<img width="1920" height="1080" alt="aws-ec2" src="https://github.com/user-attachments/assets/9199a2c6-d929-4bb6-990c-1b0fa3c56a02" />

### 🪣 AWS S3 Storage
<img width="1920" height="1080" alt="aws-s3" src="https://github.com/user-attachments/assets/1fe765cd-7127-4871-93cd-7407c24a1b70" />

## Production Deployment

The application is deployed on AWS EC2 using:

- Flask
- Gunicorn (WSGI Server)
- Systemd Service Management
- AWS S3 Storage
- IAM User Access Control

The application automatically starts on server reboot using a Linux systemd service.

## 🚀 Features

### 📊 Data Analytics

* Class average calculation
* Pass/Fail statistics
* Subject-wise performance analysis
* Top performers identification
* Students requiring attention

### 🤖 Machine Learning

* Performance prediction
* Academic trend analysis
* Risk identification

### 📄 PDF Report Generation

Generate:

* Class Performance Report
* Individual Student Report

### 🔍 Student Search

Search students instantly using Roll Number.

### ☁️ Cloud Integration

Uploaded files are automatically stored in AWS S3 for secure cloud storage.

### 🌍 Cloud Deployment

Application hosted on AWS EC2 and accessible through a public IP address.

---

## 🏗️ System Architecture

User Uploads Dataset

↓

Flask Application (EC2)

↓

Pandas Data Analysis

↓

Machine Learning Prediction

↓

PDF Report Generation

↓

AWS S3 Storage

↓

Dashboard Visualization

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask

### Data Analytics

* Pandas
* NumPy

### Machine Learning

* Scikit-Learn

### Cloud

* AWS EC2
* AWS S3
* IAM

### Reports

* ReportLab

### Frontend

* HTML
* CSS
* JavaScript

---

## 📂 Project Structure

```text
student-performance-analytics/

├── app.py
├── analysis.py
├── ml_model.py
├── pdf_generator.py
├── requirements.txt
│
├── templates/
│ ├── index.html
│ └── dashboard.html
│
├── static/
│
├── uploads/
│
└── reports/
```

## 📁 Sample Dataset

Use the following sample format:

| Roll Number | Name  | Maths | Physics | Chemistry | English | Biology |
| ----------- | ----- | ----- | ------- | --------- | ------- | ------- |
| 101         | Rahul | 85    | 78      | 82        | 88      | 90      |
| 102         | Priya | 92    | 89      | 94        | 90      | 95      |
| 103         | Aman  | 65    | 72      | 68        | 70      | 75      |

Save as:

```text
sample_student_data.csv
```

and upload through the application.

---

## ⚙️ Installation

Clone Repository

```bash
git clone https://github.com/Devdeepakjha/student-performance-analytics.git

cd student-performance-analytics
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Application

```bash
python app.py
```

---

## ☁️ AWS Services Used

### AWS EC2

Used for hosting and deploying the Flask application.

Benefits:

* Public accessibility
* Scalable deployment
* Real-world cloud infrastructure

### AWS S3

Used for storing uploaded datasets.

Benefits:

* Durable cloud storage
* Secure object storage
* Easy integration with analytics workflows

### IAM

Used for access control and security management.

---

## 🎯 Why This Project Matters

Educational institutions often manage large volumes of student data manually.

This project helps:

* Reduce manual analysis effort
* Identify weak-performing students quickly
* Generate automated reports
* Improve decision making using analytics
* Leverage cloud computing for scalability

---

## 📈 Future Enhancements

* User Authentication
* Dashboard Charts & Visualizations
* Email Report Delivery
* Database Integration (MySQL/PostgreSQL)
* Docker Deployment
* CI/CD Pipeline
* Domain Name + HTTPS
* Advanced ML Models

---

## 👨‍💻 Author

Deepak Jha

Computer Science Engineering Student

GitHub:
https://github.com/Devdeepakjha

---

## ⭐ Acknowledgements

Built as a cloud-based analytics project demonstrating:

* Data Analytics
* Machine Learning
* Cloud Computing
* AWS Deployment
* Full Stack Development

This project serves as a practical implementation of modern cloud-enabled data analytics systems.
