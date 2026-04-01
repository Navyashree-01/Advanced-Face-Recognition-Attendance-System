import os

def menu():
    print("\n" + "="*55)
    print("   🎓 FACE RECOGNITION ATTENDANCE SYSTEM")
    print("="*55)
    print("  1. Register New Student (Capture 30 Photos)")
    print("  2. Train / Retrain Face Model")
    print("  3. Start Attendance Session")
    print("  4. Open Dashboard (Browser)")
    print("  5. Exit")
    print("="*55)
    return input("  Choose option (1-5): ").strip()

while True:
    choice = menu()

    if choice == "1":
        from register_student import register_student
        register_student()

    elif choice == "2":
        from attendance_tracker import train_model
        train_model()

    elif choice == "3":
        subject  = input("\nEnter Subject Name (e.g. Mathematics): ").strip()
        period   = input("Enter Period (e.g. Period 1): ").strip()
        dur      = input("Duration in minutes (default 50): ").strip()
        duration = int(dur) if dur.isdigit() else 50
        from attendance_tracker import run_attendance
        run_attendance(subject, period, duration)

    elif choice == "4":
        print("\n[INFO] Opening dashboard at http://localhost:5000")
        os.system("python dashboard.py")

    elif choice == "5":
        print("\nGoodbye!\n")
        break

    else:
        print("Invalid choice. Try again.")