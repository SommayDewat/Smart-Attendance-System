import customtkinter as ctk
from tkinter import ttk, messagebox
from database import connect_db


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# -------------------------------------------------
# CLEAR FIELDS
# -------------------------------------------------

def clear_fields():

    id_entry.configure(state="normal")
    id_entry.delete(0, "end")
    id_entry.configure(state="disabled")

    name_entry.delete(0, "end")
    class_entry.delete(0, "end")
    roll_entry.delete(0, "end")
    email_entry.delete(0, "end")


# -------------------------------------------------
# LOAD STUDENTS
# -------------------------------------------------

def load_students():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
        student_id,
        name,
        class,
        roll_no,
        email
        FROM students
    """)

    rows = cursor.fetchall()

    student_table.delete(
        *student_table.get_children()
    )

    for row in rows:
        student_table.insert(
            "",
            "end",
            values=row
        )

    total_label.configure(
        text=f"Total Students: {len(rows)}"
    )

    connection.close()


# -------------------------------------------------
# ADD STUDENT
# -------------------------------------------------

def add_student():

    if name_entry.get() == "":
        messagebox.showerror(
            "Error",
            "Student Name is required"
        )
        return

    if roll_entry.get() == "":
        messagebox.showerror(
            "Error",
            "Roll Number is required"
        )
        return

    if (
        email_entry.get() != ""
        and "@" not in email_entry.get()
    ):
        messagebox.showerror(
            "Error",
            "Please enter a valid email"
        )
        return

    try:

        connection = connect_db()
        cursor = connection.cursor()

        query = """
        INSERT INTO students
        (
            name,
            class,
            roll_no,
            email
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """

        cursor.execute(
            query,
            (
                name_entry.get(),
                class_entry.get(),
                roll_entry.get(),
                email_entry.get()
            )
        )

        connection.commit()
        connection.close()

        load_students()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Student record added successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )
    finally:
        try:
            connection.close()
        except:
            pass

# -------------------------------------------------
# UPDATE STUDENT
# -------------------------------------------------

def update_student():

    selected_id = id_entry.get()

    if selected_id == "":
        messagebox.showerror(
            "Error",
            "Please select a student first"
        )
        return

    try:

        connection = connect_db()
        cursor = connection.cursor()

        query = """
        UPDATE students
        SET
            name=%s,
            class=%s,
            roll_no=%s,
            email=%s
        WHERE student_id=%s
        """

        cursor.execute(
            query,
            (
                name_entry.get(),
                class_entry.get(),
                roll_entry.get(),
                email_entry.get(),
                selected_id
            )
        )

        connection.commit()
        connection.close()

        load_students()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Student record updated successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )
    finally:
        try:
            connection.close()
        except:
            pass


# -------------------------------------------------
# SELECT STUDENT
# -------------------------------------------------

def select_student(event=None):

    selected = student_table.focus()
    if not selected:
        return

    values = student_table.item(selected, "values")
    if not values:
        return

    student_id, name, student_class, roll, email = values

    id_entry.configure(state="normal")
    id_entry.delete(0, "end")
    id_entry.insert(0, student_id)
    id_entry.configure(state="disabled")

    name_entry.delete(0, "end")
    name_entry.insert(0, name)

    class_entry.delete(0, "end")
    class_entry.insert(0, student_class)

    roll_entry.delete(0, "end")
    roll_entry.insert(0, roll)

    email_entry.delete(0, "end")
    email_entry.insert(0, email)


# -------------------------------------------------
# DELETE STUDENT
# -------------------------------------------------

def delete_student():

    selected_id = id_entry.get()

    if selected_id == "":
        messagebox.showerror(
            "Error",
            "Please select a student first"
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if not confirm:
        return

    try:

        connection = connect_db()
        cursor = connection.cursor()

        # Check attendance records first
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id=%s
            """,
            (selected_id,)
        )

        attendance_count = cursor.fetchone()[0]

        if attendance_count > 0:

            messagebox.showwarning(
                "Cannot Delete",
                "This student already has attendance history. Delete attendance records first."
            )

            connection.close()
            return

        # Delete student
        cursor.execute(
            """
            DELETE FROM students
            WHERE student_id=%s
            """,
            (selected_id,)
        )

        connection.commit()
        connection.close()

        load_students()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Student record deleted successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:
        try:
            connection.close()
        except:
            pass


