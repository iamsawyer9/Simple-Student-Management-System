import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="database-host",
        user="database-user",
        passwd="/database-password/",
        database="student_management"
    )

def insert_student(name, age, grade):
    conn = create_connection()
    cursor = conn.cursor()
    query = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, age, grade))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student added successfully")
    refresh_listbox()

def update_student(id, name, age, grade):
    conn = create_connection()
    cursor = conn.cursor()
    query = "UPDATE students SET name = %s, age = %s, grade = %s WHERE id = %s"
    cursor.execute(query, (name, age, grade, id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student updated successfully")
    refresh_listbox()

def delete_student(id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully")
    refresh_listbox()

def get_student_id():
    try:
        index = student_listbox.curselection()[0]
        selected_student = student_listbox.get(index)
        student_id = selected_student.split(' ')[0]
        return student_id
    except IndexError:
        messagebox.showerror("Error", "Please select a student from the list")
        return None

def refresh_listbox():
    student_listbox.delete(0, tk.END)
    students = view_students()
    for student in students:
        student_listbox.insert(tk.END, f"{student[0]} - {student[1]}")

def view_students():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    conn.close()
    return students

# GUI
app = tk.Tk()
app.title("Student Management System")

# Entry fields for student details
tk.Label(app, text="Name").grid(row=0, column=0)
name_text = tk.StringVar()
tk.Entry(app, textvariable=name_text).grid(row=0, column=1)

tk.Label(app, text="Age").grid(row=1, column=0)
age_text = tk.IntVar()
tk.Entry(app, textvariable=age_text).grid(row=1, column=1)

tk.Label(app, text="Grade").grid(row=2, column=0)
grade_text = tk.StringVar()
tk.Entry(app, textvariable=grade_text).grid(row=2, column=1)

# Buttons
tk.Button(app, text="Add Student", command=lambda: insert_student(name_text.get(), age_text.get(), grade_text.get())).grid(row=3, column=0)
tk.Button(app, text="Update Student", command=lambda: update_student(get_student_id(), name_text.get(), age_text.get(), grade_text.get())).grid(row=3, column=1)
tk.Button(app, text="Delete Student", command=lambda: delete_student(get_student_id())).grid(row=4, column=0)

# Listbox to display students
student_listbox = tk.Listbox(app)
student_listbox.grid(row=5, column=0, columnspan=2, sticky="ew")
refresh_listbox()

app.mainloop()
