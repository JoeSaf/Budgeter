import tkinter as tk
from tkinter import messagebox
from expense_page import create_expense_page
from income_page import create_income_page
from balance_page import create_balance_page
from balance_page import calculate_balance
from savings_page import create_savings_page
import json
from datetime import datetime, timedelta
import os

# File to store user data for countdown timer
DATA_FILE = "financial_data.json"

# Function to save the financial month start date and duration
def save_data(start_date, month_length):
    data = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "month_length": month_length
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Function to load the saved data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return None

# Function to calculate remaining days
def calculate_remaining_days(start_date, month_length):
    today = datetime.now()
    end_date = start_date + timedelta(days=month_length)
    remaining_days = (end_date - today).days
    return remaining_days

# Countdown timer logic
def start_countdown():
    try:
        month_length = int(month_length_entry.get())
        start_date = datetime.now()
        save_data(start_date, month_length)
        update_display()
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number of days.")

# Function to update the display based on remaining days
def update_display():
    data = load_data()
    if data:
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        month_length = data["month_length"]
        remaining_days = calculate_remaining_days(start_date, month_length)
        
        if remaining_days >= 0:
            result_label.config(text=f"Remaining days: {remaining_days}")
        else:
            result_label.config(text="The financial month has ended.")
    else:
        result_label.config(text="No data found. Please enter month length.")

# Switching between frames
def show_frame(frame):
    frame.tkraise()

# Create the main window
root = tk.Tk()
root.title("Budgeter")
root.geometry("480x480")

# Define frames for different pages
budget_frame = tk.Frame(root)
countdown_frame = tk.Frame(root)
add_income_frame = tk.Frame(root)
add_expense_frame = tk.Frame(root)
calculate_balance_frame = tk.Frame(root)
set_savings_goal_frame = tk.Frame(root)

for frame in (budget_frame, countdown_frame, add_income_frame, add_expense_frame, calculate_balance_frame, set_savings_goal_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Budget management page (budget_frame)
def add_income():
    pass  # Placeholder for adding income logic

def add_expense():
    pass  # Placeholder for adding expense logic

def set_savings_goal():
    pass  # Placeholder for setting savings goal logic

#Balance display
balance_label = tk.Label(budget_frame, text="Your Current Balance:")
balance_label.grid(row=3, column=0, padx=10, pady=10)

current_balance_label = tk.Label(frame, font=('bold', 14))
balance_label = current_balance_label
current_balance = calculate_balance()

color_balance = current_balance

#balance_display = tk.Label(budget_frame, text=f"Tsh {color_balance}")  # Placeholder for balance display
if color_balance < 0:
    balance_display = tk.Label(budget_frame, text=f"Tsh {color_balance}", fg="red")
else:
    balance_display = tk.Label(budget_frame, text=f"Tsh {color_balance}", fg="blue")
balance_display.grid(row=3, column=1, padx=10, pady=10)


# Buttons for budget management
income_button = tk.Button(budget_frame, text="Add Income", command=lambda: show_frame(add_income_frame))
income_button.grid(row=4, column=0, padx=10, pady=10)

expense_button = tk.Button(budget_frame, text="Add Expense", command=lambda: show_frame(add_expense_frame))
expense_button.grid(row=4, column=1, padx=10, pady=10)

calculate_button = tk.Button(budget_frame, text="Calculate Balance", command=lambda: show_frame(calculate_balance_frame))
calculate_button.grid(row=5, column=0, padx=10, pady=10)

goal_button = tk.Button(budget_frame, text="Set Savings Goal", command=lambda: show_frame(set_savings_goal_frame))
goal_button.grid(row=5, column=1, padx=10, pady=10)

# Mini pages for each function

# Add Income Page
add_income_label = tk.Label(add_income_frame, text="Add your income here:")
create_income_page(add_income_frame)

# Add Expense Page
add_expense_label = tk.Label(add_expense_frame, text="Add your expense here:")
create_expense_page(add_expense_frame)

# Calculate Balance Page
calculate_balance_label = tk.Label(calculate_balance_frame, text="Calculate your balance here:")
create_balance_page(calculate_balance_frame)

# Set Savings Goal Page
set_savings_goal_label = tk.Label(set_savings_goal_frame, text="Set your savings goal here:")
create_savings_page(set_savings_goal_frame)

# Countdown timer page (countdown_frame)
month_length_label = tk.Label(countdown_frame, text="Enter financial month length (days):")
month_length_label.pack(pady=10)

month_length_entry = tk.Entry(countdown_frame)
month_length_entry.pack(pady=10)

start_button = tk.Button(countdown_frame, text="Start Countdown", command=start_countdown)
start_button.pack(pady=10)

result_label = tk.Label(countdown_frame, text="")
result_label.pack(pady=10)

# Menu setup
menu = tk.Menu(root)
root.config(menu=menu)

# File menu
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Navigation menu for switching between pages
nav_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Navigate", menu=nav_menu)
nav_menu.add_command(label="Budget Management", command=lambda: show_frame(budget_frame))
nav_menu.add_command(label="Financial Countdown", command=lambda: show_frame(countdown_frame))
nav_menu.add_command(label="Add Income", command=lambda: show_frame(add_income_frame))
nav_menu.add_command(label="Add Expense", command=lambda: show_frame(add_expense_frame))
nav_menu.add_command(label="Calculate Balance", command=lambda: show_frame(calculate_balance_frame))
nav_menu.add_command(label="Set Savings Goal", command=lambda: show_frame(set_savings_goal_frame))

# Help menu
help_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Money Management Program v1.0"))

# Load and display remaining days on countdown page startup
update_display()

# Show the budget frame initially
show_frame(budget_frame)

# Start the Tkinter main loop
root.mainloop()
