# Face-Recognition-Attendance-System
This project is an AI-powered attendance system that uses face recognition to automatically log employee presence. It simplifies workforce tracking by enrolling users via webcam and marking attendance in real-time. A modern web frontend and admin dashboard provide visibility into daily and historical records through intuitive visualizations.

## 🛠️ Tools and Technologies Used

### 🐍 Programming Language
- **Python 3.9+**  
  - Primary development language chosen for its simplicity, readability, and extensive third-party library support.

---

### 🧱 Libraries and Frameworks

#### 🔧 GUI Development
- **Tkinter**  
  - Standard Python GUI library used to create the desktop interface for login, registration, and attendance workflows.

#### 📷 Computer Vision
- **OpenCV**  
  - Handles webcam video stream, face detection, and real-time image processing.
- **LBPH (Local Binary Patterns Histogram)**  
  - Face recognition algorithm used for accurate and lightweight facial identification.

#### 📊 Data Handling
- **Pandas**  
  - Manipulates tabular data (employee info and attendance logs).
- **NumPy**  
  - Powers numerical computations and image matrix transformations.
- **CSV (Python Standard Library)**  
  - Reads and writes structured data to .csv files for records management.

---

### 📈 Visualization & Reporting
- **Matplotlib**  
  - Creates attendance charts and analytics visuals for reports and dashboards.

---

### 🖼️ Image Handling
- **Pillow (PIL)**  
  - Used for GUI image rendering and resizing (e.g., icons and logos).

---

### 🔐 Authentication & Access Control
- **CSV-Based Authentication**  
  - Stores user credentials (admin/viewer) in a local file.
  - Provides role-based access control.
- **bcrypt** *(optional)*  
  - Originally used for password hashing (now optional for simplicity).

---

### 📲 Notifications (Optional)
- **Twilio API**  
  - Sends automated WhatsApp/SMS notifications for presence or absence alerts.

---

### 🧑‍💻 Development Tools
- **Visual Studio Code**  
  - IDE used for coding, debugging, and managing dependencies.
- **Python venv**  
  - Creates isolated environments for package management.
- **Git**  
  - Enables version control and code collaboration.

---

### 💻 Hardware Requirements
- **Webcam**  
  - HD or higher resolution recommended for capturing facial features.
- **Local Disk Storage**  
  - Stores captured images, trained models, and CSV-based records.

---

This collection of technologies ensures that the Attendance Management System is efficient, reliable, and scalable, while remaining accessible for future development and enhancements.
