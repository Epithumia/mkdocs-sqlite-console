DROP TABLE IF EXISTS employees;
CREATE TABLE employees
(
    id          integer,
    name        text,
    designation text,
    manager     integer,
    hired_on    date,
    salary      integer,
    commission  float,
    dept        integer
);
