CREATE DATABASE SchooolDB;

USE SchooolDB;

CREATE TABLE Subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50)
);

CREATE TABLE Teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    subject_id INT
);

INSERT INTO Subjects (subject_name) VALUES
('Mathematics'),   -- id = 1
('Science'),       -- id = 2
('English'),       -- id = 3
('History'),       -- id = 4
('Geography');     -- id = 5 (no teacher yet)

INSERT INTO Teachers (name, subject_id) VALUES
('Rahul Sir', 1),    -- Mathematics
('Priya Madam', 2),  -- Science
('Arjun Sir', NULL), -- No subject assigned
('Neha Madam', 3);   -- English

-- 7. INNER JOIN: Only matching records (Teachers with subjects)
SELECT 
    t.teacher_id,
    t.name AS teacher_name,
    s.subject_name
FROM 
    Teachers t
INNER JOIN 
    Subjects s ON t.subject_id = s.subject_id;

-- 8. LEFT JOIN: All Teachers, with subjects (if any)
SELECT 
    t.teacher_id,
    t.name AS teacher_name,
    s.subject_name
FROM 
    Teachers t
LEFT JOIN 
    Subjects s ON t.subject_id = s.subject_id;

-- 9. RIGHT JOIN: All Subjects, with teachers (if any)
SELECT 
    t.name AS teacher_name,
    s.subject_id,
    s.subject_name
FROM 
    Teachers t
RIGHT JOIN 
    Subjects s ON t.subject_id = s.subject_id;

-- 10. FULL JOIN: All records from both tables (simulated using UNION)
SELECT 
    t.teacher_id,
    t.name AS teacher_name,
    s.subject_id,
    s.subject_name
FROM 
    Teachers t
LEFT JOIN 
    Subjects s ON t.subject_id = s.subject_id

UNION

SELECT 
    t.teacher_id,
    t.name AS teacher_name,
    s.subject_id,
    s.subject_name
FROM 
    Teachers t
RIGHT JOIN 
    Subjects s ON t.subject_id = s.subject_id;
