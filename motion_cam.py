import cv2
import face_recognition
import os
import json
from datetime import datetime
import tkinter as tk
from gui_utils import create_gui_start_stop_buttons
from email_utils import send_email  # Ensure this import is correct
import threading
import time
import numpy as np

# Event to manage surveillance status
surveillance_event = threading.Event()

# Function to stop surveillance
def stop_surveillance_func():
    print("[INFO] Stopping surveillance...")
    surveillance_event.set()  # Trigger the stop event

# Function to start surveillance
def start_surveillance_func():
    print("[INFO] Starting surveillance...")
    surveillance_event.clear()  # Reset the stop event
    start_video_capture_thread()

# Function for video capture in a separate thread
def start_video_capture_thread():
    video_thread = threading.Thread(target=start_video_capture)
    video_thread.start()

def start_video_capture():
    # Load config
    with open("config.json", "r") as f:
        config = json.load(f)

    KNOWN_FACES_DIR = config.get("known_faces_dir", "known_faces")
    VIDEO_OUTPUT_DIR = "captured"
    os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

    # Load known faces
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)

            if len(face_locations) == 0:
                print(f"[WARNING] No face found in {filename}. Skipping.")
                continue

            face_encoding = face_recognition.face_encodings(image, face_locations)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])

    # Initialize camera
    video_capture = cv2.VideoCapture(0)

    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = os.path.join(VIDEO_OUTPUT_DIR, f"capture_{timestamp}.avi")
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))

    print("[INFO] Surveillance started. Press 'q' to stop.")

    sent_intruder_pics = []  # List of encodings already sent

    while not surveillance_event.is_set():
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Failed to read from camera.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            face_names.append(name)

            if name == "Unknown":
                already_sent = False
                for known_encoding in sent_intruder_pics:
                    match = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.6)[0]
                    if match:
                        already_sent = True
                        break

                if not already_sent and len(sent_intruder_pics) < 2:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    intruder_filename = os.path.join("captured", f"intruder_{timestamp}.jpg")
                    cv2.imwrite(intruder_filename, frame)
                    send_email(
                        subject="Intruder Detected",
                        body="An intruder was detected. See attached photo.",
                        attachment_path=intruder_filename
                    )
                    sent_intruder_pics.append(face_encoding)

        # Display results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        out.write(frame)
        cv2.imshow('Surveillance', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            surveillance_event.set()

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

# Create the GUI with start and stop buttons
def run_gui():
    create_gui_start_stop_buttons(start_surveillance_func, stop_surveillance_func)

# Run the GUI
run_gui()
