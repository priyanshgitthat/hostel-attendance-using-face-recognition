# modelTraining.py

import os
import face_recognition
import pickle


def generate_encodings(dataset_path="dataset", encoding_file="encodings.pkl"):
    known_encodings = []
    known_names = []

    for student_folder in os.listdir(dataset_path):
        name = student_folder  # ✅ Use full "Name_Roll"
        folder_path = os.path.join(dataset_path, student_folder)
        for image_file in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(name)  # ✅ Save full name

    with open(encoding_file, "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)

    print("✅ Face encodings updated and saved to encodings.pkl")
