# Volume Control using Hand Gestures

## Overview

This project allows users to control the system volume using **hand gestures** in real-time.

It uses computer vision techniques to detect hand landmarks and calculate the distance between fingers to adjust the volume.

---

## How it Works

1️- Capture video from webcam
2️- Detect hand using **MediaPipe**
3️- Extract hand landmarks
4️- Measure distance between thumb and index finger
5️- Map distance to system volume range
6️- Adjust volume dynamically

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* Pycaw (for volume control)

---

## How to Run

### Clone the repository

```bash id="u3w0o7"
git clone https://github.com/engasmaaibrahim/Volume-Hand-Control.git
cd Volume-Hand-Control
```

---

### Create and activate virtual environment

#### On Windows:

```bash id="g1hx6d"
python -m venv env
env\Scripts\activate
```

---

### Install dependencies

```bash id="cs1a53"
pip install -r requirements.txt
```

---

### Run the project

```bash id="67j6ru"
python main.py
```

---

## How it Controls Volume

* Short distance → Low volume 🔉
* Long distance → High volume 🔊

---


## Author

**Asmaa Ibrahim**
AI & Machine Learning Engineer
