from database.connection import DatabaseManager
from utils.logger import logger

class UserManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def register_user(self, username, budget):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, monthly_budget) VALUES (?, ?)", 
                    (username, budget)
                )
                conn.commit()
                logger.info(f"User registered: {username}")
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to register user {username}: {e}")
            return None

    def get_user(self, username):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, monthly_budget FROM users WHERE username = ?", (username,))
            return cursor.fetchone()