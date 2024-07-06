import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    amount REAL,
    date TEXT,
    category TEXT,
    type TEXT,
    description TEXT
)
''')

def add_transaction(amount, date, category, type, description):
    with conn:
        c.execute("INSERT INTO transactions (amount, date, category, type, description) VALUES (?, ?, ?, ?, ?)",
                  (amount, date, category, type, description))

def view_summary():
    c.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    total_income = c.fetchone()[0] or 0
    c.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    total_expenses = c.fetchone()[0] or 0
    balance = total_income - total_expenses
    print(f"Total Income: ${total_income}")
    print(f"Total Expenses: ${total_expenses}")
    print(f"Balance: ${balance}")

def view_transactions():
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    print("ID | Amount | Date | Category | Type | Description")
    print("---------------------------------------------------")
    for t in transactions:
        print(f"{t[0]} | ${t[1]} | {t[2]} | {t[3]} | {t[4]} | {t[5]}")

def main():
    while True:
        print("\nFinancial Budget Tracker")
        print("1. Add Transaction")
        print("2. View Summary")
        print("3. View Transactions")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            type = input("Enter type (income/expense): ")
            description = input("Enter description: ")
            add_transaction(amount, date, category, type, description)
            print("Transaction added!")
        elif choice == '2':
            view_summary()
        elif choice == '3':
            view_transactions()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Close database connection on exit
conn.close()
