# VisionGuard-AI
VisionGuard AI is a real-time face recognition surveillance system built with Python, OpenCV, and face_recognition. It features a Tkinter GUI for control, detects intruders using facial encoding, and sends automated email alerts with captured snapshots. Ideal for smart, secure monitoring.
Here's a complete **README.md** file for your **VisionGuard AI** project — professional, clean, and GitHub-ready:

## 🚀 Features

- 🔍 Real-time face recognition using `face_recognition` and OpenCV  
- 📸 Automatic snapshot and video recording on detecting intruders  
- 📧 Email alert system with attached intruder image  
- 🖥️ User-friendly GUI with Start/Stop surveillance buttons (Tkinter)  
- 🔐 Stores known face images for comparison and easy customization  
- 💾 Saves all video recordings and intruder captures locally

---

## 🛠️ Tech Stack

- **Language:** Python 3  
- **Libraries:** OpenCV, face_recognition, NumPy, Pillow, smtplib, tkinter  
- **Email Integration:** smtplib, email.message  
- **Configuration:** JSON-based settings for flexibility  
- **GUI:** Tkinter  
- **Video Format:** AVI (XVID codec)

---

## 📂 Project Structure

```

VisionGuardAI/
├── motion\_cam.py               # Main surveillance logic
├── gui\_utils.py                # GUI (start/stop buttons)
├── email\_utils.py             # Email alert handler
├── face\_recognition\_utils.py  # Load known faces
├── config.json                 # Email & face directory config
├── requirements.txt            # Dependencies
├── captured/                   # Stores intruder snapshots & videos
└── known\_faces/                # Images of known people

````

---

## 🧪 How It Works

1. Add images of known individuals in the `known_faces/` directory.
2. Launch `motion_cam.py` → The GUI opens.
3. Click **Start Surveillance** to begin face monitoring.
4. If an unknown face is detected:
   - A snapshot is captured.
   - An email alert is sent with the image.
   - The full video is saved in the `captured/` folder.
5. Click **Stop Surveillance** to stop monitoring.

---

## ⚙️ Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/VisionGuardAI.git
   cd VisionGuardAI
````

2. **Install dependencies**
   *(Use a virtual environment if preferred)*

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your email settings**
   Open `config.json` and update:

   ```json
   {
     "email_sender": "your_email@gmail.com",
     "email_password": "your_app_password",
     "email_receiver": "receiver_email@gmail.com",
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 587,
     "known_faces_dir": "known_faces"
   }
   ```

4. **Run the application**

   ```bash
   python motion_cam.py
   ```

---

## 🔐 Security Note

For Gmail, generate an **App Password** if 2FA is enabled. Do **not** use your personal password.
Avoid uploading sensitive config files or credentials to GitHub.

---

## 📌 Future Improvements

* Multi-camera support
* Web-based dashboard (Flask/React)
* SMS/push alerts (Twilio or Firebase)
* SQLite logging of events and access history
* Face registration interface for adding new known users dynamically

---

## 🤝 Contributing

Pull requests are welcome! If you'd like to add features or fix bugs, feel free to fork the repo and submit a PR.

---


