-- Средняя задача по SQL: Использование JOIN, GROUP BY и HAVING
-- Сценарий: Обычная база данных компании с отделами и сотрудниками.

-- 1. Создаем структуру таблиц
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    salary INTEGER,
    department_id INTEGER REFERENCES departments(id)
);

-- 2. Наполняем данными
INSERT INTO departments (name) VALUES ('IT'), ('HR'), ('Sales');
INSERT INTO employees (name, salary, department_id) VALUES 
('Alice', 120000, 1), ('Bob', 115000, 1), ('Charlie', 130000, 1), ('David', 90000, 1),
('Eve', 70000, 2), ('Frank', 75000, 2),
('Grace', 80000, 3), ('Heidi', 85000, 3), ('Ivan', 90000, 3);

-- 3. ЗАДАЧА:
-- Вывести названия отделов, где работает СТРОГО больше 3 сотрудников, 
-- и показать среднюю зарплату в этих отделах (округленную до 2 знаков).
SELECT d.name AS department_name, 
       COUNT(e.id) AS employee_count, 
       ROUND(AVG(e.salary), 2) AS avg_salary
FROM departments d
JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.name
HAVING COUNT(e.id) > 3;
