import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
from typing import List, Tuple, Optional

class VirtualKeyboard:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Keyboard layout
        self.keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]
        
        # Special keys
        self.special_keys = ['SPACE', 'BACKSPACE', 'ENTER']
        
        # Key dimensions and positions
        self.key_width = 60
        self.key_height = 60
        self.key_margin = 10
        self.keyboard_start_x = 50
        self.keyboard_start_y = 100
        
        # Gesture detection variables
        self.prev_time = 0
        self.tap_threshold = 0.02  # Distance threshold for tap detection
        self.tap_cooldown = 0.5    # Cooldown between taps
        self.last_tap_time = 0
        self.prev_index_tip = None
        
        # UI state
        self.hovered_key = None
        self.pressed_key = None
        self.press_animation_time = 0
        
        # Text display
        self.typed_text = ""
        self.max_text_length = 50
        
    def get_key_rect(self, row: int, col: int) -> Tuple[int, int, int, int]:
        """Get the rectangle coordinates for a key"""
        # Calculate offset for centering rows
        row_offset = 0
        if row == 1:  # Second row (ASDF...)
            row_offset = self.key_width // 4
        elif row == 2:  # Third row (ZXCV...)
            row_offset = self.key_width // 2
            
        x = self.keyboard_start_x + col * (self.key_width + self.key_margin) + row_offset
        y = self.keyboard_start_y + row * (self.key_height + self.key_margin)
        
        return x, y, x + self.key_width, y + self.key_height
    
    def get_special_key_rect(self, key_index: int) -> Tuple[int, int, int, int]:
        """Get rectangle coordinates for special keys"""
        special_key_y = self.keyboard_start_y + 3 * (self.key_height + self.key_margin)
        
        if key_index == 0:  # SPACE
            x = self.keyboard_start_x + 2 * (self.key_width + self.key_margin)
            width = 4 * self.key_width + 3 * self.key_margin
            return x, special_key_y, x + width, special_key_y + self.key_height
        elif key_index == 1:  # BACKSPACE
            x = self.keyboard_start_x + 7 * (self.key_width + self.key_margin)
            return x, special_key_y, x + self.key_width * 2, special_key_y + self.key_height
        elif key_index == 2:  # ENTER
            x = self.keyboard_start_x + 10 * (self.key_width + self.key_margin)
            return x, special_key_y, x + self.key_width, special_key_y + self.key_height
    
    def draw_keyboard(self, img: np.ndarray):
        """Draw the virtual keyboard on the image"""
        # Draw regular keys
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                x1, y1, x2, y2 = self.get_key_rect(row_idx, col_idx)
                
                # Determine key color
                color = (200, 200, 200)  # Default gray
                text_color = (0, 0, 0)   # Black text
                
                if self.hovered_key == key:
                    color = (150, 150, 255)  # Light blue for hover
                
                if self.pressed_key == key and time.time() - self.press_animation_time < 0.2:
                    color = (100, 100, 255)  # Darker blue for press
                    text_color = (255, 255, 255)  # White text
                
                # Draw key background
                cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
                
                # Draw key text
                text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                text_x = x1 + (self.key_width - text_size[0]) // 2
                text_y = y1 + (self.key_height + text_size[1]) // 2
                cv2.putText(img, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)
        
        # Draw special keys
        for i, special_key in enumerate(self.special_keys):
            x1, y1, x2, y2 = self.get_special_key_rect(i)
            
            # Determine key color
            color = (180, 180, 180)  # Slightly darker gray for special keys
            text_color = (0, 0, 0)
            
            if self.hovered_key == special_key:
                color = (150, 150, 255)
            
            if self.pressed_key == special_key and time.time() - self.press_animation_time < 0.2:
                color = (100, 100, 255)
                text_color = (255, 255, 255)
            
            # Draw key background
            cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
            
            # Draw key text (smaller font for special keys)
            font_scale = 0.6 if special_key != 'SPACE' else 0.8
            text_size = cv2.getTextSize(special_key, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
            text_x = x1 + ((x2 - x1) - text_size[0]) // 2
            text_y = y1 + ((y2 - y1) + text_size[1]) // 2
            cv2.putText(img, special_key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, 2)
    
    def draw_text_display(self, img: np.ndarray):
        """Draw the typed text display area"""
        # Text display background
        cv2.rectangle(img, (50, 20), (750, 70), (240, 240, 240), -1)
        cv2.rectangle(img, (50, 20), (750, 70), (0, 0, 0), 2)
        
        # Display typed text
        display_text = self.typed_text[-self.max_text_length:] if len(self.typed_text) > self.max_text_length else self.typed_text
        cv2.putText(img, display_text, (60, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # Cursor
        cursor_x = 60 + cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0][0]
        if int(time.time() * 2) % 2:  # Blinking cursor
            cv2.line(img, (cursor_x + 5, 30), (cursor_x + 5, 60), (0, 0, 0), 2)
    
    def get_key_at_position(self, x: int, y: int) -> Optional[str]:
        """Get the key at the given position"""
        # Check regular keys
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                x1, y1, x2, y2 = self.get_key_rect(row_idx, col_idx)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return key
        
        # Check special keys
        for i, special_key in enumerate(self.special_keys):
            x1, y1, x2, y2 = self.get_special_key_rect(i)
            if x1 <= x <= x2 and y1 <= y <= y2:
                return special_key
        
        return None
    
    def detect_tap_gesture(self, landmarks) -> bool:
        """Detect tap gesture using finger movement"""
        if landmarks is None:
            return False
        
        # Get index finger tip (landmark 8)
        index_tip = landmarks[8]
        
        if self.prev_index_tip is not None:
            # Calculate movement distance
            distance = np.sqrt(
                (index_tip.x - self.prev_index_tip.x) ** 2 +
                (index_tip.y - self.prev_index_tip.y) ** 2 +
                (index_tip.z - self.prev_index_tip.z) ** 2
            )
            
            # Check for tap (quick downward then upward movement)
            current_time = time.time()
            if (distance > self.tap_threshold and 
                current_time - self.last_tap_time > self.tap_cooldown):
                self.last_tap_time = current_time
                self.prev_index_tip = index_tip
                return True
        
        self.prev_index_tip = index_tip
        return False
    
    def process_key_press(self, key: str):
        """Process the key press and simulate keyboard input"""
        if key == 'SPACE':
            self.typed_text += ' '
            pyautogui.press('space')
        elif key == 'BACKSPACE':
            if self.typed_text:
                self.typed_text = self.typed_text[:-1]
            pyautogui.press('backspace')
        elif key == 'ENTER':
            self.typed_text += '\n'
            pyautogui.press('enter')
        else:
            self.typed_text += key.lower()
            pyautogui.press(key.lower())
        
        # Set press animation
        self.pressed_key = key
        self.press_animation_time = time.time()
    
    def run(self):
        """Main application loop"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        
        print("Virtual Keyboard with Hand Gesture Control")
        print("Instructions:")
        print("- Hold your hand in front of the camera")
        print("- Move your index finger over keys to hover")
        print("- Make a quick tap gesture to press a key")
        print("- Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            # Reset hover state
            self.hovered_key = None
            
            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Get index finger tip position
                    index_tip = hand_landmarks.landmark[8]
                    finger_x = int(index_tip.x * w)
                    finger_y = int(index_tip.y * h)
                    
                    # Draw finger tip
                    cv2.circle(frame, (finger_x, finger_y), 10, (0, 255, 0), -1)
                    
                    # Check which key is being hovered
                    hovered_key = self.get_key_at_position(finger_x, finger_y)
                    if hovered_key:
                        self.hovered_key = hovered_key

                        # PINCH DETECTION instead of tap
                        thumb_tip = hand_landmarks.landmark[4]
                        pinch_distance = np.sqrt(
                            (index_tip.x - thumb_tip.x) ** 2 +
                            (index_tip.y - thumb_tip.y) ** 2 +
                            (index_tip.z - thumb_tip.z) ** 2
                        )

                        if pinch_distance < 0.04 and time.time() - self.last_tap_time > self.tap_cooldown:
                            self.last_tap_time = time.time()
                            self.process_key_press(hovered_key)
                            print(f"Pinch detected → Key pressed: {hovered_key}")

            
            # Draw UI elements
            self.draw_keyboard(frame)
            self.draw_text_display(frame)
            
            # Draw instructions
            cv2.putText(frame, "Move finger over keys, tap to press", (50, h - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.putText(frame, "Press 'q' to quit", (50, h - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            # Show FPS
            current_time = time.time()
            fps = 1 / (current_time - self.prev_time) if self.prev_time != 0 else 0
            self.prev_time = current_time
            cv2.putText(frame, f"FPS: {int(fps)}", (w - 100, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            # Display the frame
            cv2.imshow('Virtual Keyboard - Hand Gesture Control', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    keyboard = VirtualKeyboard()
    keyboard.run()
