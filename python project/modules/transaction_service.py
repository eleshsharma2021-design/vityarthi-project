from database.connection import DatabaseManager
from utils.logger import logger

class TransactionService:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def add_transaction(self, user_id, txn_type, amount, category, description=""):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO transactions (user_id, type, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                    (user_id, txn_type.upper(), amount, category, description)
                )
                conn.commit()
                logger.info(f"Transaction recorded for user_id {user_id}: {txn_type} {amount}")
                return True
        except Exception as e:
            logger.error(f"Error recording transaction: {e}")
            return False

    def get_transactions(self, user_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, type, amount, category, description FROM transactions WHERE user_id = ?", 
                (user_id,)
            )
            return cursor.fetchall()

    def delete_transaction(self, txn_id, user_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (txn_id, user_id))
            conn.commit()
            return cursor.rowcount > 0