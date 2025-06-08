import tkinter as tk
from tkinter import messagebox
import os, cv2, shutil, csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd, datetime, time
import tkinter.font as tkfont
import pyttsx3

# project modules
import takeImage
import trainImage
import automaticAttedance
import show_attendance

# Base directory for project resources
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
USERS_CSV       = os.path.join(BASE_DIR, "users.csv")
CASCADE_PATH    = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
TRAIN_IMAGE_DIR = os.path.join(BASE_DIR, "TrainingImage")
LABEL_PATH      = os.path.join(BASE_DIR, "TrainingImageLabel", "Trainner.yml")
STUDENT_CSV     = os.path.join(BASE_DIR, "StudentDetails", "studentdetails.csv")
ATTENDANCE_DIR  = os.path.join(BASE_DIR, "Attendance")
UI_DIR          = os.path.join(BASE_DIR, "UI_Image")
ICON_PATH       = os.path.join(UI_DIR, "AMS.ico")

# Ensure necessary directories exist
os.makedirs(TRAIN_IMAGE_DIR, exist_ok=True)
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# === Theme configuration ===
BG_COLOR       = "#2E3440"
FG_COLOR       = "#ECEFF4"
ACCENT_COLOR   = "#88C0D0"
BUTTON_BG      = "#5E81AC"
BUTTON_FG      = "#ECEFF4"
FONT_TITLE     = ("Segoe UI", 32, "bold")
FONT_SUBTITLE  = ("Segoe UI", 18)
FONT_LABEL     = ("Segoe UI", 14)
FONT_BUTTON    = ("Segoe UI", 14)

# Text-to-speech helper
def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# -- Authentication without bcrypt --
def check_credentials(username, password):
    try:
        with open(USERS_CSV, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'].strip() == username.strip() \
and row['password'].strip() == password.strip():

                    return True, row['role']
    except FileNotFoundError:
        messagebox.showerror("Error", "users.csv not found.")
    return False, None

def show_login():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x200")
    login.configure(bg=BG_COLOR)
    login.resizable(False, False)

    tk.Label(login, text="Username:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).pack(pady=(20,0))
    user_ent = tk.Entry(login, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
    user_ent.pack()
    tk.Label(login, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).pack(pady=(10,0))
    pass_ent = tk.Entry(login, show="*", bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
    pass_ent.pack()

    def attempt_login():
        ok, role = check_credentials(user_ent.get().strip(), pass_ent.get().strip())
        if ok:
            login.destroy()
            launch_main_app(role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(login, text="Login", command=attempt_login, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BUTTON).pack(pady=20)
    login.mainloop()

# -- Main Application --
def launch_main_app(user_role):
    window = tk.Tk()
    window.title("Punjab State Power Corporation Limited")
    window.geometry("1280x720")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)
    window.iconbitmap(ICON_PATH)

    # Header
    header_frame = tk.Frame(window, bg=BG_COLOR)
    header_frame.pack(fill="x", pady=10)
    logo = Image.open(os.path.join(UI_DIR, "0001.png")).resize((60, 60), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo)
    tk.Label(header_frame, image=logo_img, bg=BG_COLOR).pack(side="left", padx=20)
    title_frame = tk.Frame(header_frame, bg=BG_COLOR)
    title_frame.pack(side="left")
    tk.Label(title_frame, text="Punjab State Power Corporation Limited", bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT_TITLE).pack(anchor="w")
    tk.Label(title_frame, text="Attendance System", bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT_SUBTITLE).pack(anchor="w")

    # Register Employee UI
    def RegisterUI():
        reg_win = tk.Toplevel(window)
        reg_win.title("Register Employee")
        reg_win.geometry("400x350")
        reg_win.configure(bg=BG_COLOR)
        reg_win.resizable(False, False)
        tk.Label(reg_win, text="Enrollment No:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).pack(pady=(20,5))
        er_entry = tk.Entry(reg_win, bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL, insertbackground=FG_COLOR)
        er_entry.pack(pady=5)
        tk.Label(reg_win, text="Name:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).pack(pady=(20,5))
        name_entry = tk.Entry(reg_win, bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL, insertbackground=FG_COLOR)
        name_entry.pack(pady=5)
        notify = tk.Label(reg_win, text="", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL)
        notify.pack(pady=10)
        btn_frame = tk.Frame(reg_win, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Take Images", command=lambda: takeImage.TakeImage(er_entry.get().strip(), name_entry.get().strip(), CASCADE_PATH, TRAIN_IMAGE_DIR, notify, lambda: None, text_to_speech), bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BUTTON, padx=10, pady=5).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Train Model", command=lambda: trainImage.TrainImage(CASCADE_PATH, TRAIN_IMAGE_DIR, LABEL_PATH, notify, text_to_speech), bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BUTTON, padx=10, pady=5).grid(row=0, column=1, padx=10)

    # Main actions
    actions = [
        ("Register Employee", "register.png", RegisterUI),
        ("Take Attendance", "attendance.png", lambda: automaticAttedance.subjectChoose(text_to_speech)),
        ("View Attendance", "verifyy.png", lambda: show_attendance.subjectchoose(text_to_speech))
    ]

    # Action buttons
    main_frame = tk.Frame(window, bg=BG_COLOR)
    main_frame.pack(expand=True)
    btn_widgets = []
    for idx, (label, icon, cmd) in enumerate(actions):
        frm = tk.Frame(main_frame, bg=BG_COLOR)
        frm.grid(row=0, column=idx, padx=60)
        img = Image.open(os.path.join(UI_DIR, icon)).resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        btn = tk.Button(
            frm,
            image=photo,
            text=label,
            compound="top",
            command=cmd,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            font=FONT_BUTTON,
            bd=0,
            width=160,
            height=160,
            activebackground=ACCENT_COLOR
        )
        btn.image = photo
        btn.pack()
        btn_widgets.append(btn)

    # Disable registration if not admin
    if user_role != "administrator":
        btn_widgets[0].config(state=tk.DISABLED)

    # Footer
    footer_frame = tk.Frame(window, bg=BG_COLOR)
    footer_frame.pack(fill="x", pady=20)
    tk.Button(
        footer_frame,
        text="Exit",
        command=window.quit,
        bg="#BF616A",
        fg=BUTTON_FG,
        font=FONT_BUTTON,
        bd=0,
        width=12,
        height=1
    ).pack(side="right", padx=30)

    window.mainloop()

if __name__ == "__main__":
    show_login()
