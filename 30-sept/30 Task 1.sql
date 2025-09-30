CREATE DATABASE UniversityDB;
USE UniversityDB;
-- Students Table
CREATE TABLE Students (
student_id INT PRIMARY KEY,
name VARCHAR(50),
city VARCHAR(50)
);
-- Courses Table
CREATE TABLE Courses (
course_id INT PRIMARY KEY,
course_name VARCHAR(50),
credits INT
);
-- Enrollments Table
CREATE TABLE Enrollments (
enroll_id INT PRIMARY KEY,
student_id INT,
course_id INT,
grade CHAR(2),
FOREIGN KEY (student_id) REFERENCES Students(student_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
-- Insert Students
INSERT INTO Students VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi'),
(3, 'Arjun', 'Bengaluru'),
(4, 'Neha', 'Hyderabad'),
(5, 'Vikram', 'Chennai');
-- Insert Courses
INSERT INTO Courses VALUES
(101, 'Mathematics', 4),
(102, 'Computer Science', 3),
(103, 'Economics', 2),
(104, 'History', 3);
-- Insert Enrollments
INSERT INTO Enrollments VALUES
(1, 1, 101, 'A'),
(2, 1, 102, 'B'),
(3, 2, 103, 'A'),
(4, 3, 101, 'C'),
(5, 4, 102, 'B'),
(6, 5, 104, 'A');

DELIMITER $$
CREATE PROCEDURE ListAllStudents()
BEGIN
    SELECT * FROM Students;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE ListAllCourses()
BEGIN
    SELECT * FROM Courses;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE FindStudentsByCity(IN city_name VARCHAR(50))
BEGIN
    SELECT * FROM Students WHERE city = city_name;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE ListStudentCourses()
BEGIN
    SELECT s.student_id, s.name AS student_name, c.course_name
    FROM Students s
    JOIN Enrollments e ON s.student_id = e.student_id
    JOIN Courses c ON e.course_id = c.course_id;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE StudentsInCourse(IN cid INT)
BEGIN
    SELECT s.student_id, s.name AS student_name, c.course_name
    FROM Students s
    JOIN Enrollments e ON s.student_id = e.student_id
    JOIN Courses c ON e.course_id = c.course_id
    WHERE c.course_id = cid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE CountStudentsPerCourse()
BEGIN
    SELECT c.course_name, COUNT(e.student_id) AS student_count
    FROM Courses c
    LEFT JOIN Enrollments e ON c.course_id = e.course_id
    GROUP BY c.course_id, c.course_name;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE ListStudentsWithGrades()
BEGIN
    SELECT s.name AS student_name, c.course_name, e.grade
    FROM Enrollments e
    JOIN Students s ON e.student_id = s.student_id
    JOIN Courses c ON e.course_id = c.course_id;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE CoursesByStudent(IN sid INT)
BEGIN
    SELECT c.course_name, e.grade
    FROM Enrollments e
    JOIN Courses c ON e.course_id = c.course_id
    WHERE e.student_id = sid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AverageGradePerCourse()
BEGIN
    SELECT 
        c.course_name,
        ROUND(AVG(
            CASE e.grade
                WHEN 'A' THEN 4
                WHEN 'B' THEN 3
                WHEN 'C' THEN 2
                WHEN 'D' THEN 1
                ELSE 0
            END
        ), 2) AS average_grade
    FROM Enrollments e
    JOIN Courses c ON e.course_id = c.course_id
    GROUP BY c.course_name;
END $$
DELIMITER ;


