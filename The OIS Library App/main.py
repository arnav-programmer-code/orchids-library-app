import customtkinter as ctk
import json
import os
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import tkinter.messagebox as msgbox


class OrchidsLibraryApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("ORCHIDS Library Management System")
        self.root.geometry("1200x800")
        self.root.configure(fg_color=("#ffffff", "#2b2b2b"))

        # Data files
        self.users_file = "users.json"
        self.books_file = "books.json"
        self.borrowed_file = "borrowed_books.json"

        # Current user
        self.current_user = None
        self.is_admin = False

        # Initialize data
        self.init_data()

        # Load logo
        self.load_logo()

        # Setup UI
        self.setup_login_screen()

    def load_logo(self):
        try:
            # Create a simple orchid-like logo if ORCHIDS.png doesn't exist
            self.logo_image = ctk.CTkImage(
                light_image=Image.new('RGB', (80, 80), '#dc2626'),
                dark_image=Image.new('RGB', (80, 80), '#dc2626'),
                size=(80, 80)
            )
            if os.path.exists("ORCHIDS.png"):
                img = Image.open("ORCHIDS.png")
                self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
        except:
            self.logo_image = None

    def init_data(self):
        # Initialize users data
        if not os.path.exists(self.users_file):
            users_data = {
                "admin": {"password": "admin123", "role": "admin", "name": "Administrator"},
                "student1": {"password": "pass123", "role": "student", "name": "John Doe"},
                "student2": {"password": "pass456", "role": "student", "name": "Jane Smith"}
            }
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=2)

        # Initialize books data
        if not os.path.exists(self.books_file):
            books_data = {
                "1": {"title": "Python Programming", "author": "John Smith", "isbn": "978-0123456789",
                      "available": True},
                "2": {"title": "Data Science Basics", "author": "Mary Johnson", "isbn": "978-0987654321",
                      "available": True},
                "3": {"title": "Machine Learning", "author": "Bob Wilson", "isbn": "978-0456789123", "available": True}
            }
            with open(self.books_file, 'w') as f:
                json.dump(books_data, f, indent=2)

        # Initialize borrowed books data
        if not os.path.exists(self.borrowed_file):
            with open(self.borrowed_file, 'w') as f:
                json.dump({}, f, indent=2)

    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_data(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def setup_login_screen(self):
        self.clear_screen()

        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=20)
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # Header with logo
        header_frame = ctk.CTkFrame(main_frame, fg_color="#dc2626", corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=20)

        if self.logo_image:
            logo_label = ctk.CTkLabel(header_frame, image=self.logo_image, text="")
            logo_label.pack(pady=10)

        title_label = ctk.CTkLabel(header_frame, text="ORCHIDS", font=ctk.CTkFont(size=36, weight="bold"),
                                   text_color="white")
        title_label.pack(pady=(0, 5))

        subtitle_label = ctk.CTkLabel(header_frame, text="Professional Library Management System",
                                      font=ctk.CTkFont(size=16), text_color="white")
        subtitle_label.pack(pady=(0, 15))

        # Login form
        login_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        login_frame.pack(expand=True, pady=30)

        ctk.CTkLabel(login_frame, text="Login to Library", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#dc2626").pack(pady=20)

        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=300, height=40)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=300, height=40)
        self.password_entry.pack(pady=10)

        login_btn = ctk.CTkButton(login_frame, text="Login", command=self.login,
                                  fg_color="#dc2626", hover_color="#b91c1c", width=300, height=40)
        login_btn.pack(pady=20)

        self.password_entry.bind("<Return>", lambda e: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        users = self.load_data(self.users_file)

        if username in users and users[username]["password"] == password:
            self.current_user = username
            self.is_admin = users[username]["role"] == "admin"

            if self.is_admin:
                self.setup_admin_dashboard()
            else:
                self.setup_student_dashboard()
        else:
            msgbox.showerror("Error", "Invalid username or password!")

    def setup_student_dashboard(self):
        self.clear_screen()

        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=20)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#dc2626", corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_content, text="Student Dashboard", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="white").pack(side="left")

        ctk.CTkButton(header_content, text="Logout", command=self.logout,
                      fg_color="white", text_color="#dc2626", hover_color="#f3f4f6").pack(side="right")

        # Navigation
        nav_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(nav_frame, text="Book Catalog", command=self.show_book_catalog,
                      fg_color="#dc2626", hover_color="#b91c1c").pack(side="left", padx=(0, 10))

        ctk.CTkButton(nav_frame, text="My Books", command=self.show_my_books,
                      fg_color="#6b7280", hover_color="#4b5563").pack(side="left")

        # Content area
        self.content_frame = ctk.CTkScrollableFrame(main_frame)
        self.content_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.show_book_catalog()

    def setup_admin_dashboard(self):
        self.clear_screen()

        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=20)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#dc2626", corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_content, text="Admin Dashboard", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="white").pack(side="left")

        ctk.CTkButton(header_content, text="Logout", command=self.logout,
                      fg_color="white", text_color="#dc2626", hover_color="#f3f4f6").pack(side="right")

        # Navigation
        nav_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(nav_frame, text="Books", command=self.show_admin_books,
                      fg_color="#dc2626", hover_color="#b91c1c").pack(side="left", padx=(0, 10))

        ctk.CTkButton(nav_frame, text="Add Book", command=self.show_add_book,
                      fg_color="#16a34a", hover_color="#15803d").pack(side="left", padx=(0, 10))

        ctk.CTkButton(nav_frame, text="Issue Book", command=self.show_issue_book,
                      fg_color="#f59e0b", hover_color="#d97706").pack(side="left", padx=(0, 10))

        ctk.CTkButton(nav_frame, text="Manage Students", command=self.show_student_management,
                      fg_color="#2563eb", hover_color="#1d4ed8").pack(side="left")

        # Content area
        self.content_frame = ctk.CTkScrollableFrame(main_frame)
        self.content_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.show_admin_books()

    def show_book_catalog(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="Available Books", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#dc2626").pack(pady=(0, 20))

        books = self.load_data(self.books_file)

        for book_id, book in books.items():
            if book["available"]:
                book_frame = ctk.CTkFrame(self.content_frame, fg_color="#f9f9f9", corner_radius=10)
                book_frame.pack(fill="x", pady=5, padx=10)

                content = ctk.CTkFrame(book_frame, fg_color="transparent")
                content.pack(fill="x", padx=20, pady=15)

                ctk.CTkLabel(content, text=book["title"], font=ctk.CTkFont(size=16, weight="bold"),
                             text_color="#dc2626").pack(anchor="w")
                ctk.CTkLabel(content, text=f"Author: {book['author']}", text_color="#666").pack(anchor="w")
                ctk.CTkLabel(content, text=f"ISBN: {book['isbn']}", text_color="#666").pack(anchor="w")

    def show_my_books(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="My Books", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#dc2626").pack(pady=(0, 20))

        borrowed = self.load_data(self.borrowed_file)
        books = self.load_data(self.books_file)

        user_books = [b for b in borrowed.values() if b["student"] == self.current_user]

        if not user_books:
            ctk.CTkLabel(self.content_frame, text="No books borrowed", text_color="#666").pack(pady=20)
            return

        for borrow in user_books:
            book = books[borrow["book_id"]]
            book_frame = ctk.CTkFrame(self.content_frame, fg_color="#f9f9f9", corner_radius=10)
            book_frame.pack(fill="x", pady=5, padx=10)

            content = ctk.CTkFrame(book_frame, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(content, text=book["title"], font=ctk.CTkFont(size=16, weight="bold"),
                         text_color="#dc2626").pack(anchor="w")

            due_date = datetime.strptime(borrow["due_date"], "%Y-%m-%d")
            is_overdue = datetime.now() > due_date

            status_color = "#ef4444" if is_overdue else "#16a34a"
            status_text = "OVERDUE" if is_overdue else "Active"

            ctk.CTkLabel(content, text=f"Due: {borrow['due_date']} - {status_text}",
                         text_color=status_color).pack(anchor="w")

            if borrow.get("fine", 0) > 0:
                ctk.CTkLabel(content, text=f"Fine: ${borrow['fine']}",
                             text_color="#ef4444", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

    def show_admin_books(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="All Books", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#dc2626").pack(pady=(0, 20))

        books = self.load_data(self.books_file)

        for book_id, book in books.items():
            book_frame = ctk.CTkFrame(self.content_frame, fg_color="#f9f9f9", corner_radius=10)
            book_frame.pack(fill="x", pady=5, padx=10)

            content = ctk.CTkFrame(book_frame, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=15)

            info_frame = ctk.CTkFrame(content, fg_color="transparent")
            info_frame.pack(fill="x")

            ctk.CTkLabel(info_frame, text=book["title"], font=ctk.CTkFont(size=16, weight="bold"),
                         text_color="#dc2626").pack(anchor="w", side="left")

            status = "Available" if book["available"] else "Borrowed"
            status_color = "#16a34a" if book["available"] else "#ef4444"

            ctk.CTkLabel(info_frame, text=status, text_color=status_color,
                         font=ctk.CTkFont(weight="bold")).pack(anchor="e", side="right")

            ctk.CTkLabel(content, text=f"Author: {book['author']} | ISBN: {book['isbn']}",
                         text_color="#666").pack(anchor="w")

            if not book["available"]:
                # Show who borrowed it
                borrowed = self.load_data(self.borrowed_file)
                for borrow in borrowed.values():
                    if borrow["book_id"] == book_id:
                        ctk.CTkLabel(content, text=f"Borrowed by: {borrow['student']}",
                                     text_color="#666").pack(anchor="w")
                        break

    def show_add_book(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="Add New Book", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#dc2626").pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#f9f9f9", corner_radius=10)
        form_frame.pack(fill="x", padx=50, pady=20)

        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="x", padx=30, pady=30)

        ctk.CTkLabel(form_content, text="Title:").pack(anchor="w", pady=(0, 5))
        title_entry = ctk.CTkEntry(form_content, width=400)
        title_entry.pack(pady=(0, 15))

        ctk.CTkLabel(form_content, text="Author:").pack(anchor="w", pady=(0, 5))
        author_entry = ctk.CTkEntry(form_content, width=400)
        author_entry.pack(pady=(0, 15))

        ctk.CTkLabel(form_content, text="ISBN:").pack(anchor="w", pady=(0, 5))
        isbn_entry = ctk.CTkEntry(form_content, width=400)
        isbn_entry.pack(pady=(0, 20))

        def add_book():
            if title_entry.get() and author_entry.get() and isbn_entry.get():
                books = self.load_data(self.books_file)
                new_id = str(max([int(k) for k in books.keys()], default=0) + 1)

                books[new_id] = {
                    "title": title_entry.get(),
                    "author": author_entry.get(),
                    "isbn": isbn_entry.get(),
                    "available": True
                }

                self.save_data(self.books_file, books)
                msgbox.showinfo("Success", "Book added successfully!")
                self.show_admin_books()
            else:
                msgbox.showerror("Error", "Please fill all fields!")

        ctk.CTkButton(form_content, text="Add Book", command=add_book,
                      fg_color="#16a34a", hover_color="#15803d").pack()

    def show_issue_book(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="Issue Book to Student", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#dc2626").pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#f9f9f9", corner_radius=10)
        form_frame.pack(fill="x", padx=50, pady=20)

        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="x", padx=30, pady=30)

        # Student selection
        ctk.CTkLabel(form_content, text="Select Student:").pack(anchor="w", pady=(0, 5))
        users = self.load_data(self.users_file)
        students = {user: info["name"] for user, info in users.items() if info["role"] == "student"}
        student_var = ctk.StringVar()
        student_dropdown = ctk.CTkComboBox(form_content, values=list(students.keys()),
                                           variable=student_var, width=400)
        student_dropdown.pack(pady=(0, 15))

        # Book selection
        ctk.CTkLabel(form_content, text="Select Book:").pack(anchor="w", pady=(0, 5))
        books = self.load_data(self.books_file)
        available_books = {book_id: book["title"] for book_id, book in books.items() if book["available"]}
        book_var = ctk.StringVar()
        book_dropdown = ctk.CTkComboBox(form_content, values=list(available_books.values()),
                                        variable=book_var, width=400)
        book_dropdown.pack(pady=(0, 15))

        # Due date (default 14 days from now)
        ctk.CTkLabel(form_content, text="Due Date (YYYY-MM-DD):").pack(anchor="w", pady=(0, 5))
        due_date_entry = ctk.CTkEntry(form_content, width=400)
        default_due = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        due_date_entry.insert(0, default_due)
        due_date_entry.pack(pady=(0, 20))

        def issue_book():
            student = student_var.get()
            book_title = book_var.get()
            due_date = due_date_entry.get()

            if not student or not book_title or not due_date:
                msgbox.showerror("Error", "Please fill all fields!")
                return

            # Find book ID by title
            book_id = None
            for bid, book in books.items():
                if book["title"] == book_title and book["available"]:
                    book_id = bid
                    break

            if not book_id:
                msgbox.showerror("Error", "Selected book is not available!")
                return

            try:
                # Validate date format
                datetime.strptime(due_date, "%Y-%m-%d")

                # Update book availability
                books[book_id]["available"] = False
                self.save_data(self.books_file, books)

                # Add to borrowed books
                borrowed = self.load_data(self.borrowed_file)
                borrow_id = str(len(borrowed) + 1)
                borrowed[borrow_id] = {
                    "book_id": book_id,
                    "student": student,
                    "issue_date": datetime.now().strftime("%Y-%m-%d"),
                    "due_date": due_date,
                    "fine": 0
                }
                self.save_data(self.borrowed_file, borrowed)

                msgbox.showinfo("Success", f"Book '{book_title}' issued to {students[student]} successfully!")
                self.show_admin_books()

            except ValueError:
                msgbox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")

        ctk.CTkButton(form_content, text="Issue Book", command=issue_book,
                      fg_color="#f59e0b", hover_color="#d97706").pack()

    def show_student_management(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="Student Management", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#dc2626").pack(pady=(0, 20))

        borrowed = self.load_data(self.borrowed_file)
        books = self.load_data(self.books_file)
        users = self.load_data(self.users_file)

        for borrow_id, borrow in borrowed.items():
            book = books[borrow["book_id"]]
            student_name = users[borrow["student"]]["name"]

            student_frame = ctk.CTkFrame(self.content_frame, fg_color="#f9f9f9", corner_radius=10)
            student_frame.pack(fill="x", pady=5, padx=10)

            content = ctk.CTkFrame(student_frame, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(content, text=f"{student_name} - {book['title']}",
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="#dc2626").pack(anchor="w")

            due_date = datetime.strptime(borrow["due_date"], "%Y-%m-%d")
            is_overdue = datetime.now() > due_date

            info_text = f"Due: {borrow['due_date']}"
            if borrow.get("fine", 0) > 0:
                info_text += f" | Fine: ${borrow['fine']}"

            ctk.CTkLabel(content, text=info_text, text_color="#666").pack(anchor="w")

            btn_frame = ctk.CTkFrame(content, fg_color="transparent")
            btn_frame.pack(anchor="w", pady=(10, 0))

            def return_book(bid=borrow_id):
                self.return_book(bid)

            def apply_fine(bid=borrow_id):
                self.apply_fine(bid)

            ctk.CTkButton(btn_frame, text="Return Book", command=return_book,
                          fg_color="#16a34a", hover_color="#15803d", width=100).pack(side="left", padx=(0, 10))

            if is_overdue:
                ctk.CTkButton(btn_frame, text="Apply Fine", command=apply_fine,
                              fg_color="#ef4444", hover_color="#dc2626", width=100).pack(side="left")

    def return_book(self, borrow_id):
        borrowed = self.load_data(self.borrowed_file)
        books = self.load_data(self.books_file)

        if borrow_id in borrowed:
            book_id = borrowed[borrow_id]["book_id"]
            books[book_id]["available"] = True
            del borrowed[borrow_id]

            self.save_data(self.books_file, books)
            self.save_data(self.borrowed_file, borrowed)

            msgbox.showinfo("Success", "Book returned successfully!")
            self.show_student_management()

    def apply_fine(self, borrow_id):
        borrowed = self.load_data(self.borrowed_file)

        if borrow_id in borrowed:
            borrowed[borrow_id]["fine"] = borrowed[borrow_id].get("fine", 0) + 5
            self.save_data(self.borrowed_file, borrowed)

            msgbox.showinfo("Success", "Fine applied successfully!")
            self.show_student_management()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def logout(self):
        self.current_user = None
        self.is_admin = False
        self.setup_login_screen()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = OrchidsLibraryApp()
    app.run()