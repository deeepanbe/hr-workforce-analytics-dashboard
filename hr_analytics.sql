-- HR Workforce Analytics SQL Queries
-- Author: Deepanraj A - Data Analyst
-- Database: MySQL/PostgreSQL Compatible

-- Employee Turnover Analysis
SELECT 
    department,
    COUNT(*) as total_employees,
    SUM(CASE WHEN termination_date IS NOT NULL THEN 1 ELSE 0 END) as terminated,
    ROUND(SUM(CASE WHEN termination_date IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as turnover_rate
FROM employees
GROUP BY department
ORDER BY turnover_rate DESC;

-- Average Tenure by Department
SELECT 
    department,
    ROUND(AVG(DATEDIFF(COALESCE(termination_date, CURDATE()), hire_date) / 365.25), 2) as avg_tenure_years
FROM employees
GROUP BY department;

-- Salary Analysis by Job Title
SELECT 
    job_title,
    COUNT(*) as employee_count,
    ROUND(AVG(salary), 2) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary
FROM employees
WHERE termination_date IS NULL
GROUP BY job_title
ORDER BY avg_salary DESC;

-- Performance Rating Distribution
SELECT 
    performance_rating,
    COUNT(*) as employee_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM employee_performance
WHERE review_year = YEAR(CURDATE())
GROUP BY performance_rating;

-- High Turnover Risk Employees
SELECT 
    employee_id,
    employee_name,
    department,
    job_title,
    DATEDIFF(CURDATE(), hire_date) / 365.25 as tenure_years,
    performance_rating,
    salary
FROM employees e
JOIN employee_performance ep ON e.employee_id = ep.employee_id
WHERE e.termination_date IS NULL
    AND ep.performance_rating >= 4
    AND e.salary < (SELECT AVG(salary) * 0.9 FROM employees WHERE department = e.department)
ORDER BY performance_rating DESC;
