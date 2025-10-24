import sqlite3
import csv

DB_NAME = "students.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            StudentID INTEGER PRIMARY KEY,
            Name TEXT,
            Age INTEGER,
            Course TEXT
        )
        ''')
        conn.commit()

def insert_from_csv(csv_filename="students.csv"):
    with get_connection() as conn:
        cursor = conn.cursor()
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute('''
                    INSERT OR IGNORE INTO students (StudentID, Name, Age, Course)
                    VALUES (?, ?, ?, ?)''',
        (int(row['StudentID']), row['Name'], int(row['Age']), row['Course']))
        conn.commit()

def get_all_students():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        return cursor.fetchall()

def add_student(student):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students VALUES (?, ?, ?, ?)',
                       (student.StudentID, student.Name, student.Age, student.Course))
        conn.commit()

def update_student(student_id, updates):
    with get_connection() as conn:
        cursor = conn.cursor()
        fields = []
        values = []
        if updates.Name:
            fields.append("Name = ?")
            values.append(updates.Name)
        if updates.Age:
            fields.append("Age = ?")
            values.append(updates.Age)
        if updates.Course:
            fields.append("Course = ?")
            values.append(updates.Course)
        if not fields:
            return
        values.append(student_id)
        sql = f"UPDATE students SET {', '.join(fields)} WHERE StudentID = ?"
        cursor.execute(sql, values)
        conn.commit()

def delete_student(student_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE StudentID = ?', (student_id,))
        conn.commit()
