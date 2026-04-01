import cv2
import os
import time
from PIL import Image

STUDENT_PHOTOS_DIR = "student_photos"
PHOTOS_PER_STUDENT = 30

def register_student():
    if not os.path.isdir(STUDENT_PHOTOS_DIR):
        if os.path.exists(STUDENT_PHOTOS_DIR):
            os.remove(STUDENT_PHOTOS_DIR)
        os.mkdir(STUDENT_PHOTOS_DIR)

    print("\n" + "="*50)
    print("   STUDENT REGISTRATION")
    print("="*50)
    roll = input("Enter Roll Number (e.g. 628): ").strip().upper()
    name = input("Enter Student Name (e.g. Navya): ").strip().title()

    folder_name = f"{roll}_{name}"
    save_path = os.path.join(STUDENT_PHOTOS_DIR, folder_name)

    if os.path.exists(save_path):
        print(f"\n[WARNING] {name} ({roll}) already registered!")
        choice = input("Re-register? (y/n): ").strip().lower()
        if choice != 'y':
            print("Cancelled.")
            return
        for f in os.listdir(save_path):
            os.remove(os.path.join(save_path, f))
    else:
        os.makedirs(save_path)

    print(f"\n[INFO] Camera starting for {name} ({roll})")
    print("[INFO] Sit close, face camera directly, good lighting")
    print("[INFO] Press A = Auto capture | SPACE = Manual | Q = Quit\n")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    photo_count = 0
    auto_mode = False

    while photo_count < PHOTOS_PER_STUDENT:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(80, 80))
        face_detected = len(faces) > 0

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.rectangle(frame, (0, 0), (640, 50), (20, 20, 20), cv2.FILLED)
        cv2.putText(frame, f"Student: {name} ({roll})", (10, 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        cv2.putText(frame, f"Photos: {photo_count}/{PHOTOS_PER_STUDENT} | A=Auto SPACE=Manual Q=Quit",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (180, 180, 180), 1)

        bar_width = int((photo_count / PHOTOS_PER_STUDENT) * 620)
        cv2.rectangle(frame, (10, 460), (630, 475), (50, 50, 50), cv2.FILLED)
        cv2.rectangle(frame, (10, 460), (10 + bar_width, 475), (0, 220, 100), cv2.FILLED)

        status = "FACE DETECTED - Ready!" if face_detected else "NO FACE - Move closer / improve lighting"
        color = (0, 255, 100) if face_detected else (0, 100, 255)
        cv2.putText(frame, status, (10, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.42, color, 1)

        cv2.imshow("Student Registration", frame)
        key = cv2.waitKey(1) & 0xFF

        if auto_mode and face_detected:
            time.sleep(0.35)
            ret2, frame2 = cap.read()
            if ret2:
                filename = os.path.join(save_path, f"photo_{photo_count+1:02d}.jpg")
                rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                Image.fromarray(rgb).save(filename)
                photo_count += 1
                print(f"  [AUTO] Photo {photo_count}/{PHOTOS_PER_STUDENT} saved")

        elif key == ord(' ') and face_detected:
            filename = os.path.join(save_path, f"photo_{photo_count+1:02d}.jpg")
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            Image.fromarray(rgb).save(filename)
            photo_count += 1
            print(f"  [CAPTURED] Photo {photo_count}/{PHOTOS_PER_STUDENT}")

        elif key == ord('a'):
            auto_mode = not auto_mode
            print(f"  [AUTO MODE] {'ON' if auto_mode else 'OFF'}")

        elif key == ord('q'):
            print("\n[CANCELLED]")
            cap.release()
            cv2.destroyAllWindows()
            return

    cap.release()
    cv2.destroyAllWindows()

    if photo_count == PHOTOS_PER_STUDENT:
        print(f"\n[SUCCESS] {photo_count} photos saved for {name} ({roll})")
    else:
        print(f"\n[INCOMPLETE] Only {photo_count} photos. Re-register.")

if __name__ == "__main__":
    register_student()