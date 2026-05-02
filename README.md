# ProfBlocker 🛡️

A lightweight, real-time facial recognition desktop application built with Python. ProfBlocker continuously monitors the webcam feed to verify user identity, actively protecting your workspace from unauthorized access.

## ⚡ Key Features

* **Real-Time Continuous Monitoring:** Instantly identifies authorized users and flags unknown faces.
* **Highly Optimized Pipeline:** Uses frame-skipping algorithms and resolution downscaling to maintain smooth video playback with minimal CPU overhead.
* **Dynamic UI Scaling:** Built with `customtkinter`, the video feed dynamically scales to any window size while strictly preserving the camera's native 16:9 aspect ratio (no stretching or cropping).
* **Local Biometric Database:** Securely stores facial embeddings using SQLite3. Easily add or manage users directly from the UI.
* **Active Protection Modules:** Toggleable security actions triggered by face detection states.

## 🛠 Tech Stack

* **Language:** Python 3
* **Computer Vision:** OpenCV (`cv2`)
* **Machine Learning / Detection:** `face_recognition` (dlib)
* **GUI Framework:** `customtkinter` + standard `tkinter`
* **Database:** SQLite3

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone [https://github.com/wojzmuda/ProfBlocker.git](https://github.com/wojzmuda/ProfBlocker.git)
cd ProfBlocker
```

### 2. Install dependencies
*(Note: `face_recognition` requires a C++ compiler and CMake installed on your system to build `dlib`. Since this project uses `uv`, you can install dependencies quickly using it, or fallback to standard pip)*
```bash
pip install opencv-python face_recognition customtkinter Pillow numpy
```

### 3. Run the application
```bash
python main.py
```

## 📂 Project Structure
```text
ProfBlocker/
├── core/
│   ├── __init__.py
│   ├── actions.py
│   ├── camera.py
│   ├── databasemanager.py
│   ├── facerecognizer.py
│   ├── gui.py
│   └── test.py
├── faces/
│   ├── test_unit.jpg
│   └── user.jpg
├── tests/
├── .gitignore
├── .python-version
├── conftest.py
├── LICENSE
├── main.py
├── pyproject.toml
├── README.md
├── struktura.txt
├── users_info.db
└── uv.lock
```