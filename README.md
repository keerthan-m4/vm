# Virtual Mouse Using Hand Gestures and Blink Detection

A Python-based virtual mouse that allows users to control the computer cursor using hand gestures and perform mouse clicks using eye blinks.

## Features

* 🖱️ Control the mouse cursor using the index finger.
* 👁️ Perform a mouse click using a double blink.
* ✋ Detect a middle-finger gesture to close the application.
* 🎥 Real-time hand and face tracking using the webcam.
* 🎯 Cursor movement smoothing for better control.

## Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy

## How It Works

The webcam captures the user's hand and face movements in real time.

* The **index finger** controls the position of the mouse cursor.
* A **double blink** triggers a mouse click.
* Extending the **middle finger** while the other fingers are folded closes the application.
* MediaPipe is used for hand and facial landmark detection.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/virtual-mouse.git
cd virtual-mouse
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Run the Program

```bash
python virtual_mouse.py
```

Make sure your webcam is connected and Python has permission to access it.

## Controls

| Gesture          | Action            |
| ---------------- | ----------------- |
| ☝️ Index finger  | Move mouse cursor |
| 😉 Double blink  | Mouse click       |
| 🖕 Middle finger | Close application |
| `ESC`            | Exit application  |

## Requirements

* Python 3.x
* Working webcam
* Windows/Linux/macOS
* Required Python libraries listed in `requirements.txt`

## Future Improvements

* Left and right click gesture support
* Scroll control using hand gestures
* Drag-and-drop gestures
* Improved blink detection
* Customizable gestures
* Better cursor calibration

## Author

Developed as a Python computer-vision project.
