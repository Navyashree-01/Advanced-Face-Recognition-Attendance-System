import os
import pickle

STUDENT_PHOTOS_DIR = "student_photos"

def encode_all_students():
    import face_recognition
    known_encodings = []
    known_names = []
    known_rolls = []

    students = [d for d in os.listdir(STUDENT_PHOTOS_DIR)
                if os.path.isdir(os.path.join(STUDENT_PHOTOS_DIR, d))]

    print(f"Training on {len(students)} student(s)...")

    for student_folder in students:
        parts = student_folder.split("_", 1)
        roll_no = parts[0]
        name = parts[1] if len(parts) > 1 else student_folder
        folder_path = os.path.join(STUDENT_PHOTOS_DIR, student_folder)
        photos = [f for f in os.listdir(folder_path)
                  if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        encoded = 0
        for photo_file in photos:
            try:
                image = face_recognition.load_image_file(
                    os.path.join(folder_path, photo_file))
                encs = face_recognition.face_encodings(image)
                if encs:
                    known_encodings.append(encs[0])
                    known_names.append(name)
                    known_rolls.append(roll_no)
                    encoded += 1
            except Exception as e:
                print(f"  Skipped: {e}")
        print(f"  OK: {name} ({roll_no}) - {encoded}/{len(photos)} encoded")

    with open("face_data.pkl", "wb") as f:
        pickle.dump({
            "encodings": known_encodings,
            "names": known_names,
            "rolls": known_rolls
        }, f)

    print(f"SUCCESS: Trained {len(set(known_rolls))} student(s) - {len(known_encodings)} encodings saved!")

if __name__ == "__main__":
    encode_all_students()