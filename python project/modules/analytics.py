from database.connection import DatabaseManager

class AnalyticsEngine:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def generate_summary(self, user_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT monthly_budget FROM users WHERE id = ?", (user_id,))
            budget = cursor.fetchone()[0]

            cursor.execute(
                "SELECT type, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY type", 
                (user_id,)
            )
            totals = dict(cursor.fetchall())

        income = totals.get('INCOME', 0.0)
        expenses = totals.get('EXPENSE', 0.0)
        remaining_budget = budget - expenses

        return {
            "monthly_budget": budget,
            "total_income": income,
            "total_expenses": expenses,
            "remaining_budget": remaining_budget,
            "budget_exceeded": expenses > budget
        }