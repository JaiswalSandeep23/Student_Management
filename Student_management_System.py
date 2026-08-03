import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ==============================
# File for Permanent Storage
# ==============================
FILE_NAME = "students.json"

# ==============================
# Load Data
# ==============================
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                return [tuple(record) for record in data]
        except:
            return []
    return []

# ==============================
# Save Data
# ==============================
def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)

# ==============================
# Grade Calculator
# ==============================
def grade(score):
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

# ==============================
# Refresh Table
# ==============================
def refresh(data=None):
    tree.delete(*tree.get_children())

    if data is None:
        data = students

    for student in data:
        tree.insert("", tk.END, values=student)

# ==============================
# Clear Entry Boxes
# ==============================
def clear():
    name_entry.delete(0, tk.END)
    score_entry.delete(0, tk.END)

# ==============================
# Add Student
# ==============================
def add_student():
    name = name_entry.get().strip()

    if name == "":
        messagebox.showwarning("Warning", "Please enter student name.")
        return

    try:
        score = int(score_entry.get())

        if score < 0 or score > 100:
            raise ValueError

    except:
        messagebox.showerror("Error", "Score must be between 0 and 100.")
        return

    students.append((
        name,
        score,
        grade(score),
        "PASS" if score >= 50 else "FAIL"
    ))

    save_data()
    refresh()
    clear()

# ==============================
# Delete Student
# ==============================
def delete_student():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a student.")
        return

    index = tree.index(selected[0])

    if messagebox.askyesno("Confirm", "Delete selected student?"):
        students.pop(index)
        save_data()
        refresh()

# ==============================
# Update Student
# ==============================
def update_student():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a student.")
        return

    try:
        score = int(score_entry.get())
    except:
        messagebox.showerror("Error", "Invalid score.")
        return

    index = tree.index(selected[0])

    students[index] = (
        name_entry.get(),
        score,
        grade(score),
        "PASS" if score >= 50 else "FAIL"
    )

    save_data()
    refresh()
    clear()

# ==============================
# Search Student
# ==============================
def search_student():

    keyword = search_entry.get().lower().strip()

    if keyword == "":
        refresh()
        return

    result = []

    for student in students:
        if keyword in student[0].lower():
            result.append(student)

    refresh(result)

# ==============================
# Statistics
# ==============================
def statistics():

    if len(students) == 0:
        messagebox.showinfo("Statistics", "No student records.")
        return

    total = len(students)

    average = sum(student[1] for student in students) / total

    topper = max(students, key=lambda x: x[1])

    messagebox.showinfo(
        "Statistics",
        f"""
Total Students : {total}

Average Score : {average:.2f}

Top Scorer : {topper[0]}
Marks : {topper[1]}
Grade : {topper[2]}
"""
    )

# ==============================
# Select Row
# ==============================
def select_record(event):

    selected = tree.selection()

    if selected:
        values = tree.item(selected[0], "values")

        clear()

        name_entry.insert(0, values[0])
        score_entry.insert(0, values[1])

# ==============================
# GUI
# ==============================
root = tk.Tk()

root.title("🎓 Student Record Management System")
root.geometry("950x650")
root.configure(bg="#EAF6FF")

title = tk.Label(
    root,
    text="🎓 Student Record Management System",
    font=("Arial", 24, "bold"),
    bg="#007ACC",
    fg="white",
    pady=10
)

title.pack(fill=tk.X)

students = load_data()

# ==============================
# Input Frame
# ==============================
frame = tk.Frame(root, bg="#EAF6FF")
frame.pack(pady=20)

tk.Label(frame, text="Student Name",
         font=("Arial", 12, "bold"),
         bg="#EAF6FF").grid(row=0, column=0)

name_entry = tk.Entry(frame, width=25, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=10)

tk.Label(frame, text="Exam Score",
         font=("Arial", 12, "bold"),
         bg="#EAF6FF").grid(row=0, column=2)

score_entry = tk.Entry(frame, width=10, font=("Arial", 12))
score_entry.grid(row=0, column=3)

# ==============================
# Buttons
# ==============================
button_frame = tk.Frame(root, bg="#EAF6FF")
button_frame.pack()

tk.Button(button_frame,
          text="➕ Add",
          bg="green",
          fg="white",
          width=12,
          command=add_student).grid(row=0, column=0, padx=5)

tk.Button(button_frame,
          text="✏ Update",
          bg="dodgerblue",
          fg="white",
          width=12,
          command=update_student).grid(row=0, column=1, padx=5)

tk.Button(button_frame,
          text="❌ Delete",
          bg="red",
          fg="white",
          width=12,
          command=delete_student).grid(row=0, column=2, padx=5)

tk.Button(button_frame,
          text="📊 Statistics",
          bg="purple",
          fg="white",
          width=12,
          command=statistics).grid(row=0, column=3, padx=5)

# ==============================
# Search
# ==============================
search_frame = tk.Frame(root, bg="#EAF6FF")
search_frame.pack(pady=15)

search_entry = tk.Entry(search_frame,
                        font=("Arial", 12),
                        width=30)

search_entry.grid(row=0, column=0)

tk.Button(search_frame,
          text="🔍 Search",
          bg="orange",
          command=search_student).grid(row=0, column=1, padx=10)

tk.Button(search_frame,
          text="Show All",
          command=refresh).grid(row=0, column=2)

# ==============================
# Table
# ==============================
tree = ttk.Treeview(
    root,
    columns=("Name", "Score", "Grade", "Status"),
    show="headings",
    height=18
)

tree.heading("Name", text="Student Name")
tree.heading("Score", text="Exam Score")
tree.heading("Grade", text="Grade")
tree.heading("Status", text="Result")

tree.column("Name", width=300)
tree.column("Score", width=120, anchor="center")
tree.column("Grade", width=120, anchor="center")
tree.column("Status", width=120, anchor="center")

tree.pack(fill="both", expand=True, padx=20, pady=20)

tree.bind("<<TreeviewSelect>>", select_record)

# ==============================
# Load Saved Records
# ==============================
refresh()

root.mainloop()
