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

git clone https://github.com/your-username/virtual-keyboard-gesture.git
cd virtual-keyboard-gesture


Install dependencies:

pip install opencv-python mediapipe pyautogui numpy


▶️**How to Run**

Run the following command:

python run_keyboard.py


⌨️ **Usage**

-> Show your hand to the camera.

-> Move your index finger over the on-screen keyboard to select a key.

-> Perform a pinch gesture (thumb + index) to press the key.

-> Press q to quit the program.