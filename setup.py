from cx_Freeze import setup, Executable
import sys
import os

# Files to include
additional_files = [
    "ORCHIDS.png",  # Your logo image
    "users.json",
    "books.json",
    "borrowed_books.json"
]

# GUI applications should use base="Win32GUI" to prevent console window
base = "Win32GUI" if sys.platform == "win32" else None

# Include packages that might not be automatically detected
build_options = {
    "packages": ["customtkinter", "PIL", "json", "os", "datetime"],
    "includes": ["tkinter"],
    "include_files": additional_files,
    "excludes": ["test"]
}

setup(
    name="OrchidsLibrary",
    version="1.0",
    description="Library Management System",
    options={"build_exe": build_options},
    executables=[Executable(
        "library_system.py",
        base=base,
        icon="ORCHIDS.ico"  # Optional: add if you have an .ico file for the exe
    )]
)