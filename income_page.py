import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store income data
DATA_FILE = "incomes_data.json"

# Function to save incomes and total incomes to the JSON file
def save_incomes(incomes):
    total_incomes = calculate_total_incomes(incomes)
    data = {"incomes": incomes, "total_incomes": total_incomes}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Function to load incomes from the JSON file
def load_incomes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("incomes", []), data.get("total_incomes", 0)
    return [], 0  # Return an empty list and 0 total if file does not exist

# Function to calculate the total sum of all incomes
def calculate_total_incomes(incomes):
    return sum(income["amount"] for income in incomes)

# Function to add a new income to the table and save it to the file
def add_income_entry(income_table_frame, income_name_entry, income_amount_entry, incomes, total_incomes_label):
    income_name = income_name_entry.get().strip()  # Strip whitespace
    income_amount = income_amount_entry.get().strip()  # Strip whitespace

    if income_name and income_amount:
        try:
            # Convert amount to float to validate
            amount = float(income_amount)

            # Add the income to the table
            row = len(incomes) + 1  # Get the next row number
            income_name_label = tk.Label(income_table_frame, text=income_name)
            income_name_label.grid(row=row, column=0, padx=10, pady=5)

            income_amount_label = tk.Label(income_table_frame, text=f"{amount:.2f}")  # Format to 2 decimal places
            income_amount_label.grid(row=row, column=1, padx=10, pady=5)

            # Add the income to the list and save to file
            incomes.append({"name": income_name, "amount": amount})
            save_incomes(incomes)

            # Update the total incomes
            total_incomes = calculate_total_incomes(incomes)
            total_incomes_label.config(text=f"Total incomes: {total_incomes:.2f}")  # Format total to 2 decimal places

            # Clear the entry fields
            income_name_entry.delete(0, tk.END)
            income_amount_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for the amount.")
    else:
        messagebox.showerror("Missing input", "Please enter both income name and amount.")

# Function to create the income page UI and load saved incomes
def create_income_page(frame):
    # Create a frame for the income table
    income_table_frame = tk.Frame(frame)
    income_table_frame.grid(row=0, column=0, columnspan=2, pady=20)

    # Table headers
    income_name_header = tk.Label(income_table_frame, text="Income Name", font=('bold', 12))
    income_name_header.grid(row=0, column=0, padx=10, pady=5)

    income_amount_header = tk.Label(income_table_frame, text="Amount", font=('bold', 12))
    income_amount_header.grid(row=0, column=1, padx=10, pady=5)

    # Load incomes and total incomes from the file
    incomes, total_incomes = load_incomes()

    # Display loaded incomes in the table
    for idx, income in enumerate(incomes, start=1):
        income_name_label = tk.Label(income_table_frame, text=income["name"])
        income_name_label.grid(row=idx, column=0, padx=10, pady=5)

        income_amount_label = tk.Label(income_table_frame, text=f"{income['amount']:.2f}")  # Format to 2 decimal places
        income_amount_label.grid(row=idx, column=1, padx=10, pady=5)

    # Entry fields for adding a new income
    income_name_label = tk.Label(frame, text="Income Name:")
    income_name_label.grid(row=1, column=0, padx=10, pady=5)

    income_name_entry = tk.Entry(frame)
    income_name_entry.grid(row=1, column=1, padx=10, pady=5)

    income_amount_label = tk.Label(frame, text="Income Amount:")
    income_amount_label.grid(row=2, column=0, padx=10, pady=5)

    income_amount_entry = tk.Entry(frame)
    income_amount_entry.grid(row=2, column=1, padx=10, pady=5)

    # Label to display the total incomes
    total_incomes_label = tk.Label(frame, text=f"Total incomes: {total_incomes:.2f}", font=('bold', 12))
    total_incomes_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Button to add the income
    add_income_button = tk.Button(frame, text="Add Income", command=lambda: add_income_entry(income_table_frame, income_name_entry, income_amount_entry, incomes, total_incomes_label))
    add_income_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Income Tracker")

    # Create the income page UI
    create_income_page(root)

    # Start the Tkinter main loop
    root.mainloop()
