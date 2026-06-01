import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from datetime import date
from datetime import date

# -------------------------------------------------
# APP SETTINGS
# -------------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# -------------------------------------------------
# LOAD STUDENTS
# -------------------------------------------------

def load_students():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT student_id, name FROM students"
    )

    students = cursor.fetchall()

    student_list = []

    for student in students:

        student_list.append(
            f"{student[0]} - {student[1]}"
        )

    student_combo.configure(
        values=student_list
    )

    connection.close()


# -------------------------------------------------
# SAVE ATTENDANCE
# -------------------------------------------------

def save_attendance():

    selected_student = student_combo.get()
    status = status_combo.get()

    if selected_student == "":
        messagebox.showerror(
            "Error",
            "Please select a student"
        )
        return

    if status == "":
        messagebox.showerror(
            "Error",
            "Please select attendance status"
        )
        return

    try:

        student_id = selected_student.split(
            " - "
        )[0]

        attendance_date = date.today()

        connection = connect_db()
        cursor = connection.cursor()

        query = """
        INSERT INTO attendance
        (
            student_id,
            attendance_date,
            status
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """

        cursor.execute(
            query,
            (
                student_id,
                attendance_date,
                status
            )
        )

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Attendance Marked Successfully"
        )

        student_combo.set("")
        status_combo.set("")

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# -------------------------------------------------
# MAIN WINDOW
# -------------------------------------------------

app = ctk.CTk()

app.title("Attendance Management")
app.geometry("650x500")
app.resizable(False, False)


# -------------------------------------------------
# HEADER
# -------------------------------------------------

title = ctk.CTkLabel(
    app,
    text="📅 Mark Attendance",
    font=("Segoe UI", 28, "bold")
)

title.pack(
    pady=(25, 10)
)

subtitle = ctk.CTkLabel(
    app,
    text="Select a student and mark attendance",
    font=("Arial", 14)
)

subtitle.pack(
    pady=(0, 20)
)


# -------------------------------------------------
# MAIN CARD
# -------------------------------------------------

card = ctk.CTkFrame(
    app,
    width=500,
    height=320,
    corner_radius=15
)

card.pack(
    pady=10
)

card.pack_propagate(False)


# -------------------------------------------------
# DATE LABEL
# -------------------------------------------------

date_label = ctk.CTkLabel(
    app,
    text=f"Date: {date.today()}",
    font=("Arial", 13)
)

date_label.pack()


# -------------------------------------------------
# STUDENT LABEL
# -------------------------------------------------

student_label = ctk.CTkLabel(
    card,
    text="Select Student",
    font=("Arial", 14, "bold")
)

student_label.pack(
    pady=(25, 5)
)


# -------------------------------------------------
# STUDENT COMBOBOX
# -------------------------------------------------

student_combo = ctk.CTkComboBox(
    card,
    width=320,
    values=["Select Student"]
)

student_combo.pack(
    pady=5
)


# -------------------------------------------------
# STATUS LABEL
# -------------------------------------------------

status_label = ctk.CTkLabel(
    card,
    text="Attendance Status",
    font=("Arial", 14, "bold")
)

status_label.pack(
    pady=(20, 5)
)


# -------------------------------------------------
# STATUS COMBOBOX
# -------------------------------------------------

status_combo = ctk.CTkComboBox(
    card,
    width=320,
    values=[
        "Present",
        "Absent"
    ]
)

status_combo.pack(
    pady=5
)


# -------------------------------------------------
# SAVE BUTTON
# -------------------------------------------------

save_btn = ctk.CTkButton(
    card,
    text="✅ Save Attendance",
    width=250,
    height=45,
    command=save_attendance
)

save_btn.pack(
    pady=35
)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

footer = ctk.CTkLabel(
    app,
    text="Smart Attendance System",
    font=("Arial", 12)
)

footer.pack(
    pady=15
)


# -------------------------------------------------
# ENTER KEY SUPPORT
# -------------------------------------------------

app.bind(
    "<Return>",
    lambda event: save_attendance()
)


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

load_students()

# -------------------------------------------------
# RUN APP
# -------------------------------------------------
app.mainloop()