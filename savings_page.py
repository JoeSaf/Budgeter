import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta

# File to store savings data
DATA_FILE = "savings_data.json"

# Function to save savings and total savings to the JSON file
def save_savings(savings):
    total_savings = calculate_total_savings(savings)
    data = {"savings": savings, "total_savings": total_savings}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Function to load savings from the JSON file
def load_savings():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("savings", []), data.get("total_savings", 0)
    return [], 0  # Return an empty list and 0 total if file does not exist

# Function to calculate the total sum of all savings
def calculate_total_savings(savings):
    return sum(saving["amount"] for saving in savings)

# Function to add a new savings entry to the table and save it to the file
def add_savings_entry(savings_table_frame, savings_name_entry, savings_amount_entry, savings, total_savings_label):
    savings_name = savings_name_entry.get().strip()  # Strip whitespace
    savings_amount = savings_amount_entry.get().strip()  # Strip whitespace

    if savings_name and savings_amount:
        try:
            # Convert amount to float to validate
            amount = float(savings_amount)

            # Add the savings to the table
            row = len(savings) + 1  # Get the next row number
            savings_name_label = tk.Label(savings_table_frame, text=savings_name)
            savings_name_label.grid(row=row, column=0, padx=10, pady=5)

            savings_amount_label = tk.Label(savings_table_frame, text=f"{amount:.2f}")  # Format to 2 decimal places
            savings_amount_label.grid(row=row, column=1, padx=10, pady=5)

            # Add the savings to the list and save to file
            savings.append({"name": savings_name, "amount": amount})
            save_savings(savings)

            # Update the total savings
            total_savings = calculate_total_savings(savings)
            total_savings_label.config(text=f"Total savings: {total_savings:.2f}")  # Format total to 2 decimal places

            # Clear the entry fields
            savings_name_entry.delete(0, tk.END)
            savings_amount_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for the amount.")
    else:
        messagebox.showerror("Missing input", "Please enter both savings name and amount.")

# Function to create the savings page UI and load saved savings
def create_savings_page(frame):
    # Create a frame for the savings table
    savings_table_frame = tk.Frame(frame)
    savings_table_frame.grid(row=0, column=0, columnspan=2, pady=20)

    # Table headers
    savings_name_header = tk.Label(savings_table_frame, text="Savings Name", font=('bold', 12))
    savings_name_header.grid(row=0, column=0, padx=10, pady=5)

    savings_amount_header = tk.Label(savings_table_frame, text="Amount", font=('bold', 12))
    savings_amount_header.grid(row=0, column=1, padx=10, pady=5)

    # Load savings and total savings from the file
    savings, total_savings = load_savings()

    # Display loaded savings in the table
    for idx, saving in enumerate(savings, start=1):
        savings_name_label = tk.Label(savings_table_frame, text=saving["name"])
        savings_name_label.grid(row=idx, column=0, padx=10, pady=5)

        savings_amount_label = tk.Label(savings_table_frame, text=f"{saving['amount']:.2f}")  # Format to 2 decimal places
        savings_amount_label.grid(row=idx, column=1, padx=10, pady=5)

    # Entry fields for adding a new savings entry
    savings_name_label = tk.Label(frame, text="Savings Name:")
    savings_name_label.grid(row=1, column=0, padx=10, pady=5)

    savings_name_entry = tk.Entry(frame)
    savings_name_entry.grid(row=1, column=1, padx=10, pady=5)

    savings_amount_label = tk.Label(frame, text="Savings Amount:")
    savings_amount_label.grid(row=2, column=0, padx=10, pady=5)

    savings_amount_entry = tk.Entry(frame)
    savings_amount_entry.grid(row=2, column=1, padx=10, pady=5)

    # Label to display the total savings
    total_savings_label = tk.Label(frame, text=f"Total savings: {total_savings:.2f}", font=('bold', 12))
    total_savings_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Button to add the savings
    add_savings_button = tk.Button(frame, text="Add Savings", command=lambda: add_savings_entry(savings_table_frame, savings_name_entry, savings_amount_entry, savings, total_savings_label))
    add_savings_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Savings Tracker")

    # Create the savings page UI
    create_savings_page(root)

    # Start the Tkinter main loop
    root.mainloop()
