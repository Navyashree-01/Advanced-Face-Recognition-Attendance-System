import cv2
import os
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image


def build_student_db():
    STUDENT_PHOTOS_DIR = "student_photos"
    db = {}
    if not os.path.exists(STUDENT_PHOTOS_DIR):
        return db
    for folder in os.listdir(STUDENT_PHOTOS_DIR):
        folder_path = os.path.join(STUDENT_PHOTOS_DIR, folder)
        if not os.path.isdir(folder_path):
            continue
        parts = folder.split("_", 1)
        roll = parts[0]
        name = parts[1] if len(parts) > 1 else folder
        photos = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if photos:
            db[roll] = {"name": name, "roll": roll, "photos": photos}
    return db


def train_model():
    from deepface import DeepFace
    db = build_student_db()
    if not db:
        print("[ERROR] No students found!")
        return False

    print(f"\n[INFO] Training on {len(db)} student(s)...")
    encodings = {}
    for roll, info in db.items():
        embs = []
        for photo_path in info["photos"]:
            try:
                result = DeepFace.represent(
                    img_path=photo_path,
                    model_name="Facenet",
                    enforce_detection=False
                )
                if result:
                    embs.append(result[0]["embedding"])
            except Exception as e:
                pass
        if embs:
            encodings[roll] = {
                "name": info["name"],
                "roll": roll,
                "embedding": np.mean(embs, axis=0)
            }
            print(f"  [OK] {info['name']} ({roll}) - {len(embs)}/{len(info['photos'])} encoded")
        else:
            print(f"  [SKIP] {info['name']} - no face detected in photos")

    if not encodings:
        print("[ERROR] No faces encoded!")
        return False

    with open("face_data.pkl", "wb") as f:
        pickle.dump(encodings, f)
    print(f"\n[SUCCESS] Trained {len(encodings)} student(s)! Ready for attendance.")
    return True


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def run_attendance(subject, period, duration_minutes=50):
    from deepface import DeepFace
    from email_sender import send_bulk_absence_emails

    if not os.path.exists("face_data.pkl"):
        print("[ERROR] No face data! Run Option 2 first.")
        return

    with open("face_data.pkl", "rb") as f:
        encodings = pickle.load(f)

    if not encodings:
        print("[ERROR] No faces trained! Run Option 2 first.")
        return

    student_data = {}
    for roll, info in encodings.items():
        student_data[roll] = {
            "name": info["name"],
            "roll": roll,
            "first_seen": None,
            "last_seen": None,
            "total_seconds": 0,
            "status": "ABSENT",
            "detection_count": 0
        }

    date = datetime.now().strftime("%Y-%m-%d")
    end_time = datetime.now() + timedelta(minutes=duration_minutes)

    print(f"\n{'='*55}")
    print(f"  ATTENDANCE STARTED")
    print(f"  Subject : {subject} | Period: {period}")
    print(f"  Duration: {duration_minutes} min | Students: {len(student_data)}")
    print(f"  Press Q to end")
    print(f"{'='*55}\n")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("[ERROR] Camera not found!")
        return

    SIMILARITY_THRESHOLD = 0.70
    FRAME_SKIP = 5
    MIN_PRESENT_SECONDS = 30
    frame_count = 0

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    while datetime.now() < end_time:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        display = frame.copy()

        if frame_count % FRAME_SKIP == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(60, 60))

            for (x, y, w, h) in faces:
                face_crop = frame[y:y+h, x:x+w]
                if face_crop.size == 0:
                    continue

                try:
                    rgb_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(rgb_crop)
                    temp_path = "temp_face.jpg"
                    pil_img.save(temp_path)

                    result = DeepFace.represent(
                        img_path=temp_path,
                        model_name="Facenet",
                        enforce_detection=False
                    )

                    if not result:
                        continue

                    face_emb = result[0]["embedding"]

                    best_roll = None
                    best_sim = 0
                    for roll, info in encodings.items():
                        sim = cosine_similarity(face_emb, info["embedding"])
                        if sim > best_sim:
                            best_sim = sim
                            best_roll = roll

                    if best_roll and best_sim >= SIMILARITY_THRESHOLD:
                        s = student_data[best_roll]
                        now = datetime.now()
                        s["detection_count"] += 1

                        if s["first_seen"] is None:
                            s["first_seen"] = now
                            print(f"  [SEEN] {s['name']} ({best_roll}) at {now.strftime('%H:%M:%S')}")

                        if s["last_seen"] is not None:
                            gap = (now - s["last_seen"]).total_seconds()
                            if gap <= 15:
                                s["total_seconds"] += gap
                        s["last_seen"] = now

                        if s["total_seconds"] >= MIN_PRESENT_SECONDS:
                            if s["status"] != "PRESENT":
                                print(f"  [PRESENT] {s['name']} confirmed! {int(s['total_seconds'])}s")
                            s["status"] = "PRESENT"

                        color = (0, 220, 80) if s["status"] == "PRESENT" else (0, 220, 255)
                        time_min = round(s["total_seconds"] / 60, 1)
                        conf = round(best_sim * 100, 1)

                        cv2.rectangle(display, (x, y), (x+w, y+h), color, 2)
                        cv2.rectangle(display, (x, y+h), (x+w, y+h+45), color, cv2.FILLED)
                        cv2.putText(display, f"{s['name']} {conf}%",
                                    (x+4, y+h+16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,0), 1)
                        cv2.putText(display, f"{time_min}min | {s['status']}",
                                    (x+4, y+h+34), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0,0,0), 1)
                    else:
                        cv2.rectangle(display, (x, y), (x+w, y+h), (0, 0, 200), 2)
                        cv2.putText(display, "Unknown", (x+4, y+h+16),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 200), 1)

                except Exception as e:
                    cv2.rectangle(display, (x, y), (x+w, y+h), (0, 0, 200), 2)

        present = sum(1 for s in student_data.values() if s["status"] == "PRESENT")
        total = len(student_data)
        remaining = max(0, int((end_time - datetime.now()).total_seconds() / 60))

        cv2.rectangle(display, (0, 0), (640, 40), (15, 15, 15), cv2.FILLED)
        cv2.putText(display,
                    f"{subject} | Present:{present}/{total} | Left:{remaining}min | Q=End",
                    (8, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 255, 200), 1)

        cv2.imshow("Attendance System", display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n[INFO] Session ended.")
            break

    cap.release()
    cv2.destroyAllWindows()
    if os.path.exists("temp_face.jpg"):
        os.remove("temp_face.jpg")

    os.makedirs("attendance_records", exist_ok=True)
    records = []
    for s in student_data.values():
        records.append({
            "Date": date, "Subject": subject, "Period": period,
            "Roll No": s["roll"], "Name": s["name"], "Status": s["status"],
            "First Seen": s["first_seen"].strftime("%H:%M:%S") if s["first_seen"] else "Absent",
            "Last Seen": s["last_seen"].strftime("%H:%M:%S") if s["last_seen"] else "Absent",
            "Time in Class (min)": round(s["total_seconds"] / 60, 2),
            "Detections": s["detection_count"]
        })

    df = pd.DataFrame(records)
    fname = f"attendance_records/attendance_{subject.replace(' ','_')}_{date}_{period.replace(' ','_')}.xlsx"
    df.to_excel(fname, index=False)

    present = sum(1 for s in student_data.values() if s["status"] == "PRESENT")
    total = len(student_data)
    print(f"\n{'='*55}")
    print(f"  Present : {present}/{total}")
    print(f"  Absent  : {total-present}")
    print(f"  Saved   : {fname}")
    print(f"{'='*55}")

    absent = [s for s in student_data.values() if s["status"] == "ABSENT"]
    send_bulk_absence_emails(absent, subject, date, period)