import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class LibraryItem:
    def __init__(self, title, author, category, item_type, is_available=True):
        self.title = title
        self.author = author
        self.category = category
        self.item_type = item_type
        self.is_available = is_available
        self.borrower = None
        self.due_date = None

class LibrarySystem:
    def __init__(self):
        self.catalog = []
        self.fines_per_day = 0.50

    def add_item(self, title, author, category, item_type):
        item = LibraryItem(title, author, category, item_type)
        self.catalog.append(item)

    def checkout_item(self, title, borrower, due_date):
        for item in self.catalog:
            if item.title == title and item.is_available:
                item.is_available = False
                item.borrower = borrower
                item.due_date = due_date
                return True
        return False

    def return_item(self, title, return_date):
        for item in self.catalog:
            if item.title == title and not item.is_available:
                item.is_available = True
                overdue_days = max((return_date - item.due_date).days, 0)
                fine = overdue_days * self.fines_per_day
                item.borrower = None
                item.due_date = None
                return fine, overdue_days
        return None, None

    def search_items(self, query, search_by):
        results = []
        for item in self.catalog:
            if search_by == "title" and query.lower() in item.title.lower():
                results.append(item)
            elif search_by == "author" and query.lower() in item.author.lower():
                results.append(item)
            elif search_by == "category" and query.lower() in item.category.lower():
                results.append(item)
        return results

class LibraryApp:
    def __init__(self, root):
        self.library = LibrarySystem()
        self.root = root
        self.root.title("Library Management System")

        # UI Elements
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.title_label = tk.Label(self.frame, text="Title:")
        self.title_label.grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self.frame)
        self.title_entry.grid(row=0, column=1)

        self.author_label = tk.Label(self.frame, text="Author:")
        self.author_label.grid(row=1, column=0, sticky="w")
        self.author_entry = tk.Entry(self.frame)
        self.author_entry.grid(row=1, column=1)

        self.category_label = tk.Label(self.frame, text="Category:")
        self.category_label.grid(row=2, column=0, sticky="w")
        self.category_entry = tk.Entry(self.frame)
        self.category_entry.grid(row=2, column=1)

        self.type_label = tk.Label(self.frame, text="Type:")
        self.type_label.grid(row=3, column=0, sticky="w")
        self.type_entry = tk.Entry(self.frame)
        self.type_entry.grid(row=3, column=1)

        self.add_button = tk.Button(self.frame, text="Add Item", command=self.add_item)
        self.add_button.grid(row=4, column=0, pady=5)

        self.list_button = tk.Button(self.frame, text="List Items", command=self.list_items)
        self.list_button.grid(row=4, column=1, pady=5)

        self.checkout_label = tk.Label(self.frame, text="Checkout Title:")
        self.checkout_label.grid(row=5, column=0, sticky="w")
        self.checkout_entry = tk.Entry(self.frame)
        self.checkout_entry.grid(row=5, column=1)

        self.borrower_label = tk.Label(self.frame, text="Borrower:")
        self.borrower_label.grid(row=6, column=0, sticky="w")
        self.borrower_entry = tk.Entry(self.frame)
        self.borrower_entry.grid(row=6, column=1)

        self.checkout_button = tk.Button(self.frame, text="Checkout Item", command=self.checkout_item)
        self.checkout_button.grid(row=7, column=0, pady=5)

        self.return_label = tk.Label(self.frame, text="Return Title:")
        self.return_label.grid(row=8, column=0, sticky="w")
        self.return_entry = tk.Entry(self.frame)
        self.return_entry.grid(row=8, column=1)

        self.return_button = tk.Button(self.frame, text="Return Item", command=self.return_item)
        self.return_button.grid(row=9, column=0, pady=5)

    def add_item(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        category = self.category_entry.get()
        item_type = self.type_entry.get()

        if title and author and category and item_type:
            self.library.add_item(title, author, category, item_type)
            messagebox.showinfo("Success", f"Item '{title}' added to the library.")
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    def list_items(self):
        items = self.library.catalog
        if items:
            output = "\n".join(f"- {item.title} by {item.author} ({item.item_type}, {'Available' if item.is_available else 'Checked out'})" for item in items)
            messagebox.showinfo("Catalog", output)
        else:
            messagebox.showinfo("Catalog", "No items in the catalog.")

    def checkout_item(self):
        title = self.checkout_entry.get()
        borrower = self.borrower_entry.get()
        due_date = datetime.now() + timedelta(days=7)

        if self.library.checkout_item(title, borrower, due_date):
            messagebox.showinfo("Success", f"Item '{title}' checked out to {borrower} until {due_date.date()}.")
        else:
            messagebox.showerror("Error", f"Item '{title}' is not available or does not exist.")

    def return_item(self):
        title = self.return_entry.get()
        return_date = datetime.now()

        fine, overdue_days = self.library.return_item(title, return_date)
        if fine is not None:
            messagebox.showinfo("Success", f"Item '{title}' returned. Overdue by {overdue_days} days. Fine: ${fine:.2f}")
        else:
            messagebox.showerror("Error", f"Item '{title}' was not checked out or does not exist.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
