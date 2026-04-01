Project Folder Structure

attendance_system/ 
├── student_photos/ ← Auto-created during registration 
├── attendance_records/ ← Auto-created during attendance 
├── .env ← Your email settings 
├── register_student.py ← STEP 1: Register new student (captures 30 pics)        
├── encode_faces.py ← STEP 2: Train on all registered students 
├── email_sender.py ← Email module 
├── attendance_tracker.py ← STEP 3: Run attendance + track time 
├── dashboard.py ← STEP 4: View records on browser 
└── main.py

Implementation Steps
1.	Install required software (Python, OpenCV, Database).
2.	Collect and store student facial images.
3.	Train the face recognition model.
4.	Capture real-time images using webcam.
5.	Detect and recognize faces.
6.	Mark attendance automatically.
7.	Store attendance data in database.
8.	Generate attendance reports.
Tools & Technologies Used
•	Python
•	OpenCV
•	NumPy
•	Face Recognition Library / Deep Learning Model
•	MySQL / SQLite
•	Webcam

5.1.1	INSTALLATIONS AND LIBRARIES USED

Advanced Face Recognition Attendance System

 Software Installations Required

1.	Python (3.8 or above)
Used as the main programming language for developing the system.
2.	Anaconda (Optional)
Used for managing virtual environments and packages.
3.	Visual Studio Code / PyCharm
Used as an IDE for writing and executing the program.
4.	MySQL / SQLite
Used for storing student details and attendance records.
5.	Webcam Drivers
Required for capturing real-time facial images.


Libraries Used

The following Python libraries are used in the implementation:

1.	OpenCV (cv2)
Used for image processing, face detection, and webcam handling.
2.	NumPy
Used for numerical operations and array handling.
3.	face_recognition
Used for face encoding and face matching.
4.	Pandas
Used for managing attendance records and exporting reports (CSV/Excel).
5.	Datetime
Used to record date and time of attendance.
6.	OS Module
Used for file handling operations.
7.	Tkinter / Flask (Optional)
Used for building graphical user interface or web interface.

RESULTS ANALYSIS
This section describes step-by-step the system analysis and the results obtained. The system was designed and simulated in proteus and a working prototype was developed using the different hardware components with data being sent to the mobile application.


CODE OUTPUT:

<img width="1079" height="573" alt="image" src="https://github.com/user-attachments/assets/a97e27d1-738e-4f18-8c8b-d2ab8006955e" />

  



Fig  : Code Output 
 
<img width="1079" height="573" alt="image" src="https://github.com/user-attachments/assets/dfebcf27-75e8-4279-a134-8f0ddea044bb" />

 
<img width="1079" height="567" alt="image" src="https://github.com/user-attachments/assets/543011ea-cffd-4694-b240-3acf4030d287" />



 
	
Fig  : Application Interface
 
<img width="1079" height="498" alt="image" src="https://github.com/user-attachments/assets/bd589d37-898c-4303-bf1c-402755ef8e4a" />



<img width="1079" height="629" alt="image" src="https://github.com/user-attachments/assets/374778f0-3327-4c57-aee7-2a9524500b34" />

 

Fig : Excel sheet

CONCLUSION
The Advanced Face Recognition Attendance System successfully demonstrates the application of computer vision and machine learning techniques in automating attendance management. The system captures facial images in real time, recognizes individuals using trained models, and records attendance accurately with date and time. This eliminates the need for manual attendance marking and reduces human errors.
The project improves efficiency, saves time, and enhances transparency in attendance tracking. By integrating face recognition technology with database management, the system ensures secure and reliable storage of attendance records. Overall, the developed system provides a smart, automated, and user-friendly solution suitable for schools, colleges, and organizations. With further enhancements, it can be scaled for large institutions and integrated with advanced technologies for even better performance.