# -------------------------------------------------
# Search Student
# -------------------------------------------------

def search_student():

    keyword = search_entry.get().strip()

    if keyword == "":
        load_students()
        return

    try:

        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                student_id,
                name,
                class,
                roll_no,
                email
            FROM students
            WHERE
                name LIKE %s OR
                roll_no LIKE %s OR
                email LIKE %s
            """,
            (
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%"
            )
        )

        rows = cursor.fetchall()
        total_label.configure(
            text=f"Total Students: {len(rows)}"
        )

        student_table.delete(
            *student_table.get_children()
        )

        for row in rows:
            student_table.insert(
                "",
                "end",
                values=row
            )

        connection.close()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )
    finally:
        try:
            connection.close()
        except:
            pass

app = ctk.CTk()

app.title("Student Management System")
app.geometry("1200x700")
app.minsize(1300, 750)

title = ctk.CTkLabel(
    app,
    text="🎓 Student Management System",
    font=("Segoe UI", 28, "bold")
)

title.pack(pady=20)


# -------------------------------------------------
# MAIN CONTAINER
# -------------------------------------------------

main_container = ctk.CTkFrame(
    app,
    corner_radius=15
)

main_container.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# -------------------------------------------------
# LEFT PANEL
# -------------------------------------------------

left_panel = ctk.CTkFrame(
    main_container,
    width=420,
    corner_radius=15
)

left_panel.pack(
    side="left",
    fill="y",
    padx=15,
    pady=8
)

left_panel.pack_propagate(False)

# -------------------------------------------------
# FORM TITLE
# -------------------------------------------------

form_title = ctk.CTkLabel(
    left_panel,
    text="Student Information",
    font=("Segoe UI", 20, "bold")
)

form_title.pack(pady=10)

# -------------------------------------------------
# ID
# -------------------------------------------------

ctk.CTkLabel(
    left_panel,
    text="Student ID"
).pack(anchor="w", padx=20)

id_entry = ctk.CTkEntry(
    left_panel,
    width=320,
    state="disabled"
)

id_entry.pack(pady=5)

# -------------------------------------------------
# NAME
# -------------------------------------------------

ctk.CTkLabel(
    left_panel,
    text="Student Name"
).pack(anchor="w", padx=20)

name_entry = ctk.CTkEntry(
    left_panel,
    width=320,
    placeholder_text="Enter Student Name"
)

name_entry.pack(pady=5)

# -------------------------------------------------
# CLASS
# -------------------------------------------------

ctk.CTkLabel(
    left_panel,
    text="Class"
).pack(anchor="w", padx=20)

class_entry = ctk.CTkEntry(
    left_panel,
    width=320,
    placeholder_text="BCA / BBA / MCA"
)

class_entry.pack(pady=5)

# -------------------------------------------------
# ROLL NO
# -------------------------------------------------

ctk.CTkLabel(
    left_panel,
    text="Roll Number"
).pack(anchor="w", padx=20)

roll_entry = ctk.CTkEntry(
    left_panel,
    width=320,
    placeholder_text="Enter Roll Number"
)

roll_entry.pack(pady=5)

# -------------------------------------------------
# EMAIL
# -------------------------------------------------

ctk.CTkLabel(
    left_panel,
    text="Email"
).pack(anchor="w", padx=20)

email_entry = ctk.CTkEntry(
    left_panel,
    width=320,
    placeholder_text="Enter Email ID"
)

email_entry.pack(pady=5)

# -------------------------------------------------
# BUTTONS
# -------------------------------------------------

button_frame = ctk.CTkFrame(
    left_panel,
    fg_color="transparent"
)

button_frame.pack(
    pady=25
)

ctk.CTkButton(
    button_frame,
    text="➕ Add",
    width=145,
    command=add_student
).grid(row=0, column=0, padx=5, pady=5)

ctk.CTkButton(
    button_frame,
    text="✏️ Update",
    width=145,
    command=update_student
).grid(row=0, column=1, padx=5, pady=5)

ctk.CTkButton(
    button_frame,
    text="🗑 Delete",
    width=145,
    command=delete_student
).grid(row=1, column=0, padx=5, pady=5)

ctk.CTkButton(
    button_frame,
    text="🧹 Clear",
    width=145,
    command=clear_fields
).grid(row=1, column=1, padx=5, pady=5)


# -------------------------------------------------
# TOTAL STUDENTS
# -------------------------------------------------

total_label = ctk.CTkLabel(
    left_panel,
    text="Total Students: 0",
    font=("Arial", 13, "bold")
)

total_label.pack(
    side="bottom",
    pady=20
)


# -------------------------------------------------
# RIGHT PANEL
# -------------------------------------------------

right_panel = ctk.CTkFrame(
    main_container,
    corner_radius=15
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

# -------------------------------------------------
# TABLE TITLE
# -------------------------------------------------

table_title = ctk.CTkLabel(
    right_panel,
    text="📋 Student Records",
    font=("Segoe UI", 20, "bold")
)

table_title.pack(
    pady=15
)

# ------------------------------------
# SEARCH BAR
# ------------------------------------

search_frame = ctk.CTkFrame(
    right_panel,
    fg_color="transparent"
)

search_frame.pack(
    pady=(0, 15)
)

search_entry = ctk.CTkEntry(
    search_frame,
    width=350,
    placeholder_text="Search by Name, Roll No, Email..."
)

search_entry.grid(
    row=0,
    column=0,
    padx=10
)

search_btn = ctk.CTkButton(
    search_frame,
    text="Search",
    width=120,
    command=search_student
)

search_btn.grid(
    row=0,
    column=1,
    padx=5
)

show_all_btn = ctk.CTkButton(
    search_frame,
    text="Show All",
    width=120,
    command=load_students
)

show_all_btn.grid(
    row=0,
    column=2,
    padx=5
)

search_entry.bind(
    "<Return>",
    lambda event: search_student()
)


# -------------------------------------------------
# TABLE FRAME
# -------------------------------------------------

table_frame = ctk.CTkFrame(
    right_panel
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(20, 15)
)

# -------------------------------------------------
# TREEVIEW STYLE
# -------------------------------------------------

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="#2b2b2b",
    foreground="white",
    fieldbackground="#2b2b2b",
    rowheight=30,
    font=("Arial", 11)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold")
)

# -------------------------------------------------
# SCROLLBAR
# -------------------------------------------------

scroll_y = ttk.Scrollbar(
    table_frame,
    orient="vertical"
)

scroll_y.pack(
    side="right",
    fill="y"
)

scroll_x = ttk.Scrollbar(
    table_frame,
    orient="horizontal"
)

scroll_x.pack(
    side="bottom",
    fill="x"
)
# -------------------------------------------------
# TREEVIEW
# -------------------------------------------------

student_table = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Name",
        "Class",
        "Roll",
        "Email"
    ),
    show="headings",
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

scroll_y.config(
    command=student_table.yview
)

scroll_x.config(
    command=student_table.xview
)

student_table.heading(
    "ID",
    text="ID"
)

student_table.heading(
    "Name",
    text="Name"
)

student_table.heading(
    "Class",
    text="Class"
)

student_table.heading(
    "Roll",
    text="Roll No"
)

student_table.heading(
    "Email",
    text="Email"
)

student_table.column(
    "ID",
    width=70,
    anchor="center"
)

student_table.column(
    "Name",
    width=220
)

student_table.column(
    "Class",
    width=120,
    anchor="center"
)

student_table.column(
    "Roll",
    width=120,
    anchor="center"
)

student_table.column(
    "Email",
    width=250
)

student_table.pack(
    fill="both",
    expand=True
)

student_table.bind(
    "<<TreeviewSelect>>",
    select_student
)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------
footer = ctk.CTkLabel(
    app,
    text="© 2025 Smart Attendance System • Student Management Module. All rights reserved.",
    font=("Arial", 12)
)
footer.pack(side="bottom", pady=(10, 0))

load_students()
app.mainloop()