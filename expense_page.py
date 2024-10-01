import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store expense data
DATA_FILE = "expenses_data.json"

# Function to save expenses and total expenses to the JSON file
def save_expenses(expenses):
    total_expenses = calculate_total_expenses(expenses)
    data = {"expenses": expenses, "total_expenses": total_expenses}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Function to load expenses from the JSON file
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("expenses", []), data.get("total_expenses", 0)
    return [], 0  # Return an empty list and 0 total if file does not exist

# Function to calculate the total sum of all expenses
def calculate_total_expenses(expenses):
    return sum(expense["amount"] for expense in expenses)

# Function to add a new expense to the table and save it to the file
def add_expense_entry(expense_table_frame, expense_name_entry, expense_amount_entry, expenses, total_expenses_label):
    expense_name = expense_name_entry.get().strip()  # Strip whitespace
    expense_amount = expense_amount_entry.get().strip()  # Strip whitespace

    if expense_name and expense_amount:
        try:
            # Convert amount to float to validate
            amount = float(expense_amount)

            # Add the expense to the table
            row = len(expenses) + 1  # Get the next row number
            expense_name_label = tk.Label(expense_table_frame, text=expense_name)
            expense_name_label.grid(row=row, column=0, padx=10, pady=5)

            expense_amount_label = tk.Label(expense_table_frame, text=f"{amount:.2f}")  # Format to 2 decimal places
            expense_amount_label.grid(row=row, column=1, padx=10, pady=5)

            # Add the expense to the list and save to file
            expenses.append({"name": expense_name, "amount": amount})
            save_expenses(expenses)

            # Update the total expenses
            total_expenses = calculate_total_expenses(expenses)
            total_expenses_label.config(text=f"Total Expenses: {total_expenses:.2f}")  # Format total to 2 decimal places

            # Clear the entry fields
            expense_name_entry.delete(0, tk.END)
            expense_amount_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for the amount.")
    else:
        messagebox.showerror("Missing input", "Please enter both expense name and amount.")

# Function to create the expense page UI and load saved expenses
def create_expense_page(frame):
    # Create a frame for the expense table
    expense_table_frame = tk.Frame(frame)
    expense_table_frame.grid(row=0, column=0, columnspan=2, pady=20)

    # Table headers
    expense_name_header = tk.Label(expense_table_frame, text="Expense Name", font=('bold', 12))
    expense_name_header.grid(row=0, column=0, padx=10, pady=5)

    expense_amount_header = tk.Label(expense_table_frame, text="Amount", font=('bold', 12))
    expense_amount_header.grid(row=0, column=1, padx=10, pady=5)

    # Load expenses and total expenses from the file
    expenses, total_expenses = load_expenses()

    # Display loaded expenses in the table
    for idx, expense in enumerate(expenses, start=1):
        expense_name_label = tk.Label(expense_table_frame, text=expense["name"])
        expense_name_label.grid(row=idx, column=0, padx=10, pady=5)

        expense_amount_label = tk.Label(expense_table_frame, text=f"{expense['amount']:.2f}")  # Format to 2 decimal places
        expense_amount_label.grid(row=idx, column=1, padx=10, pady=5)

    # Entry fields for adding a new expense
    expense_name_label = tk.Label(frame, text="Expense Name:")
    expense_name_label.grid(row=1, column=0, padx=10, pady=5)

    expense_name_entry = tk.Entry(frame)
    expense_name_entry.grid(row=1, column=1, padx=10, pady=5)

    expense_amount_label = tk.Label(frame, text="Expense Amount:")
    expense_amount_label.grid(row=2, column=0, padx=10, pady=5)

    expense_amount_entry = tk.Entry(frame)
    expense_amount_entry.grid(row=2, column=1, padx=10, pady=5)

    # Label to display the total expenses
    total_expenses_label = tk.Label(frame, text=f"Total Expenses: {total_expenses:.2f}", font=('bold', 12))
    total_expenses_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Button to add the expense
    add_expense_button = tk.Button(frame, text="Add Expense", command=lambda: add_expense_entry(expense_table_frame, expense_name_entry, expense_amount_entry, expenses, total_expenses_label))
    add_expense_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Expense Tracker")

    # Create the expense page UI
    create_expense_page(root)

    # Start the Tkinter main loop
    root.mainloop()
