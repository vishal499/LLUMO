import os
import re
from datetime import datetime, date
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import motor.motor_asyncio

# Load .env if present
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "assessment_db")
COLLECTION_NAME = "employees"

app = FastAPI(title="Employees API - FastAPI + MongoDB")

# Mongo client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# -------------------------
# Pydantic Schemas
# -------------------------
class EmployeeBase(BaseModel):
    name: str
    department: str
    salary: int
    joining_date: date
    skills: List[str] = Field(default_factory=list)

class EmployeeCreate(EmployeeBase):
    employee_id: str = Field(..., example="E123")

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[int] = None
    joining_date: Optional[date] = None
    skills: Optional[List[str]] = None

# -------------------------
# Helper
# -------------------------
def employee_helper(emp_doc: dict) -> dict:
    jd = emp_doc.get("joining_date")
    if isinstance(jd, datetime):
        jd = jd.date().isoformat()
    elif isinstance(jd, date):
        jd = jd.isoformat()
    return {
        "id": str(emp_doc.get("_id")),
        "employee_id": emp_doc.get("employee_id"),
        "name": emp_doc.get("name"),
        "department": emp_doc.get("department"),
        "salary": emp_doc.get("salary"),
        "joining_date": jd,
        "skills": emp_doc.get("skills", []),
    }

# -------------------------
# Startup: indexes & optional JSON Schema
# -------------------------
@app.on_event("startup")
async def startup_actions():
    await collection.create_index("employee_id", unique=True)
    await collection.create_index("joining_date")
    await collection.create_index("skills")

    # Optional: MongoDB JSON Schema validation
    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
            "properties": {
                "employee_id": {"bsonType": "string"},
                "name": {"bsonType": "string"},
                "department": {"bsonType": "string"},
                "salary": {"bsonType": "int", "minimum": 0},
                "joining_date": {"bsonType": "date"},
                "skills": {"bsonType": "array", "items": {"bsonType": "string"}}
            }
        }
    }
    try:
        await db.command({
            "collMod": COLLECTION_NAME,
            "validator": validator,
            "validationLevel": "moderate"
        })
    except:
        pass  # collection may not exist yet

# -------------------------
# Root
# -------------------------
@app.get("/")
async def root():
    return {"message": "FastAPI + MongoDB API is running!"}

# -------------------------
# 1. Create Employee
# -------------------------
@app.post("/employees", status_code=status.HTTP_201_CREATED)
async def create_employee(payload: EmployeeCreate):
    existing = await collection.find_one({"employee_id": payload.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="employee_id already exists")
    doc = payload.dict()
    doc["joining_date"] = datetime.combine(doc["joining_date"], datetime.min.time())
    result = await collection.insert_one(doc)
    new_doc = await collection.find_one({"_id": result.inserted_id})
    return employee_helper(new_doc)

# -------------------------
# 2. Search Employees by Skill
# -------------------------
@app.get("/employees/search")
async def search_employees_by_skill(
    skill: str = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    regex = {"$elemMatch": {"$regex": f"^{re.escape(skill)}$", "$options": "i"}}
    query = {"skills": regex}
    cursor = collection.find(query).skip(skip).limit(limit)
    docs = [employee_helper(doc) async for doc in cursor]
    if not docs:
        raise HTTPException(status_code=404, detail="Employee not found")
    return docs

# -------------------------
# 3. Average Salary by Department
# -------------------------
@app.get("/employees/avg-salary")
async def avg_salary_by_department():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"_id": 0, "department": "$_id", "avg_salary": {"$round": ["$avg_salary", 0]}}}
    ]
    cursor = collection.aggregate(pipeline)
    result = [doc async for doc in cursor]
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result

# -------------------------
# 4. List Employees
# -------------------------
@app.get("/employees")
async def list_employees(
    department: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    query = {}
    if department:
        query["department"] = department
    cursor = collection.find(query).sort("joining_date", -1).skip(skip).limit(limit)
    docs = [employee_helper(doc) async for doc in cursor]
    return docs

# -------------------------
# 5. Get Employee by ID
# -------------------------
@app.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    doc = await collection.find_one({"employee_id": employee_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_helper(doc)

# -------------------------
# 6. Update Employee
# -------------------------
@app.put("/employees/{employee_id}")
async def update_employee(employee_id: str, payload: EmployeeUpdate):
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    if "joining_date" in update_data:
        update_data["joining_date"] = datetime.combine(update_data["joining_date"], datetime.min.time())
    result = await collection.update_one({"employee_id": employee_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    updated = await collection.find_one({"employee_id": employee_id})
    return employee_helper(updated)

# -------------------------
# 7. Delete Employee
# -------------------------
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    result = await collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        return {"success": False, "message": "Employee not found"}
    return {"success": True, "message": f"Employee {employee_id} deleted"}
