def validate_amount(amount_str):
    try:
        val = float(amount_str)
        if val <= 0:
            return None, "Amount must be greater than zero."
        return val, None
    except ValueError:
        return None, "Invalid numerical value."

def validate_category(category):
    valid_categories = ["Food", "Transport", "Utilities", "Entertainment", "Income", "Other"]
    if category.capitalize() not in valid_categories:
        return None, f"Category must be one of: {', '.join(valid_categories)}"
    return category.capitalize(), None