# 🏢 Employee Management API

A FastAPI + MongoDB project to manage employee data with features like create, read, update, delete, search by skill, and view average salary by department. Includes JWT-based authentication and pagination.
---
# ⚡ Features
- JWT Authentication: Secure access to all endpoints.
- CRUD Operations: Create, Read, Update, Delete employees.
- Search Employees: Find employees by skill (case-insensitive).
- Average Salary: View average salary grouped by department.
- Pagination: Skip & limit for listing employees.
- MongoDB Indexes: Optimized queries with indexes on employee_id, joining_date, and skills.
- Schema Validation: MongoDB JSON schema ensures data consistency.

---
# 🛠 Tech Stack
- Backend: FastAPI (Python)
- Database: MongoDB (NoSQL)
- Authentication: JWT tokens
- Password Hashing: Passlib (bcrypt)
- Pagination: Skip & limit for listing employees.
- Dependencies: Motor (async MongoDB driver), Pydantic, python-dotenv

---
## Run Locally

**Clone the project**
```bash
git clone https://github.com/vishal499/LLUMO.git
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```
**Start Your FastAPI App**
```bash
uvicorn main:app --reload
```

---
# 📖 API Endpoints
## 1. Create Employee ##
   - POST /employees
   - Requires JWT token

---
## 1. List Employees ##
   - GET /employees
   - Optional query parameters:
      - department → filter by department
      - skip → pagination skip (default 0)
      - limit → pagination limit (default 10)

---
   
