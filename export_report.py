import os

import pandas as pd
from tkinter import messagebox
from database import connect_db


def export_attendance():

    try:
        connection = connect_db()

        query = """
        SELECT
            students.student_id,
            students.name,
            students.class,
            attendance.attendance_date,
            attendance.status
        FROM attendance
        INNER JOIN students
        ON attendance.student_id = students.student_id
        """

        df = pd.read_sql(query, connection)
        os.makedirs(
            "reports",
            exist_ok=True
        )
        filename = "reports/attendance_report.xlsx"

        df.to_excel(
            filename,
            index=False,
            engine="openpyxl"
        )

        connection.close()

        messagebox.showinfo(
            "Success",
            f"Attendance report exported successfully!\n\nSaved as: {filename}"
        )

    except Exception as e:
        messagebox.showerror(
            "Export Error",
            str(e)
        )