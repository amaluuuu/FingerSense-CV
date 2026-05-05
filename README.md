# Finger Sense 🖐️

A real-time hand tracking, finger counting, and gesture recognition application built with Python, OpenCV, and MediaPipe (via cvzone).

## Features
- **Real-Time Finger Counting**: Tracks up to 2 hands and counts total raised fingers.
- **Gesture Recognition**: Identifies common gestures like Peace ✌️, Thumbs Up 👍, Fist ✊, and more.
- **Modern UI**: Clean HUD with semi-transparent backgrounds for better text readability.
- **FPS Counter**: Tracks camera and processing performance.
- **Interactive Controls**:
  - `q` : Quit the application
  - `d` : Toggle the drawing of the hand skeleton/landmarks
  - `s` : Save a screenshot of the current frame to a `screenshots/` folder.

## Installation

1. Clone this repository (or download the files).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from your terminal:
```bash
python "Finger Counting.py"
```

### Advanced Options
You can configure the application using command-line arguments:
```bash
python "Finger Counting.py" --camera 0 --confidence 0.8 --max_hands 2
```
- `--camera`: The index of the webcam to use (default: 0).
- `--confidence`: The minimum confidence threshold for hand detection (default: 0.8).
- `--max_hands`: Maximum number of hands to detect (default: 2).

## Technologies Used
- [OpenCV](https://opencv.org/): For real-time computer vision and image processing.
- [cvzone](https://github.com/cvzone/cvzone): A computer vision package that makes it easy to run image processing and AI functions.
- [MediaPipe](https://google.github.io/mediapipe/): Developed by Google for fast, cross-platform ML solutions (under the hood of cvzone).

## License
MIT License
