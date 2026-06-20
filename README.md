# GesturePC

> Control your computer using hand gestures.

GesturePC is an AI-powered virtual mouse that enables touchless computer interaction using real-time hand gesture recognition. Built with Python, OpenCV, and MediaPipe, it transforms a webcam into an intelligent input device capable of controlling cursor movement, clicks, scrolling, and screenshots.

---

## Features

* Smooth Cursor Movement
* Left Click Gesture
* Right Click Gesture
* Scrolling Support
* Pause/Lock Mode
* Screenshot Capture
* Real-Time Hand Tracking
* Webcam-Based Interaction

---

## Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* Pynput

---

## How It Works

1. The webcam captures hand movements.
2. MediaPipe detects and tracks hand landmarks.
3. Gesture recognition interprets finger positions.
4. Mouse actions are executed in real time.

---

## Project Structure

```text
GesturePC/
│
├── virtual_mouse_cvzone.py
├── README.md
├── requirements.txt
└── screenshots/
```

---

## Installation

```bash
git clone https://github.com/udayzx7/GesturePC.git
cd GesturePC
pip install -r requirements.txt
python virtual_mouse_cvzone.py
```

---

## Supported Gestures

| Gesture              | Action      |
| -------------------- | ----------- |
| Index Finger Up      | Move Cursor |
| Thumb + Index Finger | Left Click  |
| Two Finger Gesture   | Right Click |
| Finger Movement      | Scroll      |
| Fist                 | Pause       |
| Custom Gesture       | Screenshot  |

---

## Use Cases

* Touchless Computer Control
* Accessibility Applications
* Computer Vision Projects
* Human-Computer Interaction Research
* Smart Workstations

---

## Future Enhancements

* Voice Command Integration
* Custom Gesture Mapping
* Multi-Hand Support
* Gesture-Based Shortcuts
* Cross-Platform Optimization

---

## Author

**Uday Garasiya**

If you find this project useful, consider starring the repository.
