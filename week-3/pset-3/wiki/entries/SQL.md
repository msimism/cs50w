
# SQL

SQL (Structured Query Language) is a domain-specific language used in programming and designed for managing and manipulating relational databases. It is the standard language for relational database management systems.

## Features of SQL

- **Data Querying**: SQL allows users to query data from databases using the `SELECT` statement.
- **Data Manipulation**: SQL supports operations like `INSERT`, `UPDATE`, and `DELETE` to modify the data stored in databases.
- **Data Definition**: SQL defines the structure of data in databases using the `CREATE`, `ALTER`, and `DROP` statements.
- **Data Control**: SQL provides mechanisms to grant or revoke access to the database using `GRANT` and `REVOKE`.

## Basic SQL Syntax

### Select Statement

The `SELECT` statement is used to query data from a database.

```sql
SELECT column1, column2 
FROM table_name;
```

Example:

```sql
SELECT first_name, last_name 
FROM employees;
```

### Insert Statement

The `INSERT INTO` statement is used to insert new records into a table.

```sql
INSERT INTO table_name (column1, column2)
VALUES (value1, value2);
```

Example:

```sql
INSERT INTO employees (first_name, last_name)
VALUES ('John', 'Doe');
```

### Update Statement

The `UPDATE` statement is used to modify existing records in a table.

```sql
UPDATE table_name
SET column1 = value1
WHERE condition;
```

Example:

```sql
UPDATE employees
SET last_name = 'Smith'
WHERE employee_id = 1;
```

### Delete Statement

The `DELETE` statement is used to delete existing records from a table.

```sql
DELETE FROM table_name
WHERE condition;
```

Example:

```sql
DELETE FROM employees
WHERE employee_id = 1;
```

## Joins

SQL joins are used to combine rows from two or more tables based on a related column between them. Common types of joins include:

- **INNER JOIN**: Returns records that have matching values in both tables.
- **LEFT JOIN**: Returns all records from the left table and the matched records from the right table.
- **RIGHT JOIN**: Returns all records from the right table and the matched records from the left table.

### Example of INNER JOIN

```sql
SELECT employees.first_name, departments.department_name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.department_id;
```

## Conclusion

SQL is a powerful language used to communicate with and manipulate databases. It is widely used in data analysis, web development, and software engineering to manage data effectively.
