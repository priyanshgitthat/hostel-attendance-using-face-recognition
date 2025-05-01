#test.py

import cv2
import face_recognition
from attendance import mark_attendance
from faceRecognizer import load_encodings
import winsound

def recognize_face_and_mark_attendance():
    encodings_data = load_encodings()  # Load the face encodings
    if encodings_data:
        print("🎥 Starting real-time face recognition... (Press ESC to exit)")
        cap = cv2.VideoCapture(0)
        
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

            recognized = False  # To check if a face is recognized

            # Process each face found
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(encodings_data["encodings"], face_encoding)
                name = "Not Matched"

                distances = face_recognition.face_distance(encodings_data["encodings"], face_encoding)
                best_match_idx = distances.argmin()
                if distances[best_match_idx] < 0.5:
                    name = encodings_data["names"][best_match_idx]
                    print(f"✅ Face matched: {name}")

                    # Once face is matched, mark attendance
                    #roll_no = 28  # Example roll number, you can modify this
                    actual_name, roll_no = name.split("_")
                    roll_no = int(roll_no)  # convert string to int if needed
                    # mark_attendance(name, roll_no)
                    mark_attendance(actual_name, roll_no)
                    winsound.Beep(1000, 150)  # Play a beep sound to indicate success

                    cap.release()  # Close the camera once attendance is marked
                    cv2.destroyAllWindows()  # Close all windows after marking attendance
                    return  # Exit the function

                # If face is not recognized, display the message near the face
                else:
                    recognized = False
                    # Display the message near the detected face
                    cv2.putText(frame, "❌ Face not recognized. Please try again.", 
                                (left, top - 10),  # Position the text above the face
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

            # Show the frame (camera window)
            cv2.imshow("Face Recognition", frame)

            # Exit the loop if ESC is pressed
            if cv2.waitKey(1) == 27:  # ESC key to exit
                break

        # Release the camera and close windows
        cap.release()
        cv2.destroyAllWindows()

    else:
        print("❌ No encodings data available!")

if __name__ == "__main__":
    recognize_face_and_mark_attendance()
