
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
def connect_db():
    return sqlite3.connect("employees.db")

# Create employee table
def create_table():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add employee
def add_employee():
    name = name_entry.get().strip()
    department = dept_entry.get().strip()
    salary = salary_entry.get().strip()
    email = email_entry.get().strip()

    if not all([name, department, salary, email]):
        messagebox.showwarning("Error", "Please fill all fields")
        return

    try:
        salary = float(salary)
        if salary < 0:
            raise ValueError

        conn = connect_db()
        conn.execute(
            "INSERT INTO employees (name, department, salary, email) VALUES (?, ?, ?, ?)",
            (name, department, salary, email)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Employee added successfully")
        clear_fields()
        show_employees()

    except ValueError:
        messagebox.showerror("Error", "Enter a valid salary")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists")

# Display employees
def show_employees():
    for item in tree.get_children():
        tree.delete(item)

    conn = connect_db()
    rows = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

# Delete employee
def delete_employee():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Error", "Select an employee first")
        return

    employee_id = tree.item(selected[0])["values"][0]

    if messagebox.askyesno("Confirm", "Delete this employee?"):
        conn = connect_db()
        conn.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        conn.commit()
        conn.close()

        show_employees()
        messagebox.showinfo("Success", "Employee deleted")

# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Main window
create_table()

root = tk.Tk()
root.title("Employee Management System")
root.geometry("750x550")

title = tk.Label(
    root,
    text="EMPLOYEE MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

form = tk.Frame(root)
form.pack(pady=10)

tk.Label(form, text="Employee Name").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(form, width=30)
name_entry.grid(row=0, column=1)

tk.Label(form, text="Department").grid(row=1, column=0, padx=10, pady=5)
dept_entry = tk.Entry(form, width=30)
dept_entry.grid(row=1, column=1)

tk.Label(form, text="Salary").grid(row=2, column=0, padx=10, pady=5)
salary_entry = tk.Entry(form, width=30)
salary_entry.grid(row=2, column=1)

tk.Label(form, text="Email").grid(row=3, column=0, padx=10, pady=5)
email_entry = tk.Entry(form, width=30)
email_entry.grid(row=3, column=1)

buttons = tk.Frame(root)
buttons.pack(pady=10)

tk.Button(buttons, text="Add Employee", command=add_employee).grid(row=0, column=0, padx=5)
tk.Button(buttons, text="Show Employees", command=show_employees).grid(row=0, column=1, padx=5)
tk.Button(buttons, text="Delete Employee", command=delete_employee).grid(row=0, column=2, padx=5)
tk.Button(buttons, text="Clear Fields", command=clear_fields).grid(row=0, column=3, padx=5)

columns = ("ID", "Name", "Department", "Salary", "Email")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130)

tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

show_employees()

root.mainloop()
