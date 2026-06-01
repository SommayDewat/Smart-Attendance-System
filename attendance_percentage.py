import customtkinter as ctk
from tkinter import ttk

from database import connect_db

# -------------------------------------------------
# APP SETTINGS
# -------------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------------------------------------
# SEARCH FUNCTION
# -------------------------------------------------

def search_student():

    keyword = search_entry.get().strip()

    if keyword == "":
        load_percentage()
        return

    for row in percentage_table.get_children():
        percentage_table.delete(row)

    connection = connect_db()
    cursor = connection.cursor()

    query = """
    SELECT
        s.student_id,
        s.name,

        COUNT(
            CASE
                WHEN a.status='Present'
                THEN 1
            END
        ) AS present_days,

        COUNT(
            CASE
                WHEN a.status='Absent'
                THEN 1
            END
        ) AS absent_days,

        COUNT(a.attendance_id) AS total_days

    FROM students s

    LEFT JOIN attendance a
    ON s.student_id = a.student_id

    WHERE s.name LIKE %s

    GROUP BY
        s.student_id,
        s.name
    ORDER BY present_days DESC
    """

    cursor.execute(
        query,
        (f"%{keyword}%",)
    )

    records = cursor.fetchall()

    connection.close()

    for record in records:

        student_id = record[0]
        name = record[1]
        present_days = record[2]
        absent_days = record[3]
        total_days = record[4]

        percentage = (
            present_days / total_days * 100
        ) if total_days > 0 else 0

        if percentage >= 90:
            performance = "⭐ Excellent"

        elif percentage >= 75:
            performance = "🟢 Good"

        elif percentage >= 50:
            performance = "🟡 Average"

        else:
            performance = "🔴 Needs Improvement"

        percentage_table.insert(
            "",
            "end",
            values=(
                student_id,
                name,
                present_days,
                absent_days,
                total_days,
                f"{percentage:.2f}%",
                performance
            )
        )

# -------------------------------------------------
# LOAD ATTENDANCE PERCENTAGE
# -------------------------------------------------

def load_percentage():

    connection = connect_db()
    cursor = connection.cursor()

    query = """
    SELECT
        s.student_id,
        s.name,

        COUNT(
            CASE
                WHEN a.status='Present'
                THEN 1
            END
        ) AS present_days,

        COUNT(
            CASE
                WHEN a.status='Absent'
                THEN 1
            END
        ) AS absent_days,

        COUNT(a.attendance_id) AS total_days

    FROM students s

    LEFT JOIN attendance a
    ON s.student_id = a.student_id

    GROUP BY
        s.student_id,
        s.name
    ORDER BY present_days DESC
    """

    cursor.execute(query)

    records = cursor.fetchall()

    percentage_table.delete(
        *percentage_table.get_children()
    )

    for record in records:

        student_id = record[0]
        name = record[1]
        present_days = record[2]
        absent_days = record[3]
        total_days = record[4]

        if total_days == 0:
            percentage = 0
        else:
            percentage = (
                present_days / total_days
            ) * 100
        if percentage >= 90:
            performance = "⭐ Excellent"

        elif percentage >= 75:
            performance = "🟢 Good"

        elif percentage >= 50:
            performance = "🟡 Average"

        else:
            performance = "🔴 Needs Improvement"

        percentage_table.insert(
            "",
            "end",
            values=(
                student_id,
                name,
                present_days,
                absent_days,
                total_days,
                f"{percentage:.2f}%",
                performance
            )
        )

    # total_label.configure(
    #     text=f"Total Students: {len(records)}"
    # )
    # ---------------- CARD CALCULATIONS ---------------- #

    total_students = len(records)

    total_present = sum(
        record[2]
        for record in records
    )

    total_absent = sum(
        record[3]
        for record in records
    )

    if total_present + total_absent > 0:

        avg_rate = (
            total_present /
            (total_present + total_absent)
        ) * 100

    else:

        avg_rate = 0


    students_value.configure(
        text=str(total_students)
    )

    present_value.configure(
    text=str(total_present)
    )

    absent_value.configure(
        text=str(total_absent)
    )


    rate_value.configure(
        text=f"{avg_rate:.1f}%"
    )
    connection.close()


# -------------------------------------------------
# MAIN WINDOW
# -------------------------------------------------

app = ctk.CTk()
# app.iconbitmap("assets/icon.ico")
app.title("Attendance Summary Dashboard")
app.geometry("1400x800")
app.minsize(1300, 750)


# -------------------------------------------------
# TITLE
# -------------------------------------------------

title = ctk.CTkLabel(
    app,
    text="📊 Attendance Summary Dashboard",
    font=("Segoe UI", 28, "bold")
)

title.pack(
    pady=20
)

# -------------------------------------------------
# SUMMARY CARDS
# -------------------------------------------------

cards_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

cards_frame.pack(
    fill="x",
    padx=20,
    pady=(10, 0)
)

# Students Card

students_card = ctk.CTkFrame(
    cards_frame,
    width=250,
    height=120
)

students_card.pack(
    side="left",
    padx=10,
    pady=10,
    expand=True,
    fill="both"
)

