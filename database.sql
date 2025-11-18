CREATE TABLE guardians (
    id INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARBINARY(128) -- private data
);

CREATE TABLE staffs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(255) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    identification_number VARBINARY(512),  -- private data
    address VARBINARY(512), -- private data
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARBINARY(128),  -- private data
    department ENUM('Computing', 'Business', 'Engineering', 'Humanities', 'Science'),
    role ENUM('ARO', 'DRO' )
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
    identification_number VARBINARY(1024),  -- private data
    address VARBINARY(1024),     -- private data
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARBINARY(256),      -- private data
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
    descriptions BLOB, -- private data
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (staff_id) REFERENCES staffs(id)
);