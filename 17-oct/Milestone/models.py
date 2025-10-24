from pydantic import BaseModel

class Student(BaseModel):
    StudentID: int
    Name: str
    Age: int
    Course: str

class UpdateStudent(BaseModel):
    Name: str | None = None
    Age: int | None = None
    Course: str | None = None
