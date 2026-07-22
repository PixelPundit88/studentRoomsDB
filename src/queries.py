from typing import List, Dict
from src.db_manager import DatabaseInterface

class QueryService:
    def __init__(self, db: DatabaseInterface):
        self.db = db

    def get_rooms_with_student_count(self) -> List[Dict]:
        query = """
            SELECT r.id, r.name, COUNT(s.id) AS student_count
            FROM rooms r
            LEFT JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            ORDER BY r.id
        """
        return self.db.fetchall(query)

    def get_rooms_smallest_avg_age(self, limit: int = 5) -> List[Dict]:
        query = """
            SELECT r.id, r.name,
                   ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))), 2) AS avg_age
            FROM rooms r
            INNER JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            HAVING COUNT(s.id) > 0
            ORDER BY avg_age
            LIMIT %s
        """
        return self.db.fetchall(query, (limit,))

    def get_rooms_largest_age_diff(self, limit: int = 5) -> List[Dict]:
        query = """
            SELECT r.id, r.name,
                   (MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) -
                    MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday)))) AS age_diff
            FROM rooms r
            INNER JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            HAVING COUNT(s.id) >= 2
            ORDER BY age_diff DESC
            LIMIT %s
        """
        return self.db.fetchall(query, (limit,))

    def get_mixed_sex_rooms(self) -> List[Dict]:
        query = """
            SELECT r.id, r.name
            FROM rooms r
            INNER JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) = 2
            ORDER BY r.id
        """
        return self.db.fetchall(query)

    def run_all_queries(self) -> Dict[str, List[Dict]]:
        return {
            'rooms_with_student_count': self.get_rooms_with_student_count(),
            'rooms_smallest_avg_age': self.get_rooms_smallest_avg_age(),
            'rooms_largest_age_diff': self.get_rooms_largest_age_diff(),
            'mixed_sex_rooms': self.get_mixed_sex_rooms()
        }