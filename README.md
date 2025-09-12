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
## 2. List Employees ##
   - GET /employees
   - Optional query parameters:
      - department → filter by department
      - skip → pagination skip (default 0)
      - limit → pagination limit (default 10)

---
## 3. Search Employees by Skill ##
   - GET /employees/search?skill=Java
   - Case-insensitive search
   - Supports pagination (skip, limit)

---
## 4. Get Employee by ID ##
   - GET /employees/{employee_id}

---

## 5. Update Employee ##
   - PUT /employees/{employee_id}
   - Only provide fields you want to update

---
## 6. Delete Employee ##
   - DELETE /employees/{employee_id}
---
## 7. Average Salary by Department ##
   - GET /employees/avg-salary
   - Returns department-wise average salary
---

# 🧪 Testing
 1.Open Swagger UI:
```bash
http://127.0.0.1:8000/docs

```
- Authorize using JWT token 

- Test endpoints one by one 

---
# 🔐 Notes
- Passwords are hashed with bcrypt
- JWT token expires after 60 minutes
- Indexed fields improve performance for search and listing
  
---  




   
