import tkinter as tk
import os, cv2, csv, time, datetime
import pandas as pd
from twilio_notify import send_sms, send_whatsapp

# Base paths
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH    = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
LABEL_PATH      = os.path.join(BASE_DIR, "TrainingImageLabel", "Trainner.yml")
STUDENT_CSV     = os.path.join(BASE_DIR, "StudentDetails", "studentdetails.csv")
ATTENDANCE_DIR  = os.path.join(BASE_DIR, "Attendance")
UI_DIR          = os.path.join(BASE_DIR, "UI_Image")
ICON_PATH       = os.path.join(UI_DIR, "AMS.ico")

# Ensure attendance directory exists
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# Theme configuration
BG_COLOR       = "#2E3440"
FG_COLOR       = "#ECEFF4"
ACCENT_COLOR   = "#88C0D0"
BUTTON_BG      = "#5E81AC"
BUTTON_FG      = "#ECEFF4"
FONT_TITLE     = ("Segoe UI", 24, "bold")
FONT_LABEL     = ("Segoe UI", 14)
FONT_BUTTON    = ("Segoe UI", 12)


def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = entry_subject.get().strip()
        if not sub:
            msg = "Please enter the subject name!"
            notify_label.config(text=msg, fg=BUTTON_BG)
            text_to_speech(msg)
            return

        # Load recognizer and student data
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(LABEL_PATH)
        faceCascade = cv2.CascadeClassifier(CASCADE_PATH)
        try:
            df_students = pd.read_csv(STUDENT_CSV)
        except FileNotFoundError:
            notify_label.config(text="Student CSV not found.", fg=BUTTON_BG)
            return

        # Track seen IDs
        seen_ids = set()
        records = []

        cam = cv2.VideoCapture(0)
        font_cv = cv2.FONT_HERSHEY_SIMPLEX
        start_time = time.time()

        while True:
            ret, frame = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                if conf < 70 and Id not in seen_ids:
                    # Safe lookup of name
                    matches = df_students.loc[df_students["Enrollment"] == Id, "Name"].values
                    name_val = matches[0] if len(matches) > 0 else "Unknown"
                    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    records.append({"Enrollment": Id, "Name": name_val, "Timestamp": ts})
                    seen_ids.add(Id)
                # draw
                color = (0, 255, 0) if (conf < 70) else (0, 0, 255)
                label_text = f"{Id}-{name_val}" if conf < 70 else "Unknown"
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label_text, (x, y-10), font_cv, 0.8, (255,255,255), 2)

            cv2.imshow("Filling Attendance...", frame)
            if cv2.waitKey(30) == 27 or time.time() - start_time > 20:
                break

        cam.release()
        cv2.destroyAllWindows()

        # Build DataFrame
        attendance_df = pd.DataFrame(records)

        # Update master CSV per subject
        subject_dir = os.path.join(ATTENDANCE_DIR, sub)
        os.makedirs(subject_dir, exist_ok=True)
        master_csv = os.path.join(subject_dir, f"{sub}.csv")

        if os.path.exists(master_csv):
            master_df = pd.read_csv(master_csv)
        else:
            master_df = pd.DataFrame(columns=["Enrollment", "Name", "Timestamp"])

        combined = pd.concat([master_df, attendance_df], ignore_index=True)
        combined.drop_duplicates(subset=["Enrollment"], keep="first", inplace=True)
        combined.to_csv(master_csv, index=False)

        msg = f"Attendance updated for {sub}"
        notify_label.config(text=msg, fg=ACCENT_COLOR)
        text_to_speech(msg)

        # Display combined sheet
        sheet = tk.Toplevel()
        sheet.title(f"Attendance: {sub}")
        sheet.configure(bg=BG_COLOR)
        for r, row in combined.iterrows():
            for c, val in enumerate(row):
                tk.Label(sheet, text=val, bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL, relief=tk.RIDGE, width=12).grid(row=r, column=c, padx=2, pady=2)
        sheet.mainloop()

    def CheckSheets():
        sub = entry_subject.get().strip()
        if not sub:
            notify_label.config(text="Please enter subject!", fg=BUTTON_BG)
            return
        subject_dir = os.path.join(ATTENDANCE_DIR, sub)
        if os.path.isdir(subject_dir):
            os.startfile(subject_dir)
        else:
            notify_label.config(text=f"No sheets for '{sub}'", fg=BUTTON_BG)

    # UI setup
    win = tk.Tk()
    win.title("Class Vision - Automatic Attendance")
    win.geometry("600x400")
    win.configure(bg=BG_COLOR)
    win.resizable(False, False)
    win.iconbitmap(ICON_PATH)

    tk.Label(win, text="Automatic Attendance", bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT_TITLE).pack(pady=20)

    frame = tk.Frame(win, bg=BG_COLOR)
    frame.pack(pady=10)
    tk.Label(frame, text="Subject:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).grid(row=0, column=0)
    entry_subject = tk.Entry(frame, bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL, insertbackground=FG_COLOR)
    entry_subject.grid(row=0, column=1)

    notify_label = tk.Label(win, text="", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL)
    notify_label.pack(pady=5)

    btn_frame = tk.Frame(win, bg=BG_COLOR)
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Fill Attendance", command=FillAttendance, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BUTTON).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Check Sheets", command=CheckSheets, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_BUTTON).grid(row=0, column=1, padx=10)

    win.mainloop()
