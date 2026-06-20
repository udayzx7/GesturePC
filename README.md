# 🖱️ GesturePC: AI-Powered Virtual Mouse

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**GesturePC** is an advanced, touchless computer control system that uses computer vision and hand tracking to replace traditional physical mouse inputs. By leveraging your webcam, this application tracks hand landmarks in real-time to perform cursor movements, clicks, scrolling, and even system screenshots entirely through intuitive hand gestures.

## ✨ Key Features

* **Real-Time Hand Tracking:** High-precision, low-latency tracking for up to two hands simultaneously.
* **Smooth Cursor Control:** Stabilized coordinate mapping for jitter-free cursor movement.
* **Dual-Hand & Single-Hand Modes:** Context-aware gesture recognition that automatically switches between single-hand operations and advanced dual-hand macros.
* **On-Screen HUD:** Live user interface displaying the active mode, gesture readiness, and visual feedback directly on the video feed.
* **Fully Offline:** Runs entirely locally on your machine without requiring an internet connection.

---

## 🖐️ Gesture Command Guide

### 👆 Single-Hand Operations
| Action | Hand Gesture |
| :--- | :--- |
| **Move Cursor** | Index Finger Up |
| **Left Click** | Pinch Thumb & Index Finger |
| **Right Click** | Pinch Thumb & Middle Finger |
| **Drag & Drop** | Thumb & Pinky pinched + Index Up |
| **Scroll Mode** | Hold Index & Middle Fingers Up (Move hand up/down) |
| **Screenshot** | Closed Fist (Holds for 3 seconds) |

### 👐 Dual-Hand Operations (Priority Mode)
| Action | Hand Gesture |
| :--- | :--- |
| **Fast Scroll Up** | Left Hand Open Palm |
| **Fast Scroll Down** | Right Hand Open Palm + Left Hand Index/Middle Up |

---

## 🛠️ Tech Stack & Libraries

* **[OpenCV (cv2)](https://opencv.org/):** Video capture, frame processing, and HUD rendering.
* **[cvzone & MediaPipe](https://github.com/cvzone/cvzone):** Machine learning pipeline for 21-point hand landmark detection.
* **[pynput](https://pypi.org/project/pynput/):** Programmatic control of the system mouse.
* **[Pillow (PIL)](https://python-pillow.org/):** Image capture for the screenshot functionality.

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You will need Python installed on your system along with a working webcam. It is highly recommended to use a virtual environment.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/udayzx7/GesturePC.git](https://github.com/udayzx7/GesturePC.git)
   cd GesturePC
Create and activate a virtual environment (Recommended):

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install the required dependencies:

Bash
pip install -r requirements.txt
Usage
Run the main Python script to launch the application:

Bash
python virtual_mouse_cvzone.py
Ensure you are in a well-lit environment for optimal hand tracking.

The application window will open. Perform the gestures listed in the guide above to control your PC.

To exit the application, press the ESC or q key on your physical keyboard.

💡 Future Scope
[ ] Add volume control via hand distance measurement.

[ ] Implement customizable gesture-to-macro mapping.

[ ] Improve background noise filtering for low-light environments.

👨‍💻 Author
Uday Garasiya * GitHub: @udayzx7

If you found this project interesting or helpful, consider giving it a ⭐!
