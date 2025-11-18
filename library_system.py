import sys

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
        self.root.title("ORCHIDS - The Library App")
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
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        try:
            # Create a simple orchid-like logo if ORCHIDS.png doesn't exist
            self.logo_image = ctk.CTkImage(
                light_image=Image.new('RGB', (80, 80), '#dc2626'),
                dark_image=Image.new('RGB', (80, 80), '#dc2626'),
                size=(80, 80)
            )
            logo_path = resource_path("ORCHIDS.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(225, 225))
        except Exception as e:
            print(f"Error loading logo: {e}")
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

        # Initialize books data with copies count
        if not os.path.exists(self.books_file):
            books_data = {
                "1": {"title": "Python Programming", "author": "John Smith", "isbn": "978-0123456789",
                      "total_copies": 3, "available_copies": 3},
                "2": {"title": "Data Science Basics", "author": "Mary Johnson", "isbn": "978-0987654321",
                      "total_copies": 2, "available_copies": 2},
                "3": {"title": "Machine Learning", "author": "Bob Wilson", "isbn": "978-0456789123",
                      "total_copies": 4, "available_copies": 4}
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

    def get_library_stats(self):
        borrowed = self.load_data(self.borrowed_file)

        total_issued = len(borrowed)
        overdue_count = 0

        for borrow in borrowed.values():
            due_date = datetime.strptime(borrow["due_date"], "%Y-%m-%d")
            if datetime.now() > due_date:
                overdue_count += 1

        return total_issued, overdue_count

    def refresh_stats_cards(self):
        """Refresh the statistics cards in admin dashboard"""
        total_issued, overdue_count = self.get_library_stats()

        # Find and update the stats cards
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        # Look for stats frame
                        stats_widgets = child.winfo_children()
                        if len(stats_widgets) >= 2:
                            # Check if these are stat cards by looking for large font labels
                            for stat_widget in stats_widgets:
                                if isinstance(stat_widget, ctk.CTkFrame):
                                    labels = stat_widget.winfo_children()
                                    if len(labels) >= 2:
                                        for label in labels:
                                            if isinstance(label, ctk.CTkLabel):
                                                # Update issued books card
                                                if "Books Issued" in str(label.cget("text")):
                                                    # Update the number label (previous sibling)
                                                    for prev_label in labels:
                                                        if isinstance(prev_label, ctk.CTkLabel) and prev_label != label:
                                                            try:
                                                                int(prev_label.cget("text"))
                                                                prev_label.configure(text=str(total_issued))
                                                                break
                                                            except:
                                                                continue
                                                # Update overdue books card
                                                elif "Books Overdue" in str(label.cget("text")):
                                                    # Update the number label (previous sibling)
                                                    for prev_label in labels:
                                                        if isinstance(prev_label, ctk.CTkLabel) and prev_label != label:
                                                            try:
                                                                int(prev_label.cget("text"))
                                                                prev_label.configure(text=str(overdue_count))
                                                                break
                                                            except:
                                                                continue

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

        # Stats cards
        stats_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)

        total_issued, overdue_count = self.get_library_stats()

        # Issued books card
        issued_card = ctk.CTkFrame(stats_frame, fg_color="#16a34a", corner_radius=10)
        issued_card.pack(side="left", padx=(0, 20), pady=10)

        ctk.CTkLabel(issued_card, text=str(total_issued), font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(issued_card, text="Books Issued", font=ctk.CTkFont(size=14),
                     text_color="white").pack(pady=(0, 15))

        # Due books card
        due_card = ctk.CTkFrame(stats_frame, fg_color="#ef4444", corner_radius=10)
        due_card.pack(side="left", pady=10)

        ctk.CTkLabel(due_card, text=str(overdue_count), font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(due_card, text="Books Overdue", font=ctk.CTkFont(size=14),
                     text_color="white").pack(pady=(0, 15))

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

        # Search frame
        search_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))

        self.book_search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search books by title or author...", width=400)
        self.book_search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="Search", command=self.search_books,
                      fg_color="#dc2626", hover_color="#b91c1c").pack(side="left")

        # Books display frame
        self.books_display_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.books_display_frame.pack(fill="both", expand=True)

        self.display_books()

    def search_books(self):
        search_term = self.book_search_entry.get().lower()
        self.display_books(search_term)

    def display_books(self, search_term=""):
        # Clear existing books
        for widget in self.books_display_frame.winfo_children():
            widget.destroy()

        books = self.load_data(self.books_file)

        for book_id, book in books.items():
            if book["available_copies"] > 0:
                # Filter books based on search term
                if search_term and search_term not in book["title"].lower() and search_term not in book["author"].lower():
                    continue

                book_frame = ctk.CTkFrame(self.books_display_frame, fg_color="#f9f9f9", corner_radius=10)
                book_frame.pack(fill="x", pady=5, padx=10)

                content = ctk.CTkFrame(book_frame, fg_color="transparent")
                content.pack(fill="x", padx=20, pady=15)

                ctk.CTkLabel(content, text=book["title"], font=ctk.CTkFont(size=16, weight="bold"),
                             text_color="#dc2626").pack(anchor="w")
                ctk.CTkLabel(content, text=f"Author: {book['author']}", text_color="#666").pack(anchor="w")
                ctk.CTkLabel(content, text=f"ISBN: {book['isbn']}", text_color="#666").pack(anchor="w")
                ctk.CTkLabel(content, text=f"Available Copies: {book['available_copies']}/{book['total_copies']}",
                             text_color="#16a34a", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

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

            copies_text = f"{book['available_copies']}/{book['total_copies']} available"
            status_color = "#16a34a" if book["available_copies"] > 0 else "#ef4444"

            ctk.CTkLabel(info_frame, text=copies_text, text_color=status_color,
                         font=ctk.CTkFont(weight="bold")).pack(anchor="e", side="right")

            ctk.CTkLabel(content, text=f"Author: {book['author']} | ISBN: {book['isbn']}",
                         text_color="#666").pack(anchor="w")

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
        isbn_entry.pack(pady=(0, 15))

        ctk.CTkLabel(form_content, text="Number of Copies:").pack(anchor="w", pady=(0, 5))
        copies_entry = ctk.CTkEntry(form_content, width=400)
        copies_entry.insert(0, "1")
        copies_entry.pack(pady=(0, 20))

        def add_book():
            if title_entry.get() and author_entry.get() and isbn_entry.get() and copies_entry.get():
                try:
                    copies = int(copies_entry.get())
                    if copies <= 0:
                        msgbox.showerror("Error", "Number of copies must be greater than 0!")
                        return

                    books = self.load_data(self.books_file)
                    new_id = str(max([int(k) for k in books.keys()], default=0) + 1)

                    books[new_id] = {
                        "title": title_entry.get(),
                        "author": author_entry.get(),
                        "isbn": isbn_entry.get(),
                        "total_copies": copies,
                        "available_copies": copies
                    }

                    self.save_data(self.books_file, books)
                    msgbox.showinfo("Success", "Book added successfully!")
                    self.refresh_stats_cards()
                    self.show_admin_books()
                except ValueError:
                    msgbox.showerror("Error", "Please enter a valid number for copies!")
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

        # Student search
        ctk.CTkLabel(form_content, text="Search Student:").pack(anchor="w", pady=(0, 5))
        student_search_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        student_search_frame.pack(fill="x", pady=(0, 15))

        self.student_search_entry = ctk.CTkEntry(student_search_frame, placeholder_text="Enter student name or ID...", width=300)
        self.student_search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(student_search_frame, text="Search", command=self.search_students,
                      fg_color="#dc2626", hover_color="#b91c1c").pack(side="left")

        # Student results
        self.student_results_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        self.student_results_frame.pack(fill="x", pady=(0, 15))

        self.selected_student = None
        self.student_display_label = ctk.CTkLabel(form_content, text="No student selected", text_color="#666")
        self.student_display_label.pack(anchor="w", pady=(0, 15))

        # Book search
        ctk.CTkLabel(form_content, text="Search Book:").pack(anchor="w", pady=(0, 5))
        book_search_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        book_search_frame.pack(fill="x", pady=(0, 15))

        self.book_search_issue_entry = ctk.CTkEntry(book_search_frame, placeholder_text="Enter book title...", width=300)
        self.book_search_issue_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(book_search_frame, text="Search", command=self.search_books_for_issue,
                      fg_color="#dc2626", hover_color="#b91c1c").pack(side="left")

        # Book results
        self.book_results_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        self.book_results_frame.pack(fill="x", pady=(0, 15))

        self.selected_book = None
        self.book_display_label = ctk.CTkLabel(form_content, text="No book selected", text_color="#666")
        self.book_display_label.pack(anchor="w", pady=(0, 15))

        # Due date
        ctk.CTkLabel(form_content, text="Due Date (YYYY-MM-DD):").pack(anchor="w", pady=(0, 5))
        self.due_date_entry = ctk.CTkEntry(form_content, width=400)
        default_due = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        self.due_date_entry.insert(0, default_due)
        self.due_date_entry.pack(pady=(0, 20))

        ctk.CTkButton(form_content, text="Issue Book", command=self.issue_book,
                      fg_color="#f59e0b", hover_color="#d97706").pack()

    def search_students(self):
        search_term = self.student_search_entry.get().lower()

        # Clear previous results
        for widget in self.student_results_frame.winfo_children():
            widget.destroy()

        if not search_term:
            return

        users = self.load_data(self.users_file)
        students = {user: info for user, info in users.items() if info["role"] == "student"}

        matched_students = []
        for student_id, student_info in students.items():
            if (search_term in student_id.lower() or
                search_term in student_info["name"].lower()):
                matched_students.append((student_id, student_info))

        if matched_students:
            for student_id, student_info in matched_students[:5]:  # Show max 5 results
                student_btn = ctk.CTkButton(self.student_results_frame,
                                          text=f"{student_info['name']} ({student_id})",
                                          command=lambda sid=student_id, sname=student_info['name']: self.select_student(sid, sname),
                                          fg_color="#e5e7eb", text_color="#374151", hover_color="#d1d5db")
                student_btn.pack(fill="x", pady=2)
        else:
            ctk.CTkLabel(self.student_results_frame, text="No students found", text_color="#666").pack()

    def select_student(self, student_id, student_name):
        self.selected_student = student_id
        self.student_display_label.configure(text=f"Selected: {student_name} ({student_id})", text_color="#16a34a")

    def search_books_for_issue(self):
        search_term = self.book_search_issue_entry.get().lower()

        # Clear previous results
        for widget in self.book_results_frame.winfo_children():
            widget.destroy()

        if not search_term:
            return

        books = self.load_data(self.books_file)
        available_books = {book_id: book for book_id, book in books.items() if book["available_copies"] > 0}

        matched_books = []
        for book_id, book in available_books.items():
            if search_term in book["title"].lower():
                matched_books.append((book_id, book))

        if matched_books:
            for book_id, book in matched_books[:5]:  # Show max 5 results
                book_btn = ctk.CTkButton(self.book_results_frame,
                                       text=f"{book['title']} (Available: {book['available_copies']})",
                                       command=lambda bid=book_id, btitle=book['title']: self.select_book(bid, btitle),
                                       fg_color="#e5e7eb", text_color="#374151", hover_color="#d1d5db")
                book_btn.pack(fill="x", pady=2)
        else:
            ctk.CTkLabel(self.book_results_frame, text="No available books found", text_color="#666").pack()

    def select_book(self, book_id, book_title):
        self.selected_book = book_id
        self.book_display_label.configure(text=f"Selected: {book_title}", text_color="#16a34a")

    def issue_book(self):
        if not self.selected_student:
            msgbox.showerror("Error", "Please select a student!")
            return

        if not self.selected_book:
            msgbox.showerror("Error", "Please select a book!")
            return

        due_date = self.due_date_entry.get()

        try:
            # Validate date format
            datetime.strptime(due_date, "%Y-%m-%d")

            books = self.load_data(self.books_file)

            # Check if book is still available
            if books[self.selected_book]["available_copies"] <= 0:
                msgbox.showerror("Error", "Selected book is no longer available!")
                return

            # Update book availability
            books[self.selected_book]["available_copies"] -= 1
            self.save_data(self.books_file, books)

            # Add to borrowed books
            borrowed = self.load_data(self.borrowed_file)
            borrow_id = str(len(borrowed) + 1)
            borrowed[borrow_id] = {
                "book_id": self.selected_book,
                "student": self.selected_student,
                "issue_date": datetime.now().strftime("%Y-%m-%d"),
                "due_date": due_date,
                "fine": 0
            }
            self.save_data(self.borrowed_file, borrowed)

            users = self.load_data(self.users_file)
            student_name = users[self.selected_student]["name"]
            book_title = books[self.selected_book]["title"]

            msgbox.showinfo("Success", f"Book '{book_title}' issued to {student_name} successfully!")
            self.refresh_stats_cards()
            self.show_admin_books()

        except ValueError:
            msgbox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")

    def show_student_management(self):
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="Student Management", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#dc2626").pack(pady=(0, 20))

        # Search frame
        search_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))

        self.student_mgmt_search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search students by name or ID...", width=400)
        self.student_mgmt_search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="Search", command=self.search_student_management,
                      fg_color="#dc2626", hover_color="#b91c1c").pack(side="left")

        ctk.CTkButton(search_frame, text="Show All", command=self.show_all_student_management,
                      fg_color="#6b7280", hover_color="#4b5563").pack(side="left", padx=(10, 0))

        # Students display frame
        self.students_mgmt_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.students_mgmt_frame.pack(fill="both", expand=True)

        self.display_student_management()

    def search_student_management(self):
        search_term = self.student_mgmt_search_entry.get().lower()
        self.display_student_management(search_term)

    def show_all_student_management(self):
        self.student_mgmt_search_entry.delete(0, 'end')
        self.display_student_management()

    def display_student_management(self, search_term=""):
        # Clear existing display
        for widget in self.students_mgmt_frame.winfo_children():
            widget.destroy()

        borrowed = self.load_data(self.borrowed_file)
        books = self.load_data(self.books_file)
        users = self.load_data(self.users_file)

        # Filter borrowed books based on search term
        filtered_borrows = []
        for borrow_id, borrow in borrowed.items():
            student_name = users[borrow["student"]]["name"]
            student_id = borrow["student"]

            if not search_term or (search_term in student_name.lower() or search_term in student_id.lower()):
                filtered_borrows.append((borrow_id, borrow))

        if not filtered_borrows:
            if search_term:
                ctk.CTkLabel(self.students_mgmt_frame, text="No students found matching your search", text_color="#666").pack(pady=20)
            else:
                ctk.CTkLabel(self.students_mgmt_frame, text="No books currently issued", text_color="#666").pack(pady=20)
            return

        for borrow_id, borrow in filtered_borrows:
            book = books[borrow["book_id"]]
            student_name = users[borrow["student"]]["name"]

            student_frame = ctk.CTkFrame(self.students_mgmt_frame, fg_color="#f9f9f9", corner_radius=10)
            student_frame.pack(fill="x", pady=5, padx=10)

            content = ctk.CTkFrame(student_frame, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(content, text=f"{student_name} ({borrow['student']}) - {book['title']}",
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

            # Increase available copies
            books[book_id]["available_copies"] += 1
            del borrowed[borrow_id]

            self.save_data(self.books_file, books)
            self.save_data(self.borrowed_file, borrowed)

            msgbox.showinfo("Success", "Book returned successfully!")
            self.refresh_stats_cards()
            self.display_student_management(self.student_mgmt_search_entry.get().lower())

    def apply_fine(self, borrow_id):
        borrowed = self.load_data(self.borrowed_file)

        if borrow_id in borrowed:
            borrowed[borrow_id]["fine"] = borrowed[borrow_id].get("fine", 0) + 5
            self.save_data(self.borrowed_file, borrowed)

            msgbox.showinfo("Success", "Fine applied successfully!")
            self.refresh_stats_cards()
            self.display_student_management(self.student_mgmt_search_entry.get().lower())

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