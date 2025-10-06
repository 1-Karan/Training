CREATE DATABASE SchoolDB;

USE SchoolDB;
CREATE table Students(
id INT auto_increment primary key,
name varchar(255),
age int,
course varchar(50),
marks int
);

INSERT INTO Students (name, age, course, marks)
VALUES
('Priya', 22, 'ML', 90),
('Arjun', 20, 'Data Science', 78);
select * from Students;
# CRUD -- Create, Read, Update & Delete

select name, age from students where marks>80;
select name, marks from students;
UPDATE Students
SET marks = 95, course = 'Advanced AI'
WHERE id = 4;
-- UPDATE Students SET course = 'AI';

delete from students where id=3;