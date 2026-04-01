import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# ===== ADD YOUR STUDENT EMAILS HERE =====
STUDENT_EMAILS = {
    "628":    "23.628navyashree@gmail.com",
    "6628":   "23.628navyashree@gmail.com",
}
# =========================================

def send_absence_email(student_name, roll_no, subject_name, date, period):
    student_email = STUDENT_EMAILS.get(roll_no)
    if not student_email:
        print(f"  [SKIP] No email registered for roll: {roll_no}")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Absence Alert - {subject_name} | {date}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = student_email

    html = f"""
    <html><body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
    <div style="max-width:560px;margin:auto;background:white;border-radius:12px;overflow:hidden;">
        <div style="background:linear-gradient(135deg,#1a1a2e,#e74c3c);padding:25px;text-align:center;">
            <h2 style="color:white;margin:0;">Absence Notification</h2>
        </div>
        <div style="padding:25px;">
            <p>Dear <strong>{student_name}</strong>,</p>
            <p>You were marked <strong style="color:red;">ABSENT</strong> for:</p>
            <table style="width:100%;border-collapse:collapse;margin:15px 0;">
                <tr style="background:#f8f9fa;">
                    <td style="padding:10px;color:#888;">Subject</td>
                    <td style="padding:10px;"><strong>{subject_name}</strong></td>
                </tr>
                <tr>
                    <td style="padding:10px;color:#888;">Date</td>
                    <td style="padding:10px;">{date}</td>
                </tr>
                <tr style="background:#f8f9fa;">
                    <td style="padding:10px;color:#888;">Period</td>
                    <td style="padding:10px;">{period}</td>
                </tr>
                <tr>
                    <td style="padding:10px;color:#888;">Roll No</td>
                    <td style="padding:10px;">{roll_no}</td>
                </tr>
            </table>
            <p style="color:#555;font-size:13px;">Contact your teacher if this is an error.</p>
            <p style="color:#aaa;font-size:11px;">— Automated Attendance System</p>
        </div>
    </div>
    </body></html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, student_email, msg.as_string())
        print(f"  [EMAIL SENT] Absence alert sent to {student_name} ({student_email})")
        return True
    except Exception as e:
        print(f"  [EMAIL FAILED] {student_name}: {e}")
        return False


def send_bulk_absence_emails(absent_students, subject_name, date, period):
    if not absent_students:
        print("\n[INFO] All students present! No emails needed.")
        return
    print(f"\n[EMAIL] Sending absence alerts to {len(absent_students)} student(s)...")
    for s in absent_students:
        send_absence_email(s["name"], s["roll"], subject_name, date, period)


