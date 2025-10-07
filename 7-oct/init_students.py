from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI demo!"}

# Path parameter example
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {
        "student_id": student_id,
        "name": "Rahul",
        "course": "AI"
    }
