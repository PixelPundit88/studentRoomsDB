-- Drop tables if they exist
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;

-- Create rooms table
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Create students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    birthday DATE NOT NULL,
    sex CHAR(1) CHECK (sex IN ('M', 'F')),
    room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE
);