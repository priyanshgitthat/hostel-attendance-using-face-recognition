import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import csv
import os
from datetime import datetime
import cv2
import face_recognition
import pickle
import winsound
import time
import mediapipe as mp  # This is the missing import

# Set appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class FaceRecognitionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Face Recognition Attendance System")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Logo label
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FRAS", 
                                     font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar buttons
        self.add_student_btn = ctk.CTkButton(self.sidebar_frame, text="Add Student", 
                                           command=self.show_add_student_frame)
        self.add_student_btn.grid(row=1, column=0, padx=20, pady=10)
        
        self.mark_attendance_btn = ctk.CTkButton(self.sidebar_frame, text="Mark Attendance", 
                                                command=self.show_mark_attendance_frame)
        self.mark_attendance_btn.grid(row=2, column=0, padx=20, pady=10)
        
        self.view_attendance_btn = ctk.CTkButton(self.sidebar_frame, text="View Attendance Log", 
                                                command=self.show_attendance_log_frame)
        self.view_attendance_btn.grid(row=3, column=0, padx=20, pady=10)
        
        # Appearance mode option menu
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, 
                                                           values=["Light", "Dark", "System"],
                                                           command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(0, 10))
        
        # Main content frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Initialize frames
        self.add_student_frame = None
        self.mark_attendance_frame = None
        self.attendance_log_frame = None
        self.capturing = False  # Flag for capture process
        
        # Show default frame
        self.show_mark_attendance_frame()
        
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_add_student_frame(self):
        self.clear_main_frame()
        
        self.add_student_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.add_student_frame.grid(row=0, column=0, sticky="nsew")
        self.add_student_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self.add_student_frame, text="Add New Student", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Form frame
        form_frame = ctk.CTkFrame(self.add_student_frame, corner_radius=10)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Name entry
        name_label = ctk.CTkLabel(form_frame, text="Student Name:")
        name_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter student name")
        self.name_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")
        
        # Roll number entry
        roll_label = ctk.CTkLabel(form_frame, text="Roll Number:")
        roll_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.roll_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter roll number")
        self.roll_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        # Add button
        add_btn = ctk.CTkButton(form_frame, text="Capture Faces", 
                                command=self.capture_faces, 
                                fg_color="#2e8b57", hover_color="#3cb371")
        add_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        # Stop button
        self.stop_btn = ctk.CTkButton(form_frame, text="Stop Capture",
                                    command=self.stop_capture,
                                    fg_color="#ff6347", hover_color="#ff4500",
                                    state="disabled")
        self.stop_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        # Status label
        self.status_label = ctk.CTkLabel(self.add_student_frame, text="", text_color="#2e8b57")
        self.status_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        # Camera preview frame
        self.camera_preview = ctk.CTkLabel(self.add_student_frame, text="Camera preview will appear here")
        self.camera_preview.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
    
    def stop_capture(self):
        """Stop the face capture process"""
        self.capturing = False
        self.status_label.configure(text="Capture stopped by user", text_color="orange")
        self.stop_btn.configure(state="disabled")
    
    def capture_faces(self):
        name = self.name_entry.get()
        roll_no = self.roll_entry.get()
        
        if not name or not roll_no:
            self.status_label.configure(text="Please enter both name and roll number", text_color="red")
            return
        
        self.status_label.configure(text=f"Preparing to capture faces for {name}...", text_color="#2e8b57")
        self.stop_btn.configure(state="normal")
        self.update()
        
        # Call your face capture function here
        self.add_student_face(name, roll_no)
        
    def add_student_face(self, name, roll_no):
        folder_name = f"dataset/{name}_{roll_no}"
        os.makedirs(folder_name, exist_ok=True)

        # Initialize MediaPipe face detection
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        
        # Initialize face detection
        with mp_face_detection.FaceDetection(
            model_selection=0, 
            min_detection_confidence=0.6
        ) as face_detection:

            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.status_label.configure(text="Error: Could not open camera", text_color="red")
                return

            count = 0
            total_images = 10
            last_capture_time = time.time()
            self.capturing = True  # Flag to control capture loop

            while self.capturing and count < total_images:
                ret, frame = cap.read()
                if not ret:
                    self.status_label.configure(text="Error reading frame", text_color="red")
                    break

                # Apply histogram equalization for lighting normalization
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
                frame[:, :, 0] = cv2.equalizeHist(frame[:, :, 0])
                frame = cv2.cvtColor(frame, cv2.COLOR_YCrCb2BGR)

                # Convert to RGB for MediaPipe
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(frame_rgb)

                if results.detections:
                    for detection in results.detections:
                        # Get face bounding box
                        bbox = detection.location_data.relative_bounding_box
                        h, w, _ = frame.shape
                        x = int(bbox.xmin * w)
                        y = int(bbox.ymin * h)
                        w_box = int(bbox.width * w)
                        h_box = int(bbox.height * h)

                        # Apply boundaries
                        x = max(0, x)
                        y = max(0, y)
                        x2 = min(w, x + w_box)
                        y2 = min(h, y + h_box)

                        # Extract and save face
                        face_crop = frame[y:y2, x:x2]
                        
                        # Draw detection on frame
                        mp_drawing.draw_detection(frame, detection)

                        # Capture image at 1 second intervals
                        if time.time() - last_capture_time > 1 and face_crop.size > 0:
                            try:
                                cv2.imwrite(f"{folder_name}/{count}.jpg", face_crop)
                                winsound.Beep(1000, 150)
                                count += 1
                                last_capture_time = time.time()
                                self.status_label.configure(
                                    text=f"Captured {count}/{total_images} images", 
                                    text_color="#2e8b57"
                                )
                                self.update()
                            except Exception as e:
                                self.status_label.configure(
                                    text=f"Error saving image: {str(e)}",
                                    text_color="red"
                                )

                # Display frame in GUI
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(image=img)
                self.camera_preview.configure(image=img)
                self.camera_preview.image = img
                self.update()

                # Check for quit command
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Clean up
            cap.release()
            cv2.destroyAllWindows()
            self.stop_btn.configure(state="disabled")

            if count == total_images:
                self.status_label.configure(
                    text=f"{name} added successfully with {total_images} images. Generating encodings...",
                    text_color="#2e8b57"
                )
                self.update()
                self.generate_encodings()
            else:
                self.status_label.configure(
                    text=f"Capture stopped. {count} images saved for {name}",
                    text_color="orange"
                )

    def generate_encodings(self, dataset_path="dataset", encoding_file="encodings.pkl"):
        try:
            known_encodings = []
            known_names = []

            for student_folder in os.listdir(dataset_path):
                name = student_folder  # Use full "Name_Roll"
                folder_path = os.path.join(dataset_path, student_folder)
                for image_file in os.listdir(folder_path):
                    image_path = os.path.join(folder_path, image_file)
                    try:
                        image = face_recognition.load_image_file(image_path)
                        encodings = face_recognition.face_encodings(image)
                        if encodings:
                            known_encodings.append(encodings[0])
                            known_names.append(name)
                    except Exception as e:
                        print(f"Error processing {image_path}: {str(e)}")
                        continue

            with open(encoding_file, "wb") as f:
                pickle.dump({"encodings": known_encodings, "names": known_names}, f)

            self.status_label.configure(
                text="✅ Face encodings updated and saved to encodings.pkl", 
                text_color="#2e8b57"
            )
        except Exception as e:
            self.status_label.configure(
                text=f"Error generating encodings: {str(e)}",
                text_color="red"
            )
    
    def show_mark_attendance_frame(self):
        self.clear_main_frame()
        
        self.mark_attendance_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.mark_attendance_frame.grid(row=0, column=0, sticky="nsew")
        self.mark_attendance_frame.grid_columnconfigure(0, weight=1)
        self.mark_attendance_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self.mark_attendance_frame, text="Mark Attendance", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Camera frame
        self.camera_frame = ctk.CTkFrame(self.mark_attendance_frame, corner_radius=10)
        self.camera_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.camera_frame.grid_columnconfigure(0, weight=1)
        self.camera_frame.grid_rowconfigure(0, weight=1)
        
        # Camera label
        self.camera_label = ctk.CTkLabel(self.camera_frame, text="Camera will start when you click below")
        self.camera_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Start button
        start_btn = ctk.CTkButton(self.mark_attendance_frame, text="Start Face Recognition", 
                                  command=self.start_face_recognition,
                                  fg_color="#4169e1", hover_color="#6495ed")
        start_btn.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        # Status label
        self.recognition_status = ctk.CTkLabel(self.mark_attendance_frame, text="", text_color="#4169e1")
        self.recognition_status.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    
    def start_face_recognition(self):
        self.recognition_status.configure(text="Starting face recognition...", text_color="#4169e1")
        self.update()
        
        encodings_data = self.load_encodings()
        if not encodings_data:
            self.recognition_status.configure(text="❌ No encodings data available!", text_color="red")
            return
        
        cap = cv2.VideoCapture(0)
        self.recognition_status.configure(text="Looking for faces...", text_color="#4169e1")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # Apply histogram equalization for lighting normalization
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
            frame[:, :, 0] = cv2.equalizeHist(frame[:, :, 0])
            frame = cv2.cvtColor(frame, cv2.COLOR_YCrCb2BGR)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Display frame in GUI
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            self.camera_label.configure(image=img)
            self.camera_label.image = img
            
            # Process each face found
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                distances = face_recognition.face_distance(encodings_data["encodings"], face_encoding)
                best_match_idx = distances.argmin()
                
                if distances[best_match_idx] < 0.5:
                    name = encodings_data["names"][best_match_idx]
                    self.recognition_status.configure(text=f"✅ Face matched: {name}", text_color="#2e8b57")
                    
                    # Mark attendance
                    actual_name, roll_no = name.split("_")
                    self.mark_attendance(actual_name, roll_no)
                    winsound.Beep(1000, 150)
                    
                    cap.release()
                    return
                else:
                    self.recognition_status.configure(text="❌ Face not recognized. Please try again.", text_color="red")
            
            self.update()
            
            # Check for ESC key press
            if cv2.waitKey(1) == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def load_encodings(self, encoding_file="encodings.pkl"):
        if not os.path.exists(encoding_file):
            return None
        with open(encoding_file, "rb") as f:
            return pickle.load(f)
    
    def mark_attendance(self, name, roll_no):
        file = "attendance.csv"
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        status = "IN"

        file_exists = os.path.exists(file)

        if file_exists:
            with open(file, "r") as f:
                reader = list(csv.reader(f))
                student_logs = [row for row in reader if row and row[0] == str(roll_no) and row[1] == name]

                if student_logs:
                    last_status = student_logs[-1][-1]
                    if last_status == "IN":
                        status = "OUT"
                    else:
                        status = "IN"

        # Write header if file doesn't exist or is empty
        write_header = not file_exists or os.path.getsize(file) == 0

        with open(file, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Roll Number", "Name", "Date", "Time", "Status"])
            writer.writerow([roll_no, name, date_str, time_str, status])
        
        self.recognition_status.configure(text=f"Attendance marked: {name} ({status})", text_color="#2e8b57")
    
    def show_attendance_log_frame(self):
        self.clear_main_frame()
        
        self.attendance_log_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.attendance_log_frame.grid(row=0, column=0, sticky="nsew")
        self.attendance_log_frame.grid_columnconfigure(0, weight=1)
        self.attendance_log_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self.attendance_log_frame, text="Attendance Log", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(self.attendance_log_frame, corner_radius=10)
        scrollable_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Load attendance data
        self.load_attendance_data(scrollable_frame)
    
    def load_attendance_data(self, parent_frame):
        file = "attendance.csv"
        
        if not os.path.exists(file):
            no_data_label = ctk.CTkLabel(parent_frame, text="No attendance data available yet.")
            no_data_label.grid(row=0, column=0, padx=20, pady=20)
            return
        
        # Create a treeview widget
        style = ttk.Style()
        style.theme_use("default")
        
        # Configure style for Treeview
        style.configure("Treeview", 
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#2a2d2e",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        
        style.configure("Treeview.Heading", 
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading", 
                background=[('active', '#3484F0')])
        
        # Create Treeview widget
        tree = ttk.Treeview(parent_frame, columns=("Roll No", "Name", "Date", "Time", "Status"), show="headings")
        
        # Define headings
        tree.heading("Roll No", text="Roll No")
        tree.heading("Name", text="Name")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Status", text="Status")
        
        # Set column widths
        tree.column("Roll No", width=100, anchor="center")
        tree.column("Name", width=150, anchor="center")
        tree.column("Date", width=120, anchor="center")
        tree.column("Time", width=100, anchor="center")
        tree.column("Status", width=80, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Load data from CSV
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row:  # Skip empty rows
                    tree.insert("", "end", values=row)
        
        # Configure grid weights
        parent_frame.grid_rowconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = FaceRecognitionApp()
    app.mainloop()