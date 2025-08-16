import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import re
import csv
import matplotlib.pyplot as plt

expenses_list = []

root = tk.Tk()
root.title("💳 Personal Finance Tracker 💰")
root.geometry("400x600")
root.configure(bg="#FDEBD0")

# ================== Home Page Labels ==================
label = tk.Label(root, text="🏠 Home Page / Menu Page 🏠", font=("Times New Roman", 20, "bold"), fg="#5D6D7E", bg="#FDEBD0")
label.pack(pady=20)

label1 = tk.Label(root, text="Choose an option:", font=("Times New Roman", 14, "bold"), fg="#4A235A", bg="#FDEBD0")
label1.pack(pady=10)


# ================== Helper: Back to Menu ==================
def back_to_menu(window):
    window.destroy()


# ================== Add Expenses ==================
def add_expenses():
    add_window = tk.Toplevel(root)
    add_window.title("➕ Add Expense")
    add_window.geometry("350x400")
    add_window.configure(bg="#E8F8F5")

    tk.Label(add_window, text="Add Expense Details", font=("Times New Roman", 16, "bold"),
             bg="#E8F8F5", fg="#117A65").pack(pady=10)

    tk.Label(add_window, text="Category:", bg="#E8F8F5").pack()
    category_entry = tk.Entry(add_window)
    category_entry.pack(pady=5)

    tk.Label(add_window, text="Amount:", bg="#E8F8F5").pack()
    amount_entry = tk.Entry(add_window)
    amount_entry.pack(pady=5)

    tk.Label(add_window, text="Date (YYYY-MM-DD):", bg="#E8F8F5").pack()
    date_entry = tk.Entry(add_window)
    date_entry.pack(pady=5)

    tk.Label(add_window, text="Code_no:", bg="#E8F8F5").pack()
    code_entry = tk.Entry(add_window)
    code_entry.pack(pady=5)

    def submit_expense():
        category = category_entry.get().strip()
        amount = amount_entry.get().strip()
        date = date_entry.get().strip()
        code = code_entry.get().strip()

        if not category.isalpha():
            messagebox.showerror("Input Error", "Category must only contain letters.")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
            return
        try:
            code = int(code)
        except ValueError:
            messagebox.showerror("Input Error", "Code No. must be a number.")
            return
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
            return

        expenses_list.append({
            "Category": category,
            "Amount": amount,
            "Date": date,
            "Code_no": code
        })
        messagebox.showinfo("Success", "Expense added successfully!")
        add_window.destroy()

    tk.Button(add_window, text="✅ Submit", bg="#82E0AA", font=("Times New Roman", 12, "bold"),
              command=submit_expense).pack(pady=20)
    tk.Button(add_window, text="⬅ Back to Menu", bg="#FAD7A0", command=lambda: back_to_menu(add_window)).pack()


