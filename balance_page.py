import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# File to store balance data
DATA_FILE = "balance_data.json"

# File to store income and expenses data
INCOME_FILE = "incomes_data.json"
EXPENSE_FILE = "expenses_data.json"

# Function to save a new balance entry with the current date
def save_balance_entry(amount):
    # Load existing balances
    balances = load_balance()
    
    # Create a new balance entry with the current date
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount
    }
    
    # Add the new balance entry to the list of balances
    balances.append(new_entry)
    
    # Save the updated balances back to the file
    with open(DATA_FILE, "w") as f:
        json.dump(balances, f)

# Function to load balance from the JSON file
def load_balance():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []  # Return an empty list if no data exists

def load_income():
    if os.path.exists(INCOME_FILE):
        try:
            with open(INCOME_FILE, "r") as f:
                data = json.load(f)
                print("Loaded Income Data:", data)  # Debug print
                return data.get("incomes", [])
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from income_data.json.")
    return []

# Function to load expenses from the JSON file
def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as f:
            data = json.load(f)
            return data.get("expenses", [])  # Only get the list of expenses
    return []


# Function to calculate the balance
def calculate_balance():
    income_data = load_income()
    expense_data = load_expenses()

    # Debug: Print loaded income and expense data
    print("Income Data:", income_data)
    print("Expense Data:", expense_data)

    # Ensure data is in expected format (list of dictionaries)
    if not isinstance(income_data, list) or not isinstance(expense_data, list):
        messagebox.showerror("Error", "Invalid data format for income or expenses.")
        return 0  # Return 0 if data format is incorrect

    # Calculate total income and expenses
    try:
        total_income = sum([float(entry['amount']) for entry in income_data if 'amount' in entry])
        total_expenses = sum([float(entry['amount']) for entry in expense_data if 'amount' in entry])
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Invalid data entry detected.")
        return 0

    # Calculate the balance
    balance = total_income - total_expenses

    # Save the new balance with the current date
    save_balance_entry(balance)

    return balance

# Function to create the balance page UI and load saved balances
def create_balance_page(frame):
    # Create a frame for the balance table
    balance_table_frame = tk.Frame(frame)
    balance_table_frame.grid(row=0, column=0, columnspan=2, pady=20)

    # Table headers
    balance_name_header = tk.Label(balance_table_frame, text="Date", font=('bold', 12))
    balance_name_header.grid(row=0, column=0, padx=10, pady=5)

    balance_amount_header = tk.Label(balance_table_frame, text="Amount", font=('bold', 12))
    balance_amount_header.grid(row=0, column=1, padx=10, pady=5)

    # Load balances from the file
    balances = load_balance()

    # Display loaded balances in the table
    for idx, balance in enumerate(balances, start=1):
        balance_name_label = tk.Label(balance_table_frame, text=balance["date"])
        balance_name_label.grid(row=idx, column=0, padx=10, pady=5)

        balance_amount_label = tk.Label(balance_table_frame, text=f"Tsh {balance['amount']:.2f}")
        balance_amount_label.grid(row=idx, column=1, padx=10, pady=5)

    # Calculate and display the current balance
    current_balance = calculate_balance()

    # Label for displaying the current balance
    current_balance_label = tk.Label(frame, font=('bold', 14))

    # Check if the balance is negative and set color accordingly
    if current_balance < 0:
        current_balance_label.config(text=f"Current Balance: -Tsh {abs(current_balance):.2f}", fg="red")
    else:
        current_balance_label.config(text=f"Current Balance: Tsh {current_balance:.2f}", fg="black")
        return current_balance

    # Place the balance label
    current_balance_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create the main window
root = tk.Tk()
root.title("Balance Page")

# Create the frame for the balance page
balance_frame = tk.Frame(root)
balance_frame.pack(pady=20, padx=20)

# Create the balance page UI
create_balance_page(balance_frame)

# Start the Tkinter main loop
root.mainloop()
