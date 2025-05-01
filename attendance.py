#attendance.py
import csv
import os
from datetime import datetime

def mark_attendance(name, roll_no):
    file = "attendance.csv"
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    status = "IN"

    file_exists = os.path.exists(file)

    if file_exists:
        with open(file, "r") as f:
            reader = list(csv.reader(f))
            student_logs = [row for row in reader if row and row[0] == str(roll_no) and row[1] == name]

            if student_logs:
                last_status = student_logs[-1][-1]
                if last_status == "IN":
                    status = "OUT"
                else:
                    status = "IN"

    # Write header if file doesn't exist or is empty
    write_header = not file_exists or os.path.getsize(file) == 0

    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Roll Number", "Name", "Date", "Time", "Status"])
        writer.writerow([roll_no, name, date_str, time_str, status])
