import tkinter as tk
import os, csv
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt

# Base paths
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
ATTENDANCE_DIR  = os.path.join(BASE_DIR, "Attendance")
UI_DIR          = os.path.join(BASE_DIR, "UI_Image")
ICON_PATH       = os.path.join(UI_DIR, "AMS.ico")

# Theme configuration
BG_COLOR       = "#2E3440"
FG_COLOR       = "#ECEFF4"
ACCENT_COLOR   = "#88C0D0"
BUTTON_BG      = "#5E81AC"
BUTTON_FG      = "#ECEFF4"
FONT_TITLE     = ("Segoe UI", 24, "bold")
FONT_LABEL     = ("Segoe UI", 14)
FONT_BUTTON    = ("Segoe UI", 12)


def subjectchoose(text_to_speech):
    def calculate_attendance():
        sub = entry_subject.get().strip()
        if not sub:
            msg = "Please enter the subject name!"
            notify_label.config(text=msg, fg=BUTTON_BG)
            text_to_speech(msg)
            return

        subject_dir = os.path.join(ATTENDANCE_DIR, sub)
        pattern = os.path.join(subject_dir, f"{sub}.csv")
        if not os.path.exists(pattern):
            msg = f"No attendance records for '{sub}'"
            notify_label.config(text=msg, fg=BUTTON_BG)
            text_to_speech(msg)
            return

        # Load master CSV
        df = pd.read_csv(pattern)
        # Compute attendance percentage
        total_sessions = df['Timestamp'].nunique()
        counts = df.groupby(['Enrollment', 'Name']).size().reset_index(name='PresentCount')
        counts['Attendance%'] = (counts['PresentCount'] / total_sessions * 100).round(1)

        # Save summary
        summary_csv = os.path.join(subject_dir, "attendance_summary.csv")
        counts.to_csv(summary_csv, index=False)

        # Display table
        sheet = tk.Toplevel()
        sheet.title(f"Attendance Summary: {sub}")
        sheet.configure(bg=BG_COLOR)
        for r, row in enumerate([counts.columns.tolist()] + counts.values.tolist()):
            for c, val in enumerate(row):
                tk.Label(
                    sheet,
                    text=val,
                    bg=BG_COLOR,
                    fg=FG_COLOR,
                    font=FONT_LABEL,
                    relief=tk.RIDGE,
                    width=12
                ).grid(row=r, column=c, padx=2, pady=2)
        sheet.mainloop()

    def show_analytics():
        sub = entry_subject.get().strip()
        if not sub:
            msg = "Please enter the subject name!"
            notify_label.config(text=msg, fg=BUTTON_BG)
            text_to_speech(msg)
            return

        master_csv = os.path.join(ATTENDANCE_DIR, sub, f"{sub}.csv")
        if not os.path.exists(master_csv):
            msg = f"No attendance records for '{sub}'"
            notify_label.config(text=msg, fg=BUTTON_BG)
            text_to_speech(msg)
            return

        df = pd.read_csv(master_csv)
        total_sessions = df['Timestamp'].nunique()
        counts = df.groupby(['Enrollment', 'Name']).size().reset_index(name='PresentCount')
        counts['Attendance%'] = (counts['PresentCount'] / total_sessions * 100).round(1)

        # Plot bar chart
        plt.figure()
        plt.bar(counts['Name'], counts['Attendance%'])
        plt.xlabel('Employee')
        plt.ylabel('Attendance %')
        plt.title(f"{sub} - Attendance Rate")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def open_sheets():
        sub = entry_subject.get().strip()
        if not sub:
            msg = "Please enter the subject name!"
            notify_label.config(text=msg, fg=BUTTON_BG)
            text_to_speech(msg)
            return
        subject_dir = os.path.join(ATTENDANCE_DIR, sub)
        if os.path.isdir(subject_dir):
            os.startfile(subject_dir)
        else:
            msg = f"No sheets for '{sub}'"
            notify_label.config(text=msg, fg=BUTTON_BG)
            text_to_speech(msg)

    # Window setup
    win = tk.Tk()
    win.title("Attendance Analytics")
    win.geometry("700x400")
    win.configure(bg=BG_COLOR)
    win.resizable(False, False)
    win.iconbitmap(ICON_PATH)

    # Header
    tk.Label(win, text="View Attendance", bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT_TITLE).pack(pady=20)

    # Input frame
    frame = tk.Frame(win, bg=BG_COLOR)
    frame.pack(pady=10)
    tk.Label(frame, text="Subject:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).grid(row=0, column=0, padx=5)
    entry_subject = tk.Entry(frame, bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL, insertbackground=FG_COLOR)
    entry_subject.grid(row=0, column=1, padx=5)

    notify_label = tk.Label(win, text="", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL)
    notify_label.pack(pady=5)

    # Buttons frame
    btn_frame = tk.Frame(win, bg=BG_COLOR)
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="View Summary", command=calculate_attendance, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BUTTON, padx=15, pady=5).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Check Sheets", command=open_sheets, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BUTTON, padx=15, pady=5).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Show Analytics", command=show_analytics, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BUTTON, padx=15, pady=5).grid(row=0, column=2, padx=10)

    win.mainloop()
