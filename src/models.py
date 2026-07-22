from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Room:
    id: int
    name: str

    def to_dict(self) -> dict:
        return {'id': self.id, 'name': self.name}


@dataclass
class Student:
    id: int
    name: str
    birthday: str
    sex: str
    room_id: int

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'birthday': self.birthday,
            'sex': self.sex,
            'room_id': self.room_id
        }


@dataclass
class RoomStatistics:
    """DTO for room statistics query results"""
    room_id: int
    room_name: str
    student_count: Optional[int] = None
    avg_age: Optional[float] = None
    age_difference: Optional[float] = None
    mixed_sex: Optional[bool] = None

    def to_dict(self) -> dict:
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'student_count': self.student_count,
            'avg_age': self.avg_age,
            'age_difference': self.age_difference,
            'mixed_sex': self.mixed_sex
        }