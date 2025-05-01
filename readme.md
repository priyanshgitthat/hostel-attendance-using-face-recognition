# Face Recognition Attendance System 🎓📸

A modern desktop GUI application that uses **Face Recognition** to mark attendance automatically. This app is developed in **Python** using **CustomTkinter**, **OpenCV**, and **face_recognition** library.

---

## 🚀 Features

- 📷 Live face detection and recognition using webcam  
- 📝 Auto attendance marking with date and time  
- ➕ Add new students and capture their face data  
- 💾 Attendance logs saved in CSV format  
- 🌗 Light/Dark mode with a clean sidebar UI (CustomTkinter)

---

## 🖥️ Tech Stack & Libraries

- **Python 3.x**
- `customtkinter`
- `opencv-python`
- `face_recognition`
- `mediapipe`
- `Pillow`
- `numpy`

---

## 📂 Folder Structure
```
FaceRecognitionAttendanceSystem/
├── dataset/                          # Captured face images for each student
│   ├── John_101/
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   └── ...
│   └── ...
├── encodings.pkl                     # Pickle file storing face encodings
├── attendance.csv                    # Attendance record in CSV format
├── FRAS-GUI-Version.py              # Main Python GUI application
├── requirements.txt                  # List of all required Python libraries
├── dlib-19.22.99-cp310-cp310-win_amd64.whl  # Precompiled dlib binary for Windows
├── README.md                         # Project readme file

```


---

## 🛠️ Installation & Setup Instructions

### step 1 : unzip the file 
### step 2 : delete the previous python virtual enviroment
### step 3 : and create a new python virtual enviroment using following command
```bash
python -m venv env
```
### step 2 : installed the required libraries using requirement.txt
```bash
pip install requirement.txt
```


#### ⚠️ Note: face_recognition requires dlib, which needs CMake and Visual C++ Build Tools on Windows. If installation fails, try using precompiled binaries or follow a guide online.

##### if dlib installation causing issue , in that case i also provided the binary file of dlib just direct install that file using pip install command

```
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
```

### after successfull installtion of the libraries, run FRAS-GUI-Version.py 


## How to use the app (User Guide)
### 1. click on add student button from the left sidebar
![alt text](image.png)

### 2. type your name and roll number
![alt text](<Project Screen Shots/03 add faces.png>)

### 3. press capture faces
![alt text](<Project Screen Shots/04 capturing faces.png>)

#### It will take some time to capture 10 images and generate encodings.pkl.
#### Wait until you see: "FACE encoding successfully updated"

### 4. click on mark attendance button and than press face recognition
![alt text](<Project Screen Shots/05 face recognition.png>)
 #### 📸 Keep your face straight, ensure good lighting, and smile!

### 5. attendance mark messaged appear on the bottom with current status IN or OUT
![alt text](<Project Screen Shots/06 marking attendance.png>)


### 6. click on view attendance button to see all the entries in csv table
![alt text](<Project Screen Shots/07 view attendance data.png>)


### if you face any trouble while using the app or you have any suggestion or feedback feel free to contact me 


Priyansh Verma
MCA Student, CSJMU
[email](mailto:priyanshverma157@gmail.com )
[github](https://github.com/priyanshgitthat)
[linkedin](https://www.linkedin.com/in/priyanshv/)
[portfolio](https://priyanshverma.netlify.app/)
📄 License

This project is open-source and free to use under the MIT License.