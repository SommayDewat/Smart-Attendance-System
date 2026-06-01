create database attendance_system;
use attendance_system;

create table teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100)
);
create table students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    class VARCHAR(50),
    roll_no VARCHAR(20) UNIQUE,
    email VARCHAR(100)
);
create table attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    attendance_date DATE,
    status VARCHAR(10),
    UNIQUE(student_id, attendance_date),

    FOREIGN KEY(student_id)
    REFERENCES students(student_id)
    ON DELETE CASCADE
);

INSERT INTO teachers(username, password)
VALUES ('admin', 'admin123');
INSERT INTO students(name, class, roll_no, email) VALUES
('Rahul Sharma', 'BCA', '101', 'rahul@gmail.com'),
('Aman Verma', 'BCA', '102', 'aman@gmail.com'),
('Priya Singh', 'BCA', '103', 'priya@gmail.com'),
('Sneha Kapoor', 'BCA', '104', 'sneha@gmail.com'),
('Rohit Mehta', 'BCA', '105', 'rohit@gmail.com'),
('Anjali Gupta', 'BCA', '106', 'anjali@gmail.com'),
('Vikas Yadav', 'BCA', '107', 'vikas@gmail.com'),
('Neha Joshi', 'BCA', '108', 'neha@gmail.com'),
('Karan Malhotra', 'BCA', '109', 'karan@gmail.com'),
('Pooja Sharma', 'BCA', '110', 'pooja@gmail.com'),
('Arjun Patel', 'BCA', '111', 'arjun@gmail.com'),
('Simran Kaur', 'BCA', '112', 'simran@gmail.com'),
('Mohit Arora', 'BCA', '113', 'mohit@gmail.com'),
('Riya Saxena', 'BCA', '114', 'riya@gmail.com'),
('Aditya Roy', 'BCA', '115', 'aditya@gmail.com'),
('Nisha Sharma', 'BCA', '116', 'nisha@gmail.com'),
('Yash Thakur', 'BCA', '117', 'yash@gmail.com'),
('Meera Iyer', 'BCA', '118', 'meera@gmail.com'),
('Harsh Dubey', 'BCA', '119', 'harsh@gmail.com'),
('Kritika Jain', 'BCA', '120', 'kritika@gmail.com'),
('Sahil Khan', 'BCA', '121', 'sahil@gmail.com'),
('Tanvi Mishra', 'BCA', '122', 'tanvi@gmail.com'),
('Deepak Chauhan', 'BCA', '123', 'deepak@gmail.com'),
('Dhruv', 'BCA', '124', 'dhruv@gmail.com'),
('Ishita Agarwal', 'BCA', '125', 'ishita@gmail.com');

USE attendance_system;
DESCRIBE students;

SELECT * FROM students LIMIT 5;