students_title = ctk.CTkLabel(
    students_card,
    text="👨‍🎓 Students",
    font=("Segoe UI", 18, "bold")
)

students_title.pack(pady=(15, 5))

students_value = ctk.CTkLabel(
    students_card,
    text="0",
    font=("Segoe UI", 28, "bold")
)

students_value.pack()


# Present Card

present_card = ctk.CTkFrame(
    cards_frame,
    width=250,
    height=120
)

present_card.pack(
    side="left",
    padx=10,
    pady=10,
    expand=True,
    fill="both"
)

present_title = ctk.CTkLabel(
    present_card,
    text="🟢 Present",
    font=("Segoe UI", 18, "bold")
)

present_title.pack(pady=(15, 5))

present_value = ctk.CTkLabel(
    present_card,
    text="0",
    font=("Segoe UI", 28, "bold")
)

present_value.pack()


# Absent Card

absent_card = ctk.CTkFrame(
    cards_frame,
    width=250,
    height=120
)

absent_card.pack(
    side="left",
    padx=10,
    pady=10,
    expand=True,
    fill="both"
)

absent_title = ctk.CTkLabel(
    absent_card,
    text="🔴 Absent",
    font=("Segoe UI", 18, "bold")
)

absent_title.pack(pady=(15, 5))

absent_value = ctk.CTkLabel(
    absent_card,
    text="0",
    font=("Segoe UI", 28, "bold")
)

absent_value.pack()


# Average Rate Card

rate_card = ctk.CTkFrame(
    cards_frame,
    width=250,
    height=120
)

rate_card.pack(
    side="left",
    padx=10,
    pady=10,
    expand=True,
    fill="both"
)

rate_title = ctk.CTkLabel(
    rate_card,
    text="📈 Avg Rate",
    font=("Segoe UI", 18, "bold")
)

rate_title.pack(pady=(15, 5))

rate_value = ctk.CTkLabel(
    rate_card,
    text="0%",
    font=("Segoe UI", 28, "bold")
)

rate_value.pack()

# -------------------------------------------------
# MAIN FRAME
# -------------------------------------------------

main_frame = ctk.CTkFrame(
    app,
    corner_radius=15
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# -------------------------------------------------
# SEARCH FRAME
# -------------------------------------------------
search_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

search_frame.pack(
    fill="x",
    padx=20,
    pady=(5, 10)
)

search_entry = ctk.CTkEntry(
    search_frame,
    width=350,
    placeholder_text="Search Student Name..."
)

search_entry.pack(
    side="left",
    padx=10
)

search_btn = ctk.CTkButton(
    search_frame,
    text="Search",
    width=120,
    command=lambda: search_student()
)

search_btn.pack(
    side="left",
    padx=10
)

show_all_btn = ctk.CTkButton(
    search_frame,
    text="Show All",
    width=120,
    command=load_percentage
)

show_all_btn.pack(
    side="left",
    padx=10
)

search_entry.bind(
    "<Return>",
    lambda event: search_student()
)


# -------------------------------------------------
# TABLE FRAME
# -------------------------------------------------

table_frame = ctk.CTkFrame(
    main_frame
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)


# -------------------------------------------------
# SCROLLBARS
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
# TABLE
# -------------------------------------------------

percentage_table = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Name",
        "Present",
        "Absent",
        "Total",
        "Percentage",
        "Performance"
    ),
    show="headings",
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

scroll_y.config(
    command=percentage_table.yview
)

scroll_x.config(
    command=percentage_table.xview
)


# -------------------------------------------------
# HEADINGS
# -------------------------------------------------

percentage_table.heading(
    "ID",
    text="Student ID"
)

percentage_table.heading(
    "Name",
    text="Student Name"
)

percentage_table.heading(
    "Present",
    text="Present Days"
)

percentage_table.heading(
    "Absent",
    text="Absent Days"
)

percentage_table.heading(
    "Total",
    text="Total Days"
)

percentage_table.heading(
    "Percentage",
    text="Attendance %"
)

percentage_table.heading(
    "Performance",
    text="Performance"
)

# -------------------------------------------------
# COLUMNS
# -------------------------------------------------

percentage_table.column(
    "ID",
    width=120,
    anchor="center"
)

percentage_table.column(
    "Name",
    width=300
)

percentage_table.column(
    "Present",
    width=150,
    anchor="center"
)

percentage_table.column(
    "Absent",
    width=140,
    anchor="center"
)

percentage_table.column(
    "Total",
    width=150,
    anchor="center"
)

percentage_table.column(
    "Percentage",
    width=180,
    anchor="center"
)

percentage_table.column(
    "Performance",
    width=180,
    anchor="center"
)

percentage_table.pack(
    fill="both",
    expand=True
)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

footer = ctk.CTkLabel(
    app,
    text="© 2025 Smart Attendance System • Attendance Analytics Module",
    font=("Arial", 12)
)

footer.pack(
    side="bottom",
    pady=(10, 0)
)


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

load_percentage()


# -------------------------------------------------
# RUN APP
# -------------------------------------------------

app.mainloop()