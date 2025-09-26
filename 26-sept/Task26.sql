CREATE TABLE Employees (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL,
age INT,
department VARCHAR(50),
salary DECIMAL(10,2)
);

INSERT INTO Employees (name, age, department, salary)
VALUES
  ('Alice', 30, 'Engineering', 75000.00),
  ('Bob', 28, 'Marketing', 55000.00),
  ('Carol', 35, 'HR', 60000.00);

SELECT * FROM Employees;
SELECT name, department
FROM Employees
WHERE salary > 60000.00;
SELECT id, name, age, salary
FROM Employees
WHERE department = 'Engineering';

UPDATE Employees
SET salary = 60000.00
WHERE id = 2;

DELETE FROM Employees
WHERE id = 1;
