CREATE TABLE guardians (
    id INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20)
);

CREATE TABLE staffs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(255) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    identification_number VARCHAR(255),
    address VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    department ENUM('Computing', 'Business', 'Engineering', 'Humanities', 'Science'),
    role ENUM('ARO', 'DRO', 'Admin', 'Faculty')
);

CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    identification_number VARCHAR(255),
    address VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    enrollment_year YEAR,
    guardian_id INT,
    guardian_relation ENUM('Father', 'Mother', 'Legal Guardian'),
    FOREIGN KEY (guardian_id) REFERENCES guardians(id)
);

CREATE TABLE grades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    term VARCHAR(10),
    grade ENUM('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F'),
    comments TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE disciplinary_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    date DATE,
    staff_id INT NOT NULL,
    descriptions TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (staff_id) REFERENCES staffs(id)
);