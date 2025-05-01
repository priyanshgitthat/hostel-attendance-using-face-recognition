#addFaces.py

import cv2
import os
import mediapipe as mp
import winsound
import time
from modelTraining import generate_encodings  # ✅ Import function

def addfaces(name, roll_no):
    folder_name = f"dataset/{name}_{roll_no}"
    os.makedirs(folder_name, exist_ok=True)

    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6)

    cap = cv2.VideoCapture(0)
    count = 0
    total_images = 10
    last_capture_time = time.time()

    while count < total_images:
        ret, frame = cap.read()
        if not ret:
            continue

        # Apply histogram equalization for lighting normalization
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        frame[:, :, 0] = cv2.equalizeHist(frame[:, :, 0])
        frame = cv2.cvtColor(frame, cv2.COLOR_YCrCb2BGR)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)

        key = cv2.waitKey(1)
        if key == ord('q'):
            print("Capture manually stopped by user.")
            break

        if results.detections:
            detection = results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            w_box = int(bbox.width * w)
            h_box = int(bbox.height * h)

            x = max(0, x)
            y = max(0, y)
            x2 = min(w, x + w_box)
            y2 = min(h, y + h_box)

            face_crop = frame[y:y2, x:x2]

            mp_drawing.draw_detection(frame, detection)

            if time.time() - last_capture_time > 1 and face_crop.size > 0:
                cv2.imwrite(f"{folder_name}/{count}.jpg", face_crop)
                winsound.Beep(1000, 150)
                print(f"Automatically saved face image {count + 1}/{total_images}")
                count += 1
                last_capture_time = time.time()

        cv2.imshow("Auto Face Capturing... (Press 'q' to quit)", frame)

    cap.release()
    cv2.destroyAllWindows()

    if count == total_images:
        print(f"{name} added successfully with {total_images} face images.")
        generate_encodings()  # ✅ Call from modelTraining.py
    else:
        print(f"{name} added with only {count} images.")


if __name__ == "__main__":
    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")
    addfaces(name, roll_no)