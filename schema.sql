CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    fee NUMERIC(10,2) NOT NULL DEFAULT 0
);

-- optional sample records
-- INSERT INTO students (name, course, fee) VALUES
-- ('Alice', 'Python', 2500.00),
-- ('Bob', 'Java', 3000.00);
