#faceRecognizer.py

import face_recognition
import cv2
import pickle
import os

def load_encodings(encoding_file="encodings.pkl"):
    if not os.path.exists(encoding_file):
        print("❌ Encoding file not found!")
        return None
    with open(encoding_file, "rb") as f:
        return pickle.load(f)

def recognize_faces_from_webcam(encodings_data, tolerance=0.5):
    if not encodings_data:
        return
    
    known_encodings = encodings_data["encodings"]
    known_names = encodings_data["names"]

    cap = cv2.VideoCapture(0)

    print("🎥 Starting real-time face recognition... (Press ESC to exit)")

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

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
            name = "Not Matched"

            distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_idx = distances.argmin()
            if distances[best_match_idx] < tolerance:
                name = f"Matched: {known_names[best_match_idx]}"
            else:
                name = "Not Matched"

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0) if "Matched" in name else (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    encodings_data = load_encodings()
    recognize_faces_from_webcam(encodings_data)