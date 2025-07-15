import face_recognition
import os

# Call this where you detect an unknown face
from gui_utils import create_gui_start_stop_buttons
create_gui_start_stop_buttons.on_intruder_detected()

def load_known_faces(known_dir="known_faces"):
    """
    Load known face encodings and names from a specified directory.

    :param known_dir: Directory containing images of known faces.
    :return: Tuple containing two lists: known face encodings and corresponding names.
    """
    known_encodings = []
    known_names = []

    # Check if the directory exists
    if not os.path.exists(known_dir):
        print(f"[ERROR] The directory '{known_dir}' does not exist.")
        return [], []  # Return empty lists if the directory doesn't exist

    # Load all images from the known_faces folder
    for filename in os.listdir(known_dir):
        if filename.endswith((".jpg", ".png")):
            image_path = os.path.join(known_dir, filename)
            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    for encoding in encodings:
                        known_encodings.append(encoding)
                        known_names.append(os.path.splitext(filename)[0])
                else:
                    print(f"[WARNING] No face found in {filename}. Skipping.")
            except Exception as e:
                print(f"[ERROR] Failed to process image {filename}: {str(e)}")

    return known_encodings, known_names
