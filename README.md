# Virtual Keyboard using Hand Gestures (OpenCV + MediaPipe)


This project implements a virtual keyboard that can be controlled using hand gestures captured via a webcam.
Instead of pressing physical keys, you can move your hand and perform a pinch gesture (index + thumb) to press keys.
The keyboard appears on the screen, and detected inputs are simulated on your computer (you can type in Google, Notepad, etc.).

✨ Features

-> Virtual on-screen keyboard

-> Hand tracking using MediaPipe

-> Pinch gesture detection to press keys (avoids unwanted presses)

-> Keys are highlighted when selected

-> Works with any application (browser, text editor, etc.)

🛠️ Tech Stack

OpenCV – computer vision and drawing the keyboard

MediaPipe – hand landmark detection

PyAutoGUI – simulate key presses

NumPy – array operations

📦 **Installation**

Clone the repository:

1. **git clone https://github.com/your-username/virtual-keyboard-gesture.git**

2. **cd virtual-keyboard-gesture**

Environment Setup:

Install Python (3.9 or higher recommended)

Download Python and make sure python and pip are added to PATH.

Create a virtual environment:

3. **python -m venv venv**


4. Activate the virtual environment

On Windows:

**venv\Scripts\activate**


On Mac/Linux:

**source venv/bin/activate**


Upgrade pip (recommended)

5. **python -m pip install --upgrade pip**

Install dependencies:

6. **pip install -r requirements.txt**


▶️**How to Run**

Run the following command:

7. **python run_keyboard.py**


⌨️ **Usage**

-> Show your hand to the camera.

-> Move your index finger over the on-screen keyboard to select a key.

-> Perform a pinch gesture (thumb + index) to press the key.


-> Press q to quit the program.
