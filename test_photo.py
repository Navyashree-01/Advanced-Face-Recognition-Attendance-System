import face_recognition
import os

folder = "student_photos"
for student in os.listdir(folder):
    student_path = os.path.join(folder, student)
    if not os.path.isdir(student_path):
        continue
    print(f"Testing: {student}")
    photos = os.listdir(student_path)
    for photo in photos[:3]:
        photo_path = os.path.join(student_path, photo)
        try:
            img = face_recognition.load_image_file(photo_path)
            print(f"  Loaded: {photo} shape={img.shape}")
            locations = face_recognition.face_locations(img)
            print(f"  Faces: {len(locations)}")
        except Exception as e:
            print(f"  Error: {e}")