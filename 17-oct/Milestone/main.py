import database as db

def main():
    # Create table & load CSV
    db.create_table()
    db.insert_from_csv()

    # Simple class to represent a student
    class Student:
        def __init__(self, StudentID, Name, Age, Course):
            self.StudentID = StudentID
            self.Name = Name
            self.Age = Age
            self.Course = Course

    new_student = Student(106, "Kiran", 22, "Data Science")
    db.add_student(new_student)
    print(f"Inserted student: {new_student.Name}")


    class Updates:
        def __init__(self, Name=None, Age=None, Course=None):
            self.Name = Name
            self.Age = Age
            self.Course = Course

    updates = Updates(Course="Data Science")
    db.update_student(102, updates)
    print("Updated student 102 course to Data Science")

    db.delete_student(105)
    print("Deleted student with ID 105")

    students = db.get_all_students()
    print("\nAll students:")
    for s in students:
        print(s)

if __name__ == "__main__":
    main()
