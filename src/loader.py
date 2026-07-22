import json
from typing import Tuple
from src.db_manager import DatabaseInterface

class DataLoader:
    def __init__(self, db: DatabaseInterface):
        self.db = db

    def load_rooms(self, filepath: str) -> int:
        with open(filepath, 'r') as f:
            rooms = json.load(f)
        if not rooms:
            print("No rooms found in file")
            return 0
        query = "INSERT INTO rooms (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING"
        values = [(room['id'], room['name']) for room in rooms]
        count = self.db.executemany(query, values)
        print(f"Loaded {count} rooms from {filepath}")
        return count

    def load_students(self, filepath: str) -> int:
        with open(filepath, 'r') as f:
            students = json.load(f)
        if not students:
            print("No students found in file")
            return 0
        query = """
                INSERT INTO students (id, name, birthday, sex, room_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING \
                """
        values = []
        for student in students:
            birthday = student['birthday'].split('T')[0]
            values.append((
                student['id'],
                student['name'],
                birthday,
                student['sex'],
                student['room']
            ))
        count = self.db.executemany(query, values)
        print(f"Loaded {count} students from {filepath}")
        return count

    def load_all(self, rooms_file: str, students_file: str) -> Tuple[int, int]:
        rooms_count = self.load_rooms(rooms_file)
        students_count = self.load_students(students_file)
        return rooms_count, students_count