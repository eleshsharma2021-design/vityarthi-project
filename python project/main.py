from database.connection import DatabaseManager
from modules.user_manager import UserManager
from modules.transaction_service import TransactionService
from modules.analytics import AnalyticsEngine
from utils.validators import validate_amount, validate_category

def main():
    db = DatabaseManager()
    user_mgr = UserManager(db)
    txn_service = TransactionService(db)
    analytics = AnalyticsEngine(db)

    print("=== Welcome to Personal Finance Tracker ===")
    username = input("Enter username: ").strip()
    user = user_mgr.get_user(username)

    if not user:
        print("User not found. Setting up new profile...")
        budget, _ = validate_amount(input("Enter monthly budget (USD/INR): "))
        user_id = user_mgr.register_user(username, budget or 1000.0)
    else:
        user_id = user[0]

    while True:
        print("\n--- MENU ---")
        print("1. Add Transaction (Income/Expense)")
        print("2. View All Transactions")
        print("3. View Financial Summary & Analytics")
        print("4. Exit")
        choice = input("Select option (1-4): ").strip()

        if choice == "1":
            t_type = input("Type (INCOME/EXPENSE): ").strip().upper()
            if t_type not in ["INCOME", "EXPENSE"]:
                print("Invalid type!")
                continue
            
            amt_in = input("Amount: ")
            amount, err = validate_amount(amt_in)
            if err:
                print(f"Error: {err}")
                continue

            cat_in = input("Category (Food/Transport/Utilities/Entertainment/Income/Other): ")
            category, err = validate_category(cat_in)
            if err:
                print(f"Error: {err}")
                continue

            desc = input("Description (optional): ")
            if txn_service.add_transaction(user_id, t_type, amount, category, desc):
                print("Transaction saved successfully!")

        elif choice == "2":
            txns = txn_service.get_transactions(user_id)
            print("\nID | Type | Amount | Category | Description")
            print("-" * 45)
            for t in txns:
                print(f"{t[0]} | {t[1]} | ${t[2]:.2f} | {t[3]} | {t[4]}")

        elif choice == "3":
            summary = analytics.generate_summary(user_id)
            print("\n=== FINANCIAL REPORT ===")
            print(f"Monthly Budget:   ${summary['monthly_budget']:.2f}")
            print(f"Total Income:     ${summary['total_income']:.2f}")
            print(f"Total Expenses:   ${summary['total_expenses']:.2f}")
            print(f"Remaining Budget: ${summary['remaining_budget']:.2f}")
            if summary['budget_exceeded']:
                print("WARNING: You have exceeded your monthly budget!")

        elif choice == "4":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()