# ================== Display Expenses ==================
def display_expenses():
    if not expenses_list:
        messagebox.showinfo("No Data", "No expenses to display yet.")
        return

    display_window = tk.Toplevel(root)
    display_window.title("📋 Your Expenses")
    display_window.geometry("450x300")
    display_window.configure(bg="#FDFEFE")

    tk.Label(display_window, text="📋 Expenses List", font=("Times New Roman", 16, "bold"),
             bg="#FDFEFE", fg="#2E4053").pack(pady=10)

    tree = ttk.Treeview(display_window, columns=("Category", "Amount", "Date", "Code_no"), show="headings")
    for col in ("Category", "Amount", "Date", "Code_no"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    for expense in expenses_list:
        tree.insert("", "end", values=(expense["Category"], expense["Amount"], expense["Date"], expense["Code_no"]))
    tree.pack(pady=10)

    tk.Button(display_window, text="⬅ Back to Menu", bg="#FAD7A0", command=lambda: back_to_menu(display_window)).pack()


# ================== Search Expenses ==================
def search_expenses():
    if not expenses_list:
        messagebox.showinfo("No Data", "No expenses to search.")
        return

    search_window = tk.Toplevel(root)
    search_window.title("🔍 Search Expense by Code No.")
    search_window.geometry("350x250")
    search_window.configure(bg="#FEF9E7")

    tk.Label(search_window, text="Enter Code No. to Search:", font=("Times New Roman", 12, "bold"),
             bg="#FEF9E7", fg="#7D6608").pack(pady=10)

    code_entry = tk.Entry(search_window)
    code_entry.pack(pady=5)

    def perform_search():
        code = code_entry.get().strip()
        if not code.isdigit():
            messagebox.showerror("Input Error", "Code No. must be a number.")
            return
        code = int(code)
        found = False

        result_window = tk.Toplevel(search_window)
        result_window.title("📄 Search Results")
        result_window.geometry("450x200")
        result_window.configure(bg="#FDFEFE")

        tree = ttk.Treeview(result_window, columns=("Category", "Amount", "Date", "Code_no"), show="headings")
        for col in ("Category", "Amount", "Date", "Code_no"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        for expense in expenses_list:
            if expense["Code_no"] == code:
                tree.insert("", "end", values=(expense["Category"], expense["Amount"], expense["Date"], expense["Code_no"]))
                found = True
        tree.pack(pady=10)

        if not found:
            tk.Label(result_window, text="❌ No expense found with that Code No.",
                     font=("Times New Roman", 12, "bold"), fg="red", bg="#FDFEFE").pack(pady=10)

        tk.Button(result_window, text="⬅ Back to Menu", bg="#FAD7A0", command=lambda: back_to_menu(result_window)).pack()

    tk.Button(search_window, text="🔎 Search", bg="#F9E79F", font=("Times New Roman", 12, "bold"),
              command=perform_search).pack(pady=15)
    tk.Button(search_window, text="⬅ Back to Menu", bg="#FAD7A0", command=lambda: back_to_menu(search_window)).pack()


# ================== Delete Expenses ==================
def delete_expenses():
    if not expenses_list:
        messagebox.showinfo("No Data", "No expenses to delete yet.")
        return

    delete_window = tk.Toplevel(root)
    delete_window.title("🗑️ Delete Expense")
    delete_window.geometry("350x200")
    delete_window.configure(bg="#FDEDEC")

    tk.Label(delete_window, text="Enter Code No. to Delete:", font=("Times New Roman", 12),
             bg="#FDEDEC", fg="#922B21").pack(pady=10)

    code_entry = tk.Entry(delete_window)
    code_entry.pack(pady=5)

    def delete_by_code():
        code = code_entry.get().strip()
        if not code.isdigit():
            messagebox.showerror("Input Error", "Code No. must be a number.")
            return
        code = int(code)
        for i, expense in enumerate(expenses_list):
            if expense.get("Code_no") == code:
                confirm = messagebox.askyesno("Confirm Delete", f"Delete:\n{expense}")
                if confirm:
                    del expenses_list[i]
                    messagebox.showinfo("Deleted", "Expense deleted successfully.")
                    delete_window.destroy()
                return
        messagebox.showinfo("Not Found", "No expense found with that Code No.")

    tk.Button(delete_window, text="🗑️ Delete", bg="#F5B7B1", font=("Times New Roman", 12, "bold"),
              command=delete_by_code).pack(pady=20)
    tk.Button(delete_window, text="⬅ Back to Menu", bg="#FAD7A0", command=lambda: back_to_menu(delete_window)).pack()


# ================== Save to CSV ==================
def save_expenses():
    if not expenses_list:
        messagebox.showinfo("No Data", "No expenses to save.")
        return
    with open("expenses.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Category", "Amount", "Date", "Code_no"])
        writer.writeheader()
        writer.writerows(expenses_list)
    messagebox.showinfo("Saved", "Expenses saved to 'expenses.csv'.")


# ================== Visualize Expenses ==================
def visualize_expense():
    if not expenses_list:
        messagebox.showinfo("No Data", "No expenses to visualize.")
        return

    code = simpledialog.askstring("Visualize Expense", "Enter Code No. to visualize:")
    if not code or not code.isdigit():
        return
    code = int(code)

    for expense in expenses_list:
        if expense["Code_no"] == code:
            plt.bar(["Amount"], [expense["Amount"]])
            plt.title(f"Expense for {expense['Category']} ({expense['Date']})")
            plt.ylabel("Amount")
            plt.show()
            return
    messagebox.showinfo("Not Found", "No expense found with that Code No.")


# ================== Buttons ==================
tk.Button(root, text="➕ Add Expenses", bg="#ABEBC6", fg="#1D8348", command=add_expenses).pack(pady=10)
tk.Button(root, text="📓 Display Expenses", bg="#AED6F1", fg="#154360", command=display_expenses).pack(pady=10)
tk.Button(root, text="🔍 Search Expenses", bg="#F9E79F", fg="#7D6608", command=search_expenses).pack(pady=10)
tk.Button(root, text="🍂 Delete Expenses", bg="#F5B7B1", fg="#922B21", command=delete_expenses).pack(pady=10)
tk.Button(root, text="📊 Visualize Expenses", bg="#D2B4DE", fg="#4A235A", command=visualize_expense).pack(pady=10)
tk.Button(root, text="💾 Save Expenses", bg="#A3E4D7", fg="#117864", command=save_expenses).pack(pady=10)
tk.Button(root, text="🖚 Exit", bg="#FADBD8", fg="#641E16", command=root.destroy).pack(pady=20)

root.mainloop()
