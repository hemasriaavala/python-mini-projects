import json
from datetime import datetime

FILE = "expenses.json"

def load_expenses():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(FILE, "w") as f:
        json.dump(expenses, f, indent=2)

def add_expense(amount, category, note=""):
    expenses = load_expenses()
    expenses.append({
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_expenses(expenses)

def show_summary():
    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)
    print(f"\nTotal Spent: ₹{total:.2f}")
    for e in expenses:
        print(f"{e['date']} - {e['category']}: ₹{e['amount']} ({e['note']})")

def main():
    print("💰 Simple Expense Tracker")
    while True:
        print("\n1. Add Expense\n2. Show Summary\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            amt = float(input("Amount: "))
            cat = input("Category: ")
            note = input("Note (optional): ")
            add_expense(amt, cat, note)
        elif choice == "2":
            show_summary()
        elif choice == "3":
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()

