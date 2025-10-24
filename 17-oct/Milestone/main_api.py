from fastapi import FastAPI, HTTPException, Request
from models import Student, UpdateStudent
import database as db
from logger_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Student CRUD API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"API call: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"API response: {response.status_code} for {request.method} {request.url}")
        return response
    except Exception as e:
        logger.error(f"API error during {request.method} {request.url}: {e}")
        raise e

@app.on_event("startup")
def startup_event():
    db.create_table()
    db.insert_from_csv()

@app.get("/")
async def root():
    return {"message": "Welcome to the Student API"}

@app.get("/students")
def get_students():
    students = db.get_all_students()
    return [
        {"StudentID": s[0], "Name": s[1], "Age": s[2], "Course": s[3]}
        for s in students
    ]

@app.post("/students")
def add_student(student: Student):
    try:
        db.add_student(student)
        return {"message": "Student added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/students/{student_id}")
def update_student(student_id: int, updates: UpdateStudent):
    db.update_student(student_id, updates)
    return {"message": "Student updated successfully"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    db.delete_student(student_id)
    return {"message": "Student deleted successfully"}
