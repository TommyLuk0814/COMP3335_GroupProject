# COMP3335 Group Project — Secure Student Information Management System

This project implements a secure database application for a university context ("ComputingU"). It features Role-Based Access Control (RBAC), field-level encryption (AES) for sensitive data, audit logging, and protection against SQL injection.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1: Database Installation & Setup](#step-1-database-installation--setup)
- [Step 2: Application Setup](#step-2-application-setup)
- [Step 3: Configuration](#step-3-configuration)
- [Step 4: Running the Application](#step-4-running-the-application)
- [Usage & Demo Accounts](#usage--demo-accounts)
- [Project Structure](#project-structure)

## Prerequisites
To run this application on a clean Windows 11 environment, install:
- Python 3.8 or higher — download from the official Python website. During installation, check "Add Python to PATH".
- MySQL Community Server — choose "Windows (x86, 64-bit), MSI Installer" and install. (Any suspicious external links were removed.)

## Step 1: Database Installation & Setup
1. Install MySQL Server and complete the setup. When prompted, set a strong root password (e.g., `Password123!`) and remember it.
2. Create the application database and import the provided SQL:

Open MySQL CLI or Workbench and run:
```sql
-- Create the database
CREATE DATABASE ComputingU;

-- Use the database
USE ComputingU;

-- Import SQL file (example path)
SOURCE C:/path/to/your/project/code/database.sql;
```
Note: Ensure `database.sql` contains both `CREATE TABLE` statements and initial `INSERT` data.

## Step 2: Application Setup
Open Command Prompt or PowerShell, navigate to the project directory (where `server.py` is located):
```powershell
cd path\to\your\project\code
```
(Optional) Create and activate a virtual environment:
```powershell
python -m venv venv
venv\Scripts\activate
```
Install dependencies:
```powershell
pip install -r requirements.txt
```

## Step 3: Configuration
Edit `db.py` and update the `DB_CONFIG` dictionary to match your local MySQL settings. Example:
```python
# db.py (example snippet)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD",
    "database": "ComputingU",
    "port": 3306
}
```
Initialize demo passwords (the project uses hashed passwords). Run:
```powershell
python test.py
```
Output should confirm that passwords have been hashed/updated.

## Step 4: Running the Application
Ensure MySQL is running, then start the Flask server:
```powershell
python server.py
```
Open a browser at: http://127.0.0.1:5000/

## Usage & Demo Accounts
Default password for demo accounts after running `test.py`: `password123`

1. Student  
   - Email: sint.chiu@stu.edu.hk  
   - Role: Access personal profile, view own grades and disciplinary records.

2. Guardian  
   - Email: jason.yip@email.com  
   - Role: Access personal profile and dependent child's records.

3. ARO (Academic Records Officer) — Staff  
   - Email: ashley.lee@staff.edu.hk  
   - Role: Add/modify/query/delete student grade records.

4. DRO (Disciplinary Records Officer) — Staff  
   - Email: matthew.martin@staff.edu.hk  
   - Role: Add/modify/query/delete student disciplinary records.

## Project Structure
- `server.py` — Main Flask application entry point.  
- `controller.py` — Request routing logic.  
- `db.py` — Database connection configuration.  
- `encryption.py` — AES encryption key management.  
- `sql_method_*.py` — SQL queries separated by role context.  
- `front/templates/` — HTML frontend templates.  
- `app.log` — System log file (records logins, errors, modifications).  
- `config.ini` — Configuration file storing AES encryption key.
