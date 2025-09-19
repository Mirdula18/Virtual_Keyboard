import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional

class GestureDetector:
    """Advanced gesture detection for virtual keyboard"""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7
        )
        
        # Gesture detection parameters
        self.tap_history = []
        self.max_history = 10
        self.tap_threshold = 0.03
        self.velocity_threshold = 0.1
        
    def get_finger_positions(self, landmarks) -> dict:
        """Extract key finger positions from hand landmarks"""
        if not landmarks:
            return {}
        
        positions = {
            'thumb_tip': landmarks[4],
            'index_tip': landmarks[8],
            'index_pip': landmarks[6],
            'middle_tip': landmarks[12],
            'ring_tip': landmarks[16],
            'pinky_tip': landmarks[20]
        }
        
        return positions
    
    def calculate_finger_distance(self, point1, point2) -> float:
        """Calculate 3D distance between two finger points"""
        return np.sqrt(
            (point1.x - point2.x) ** 2 +
            (point1.y - point2.y) ** 2 +
            (point1.z - point2.z) ** 2
        )
    
    def detect_pinch_gesture(self, landmarks) -> bool:
        """Detect pinch gesture (thumb and index finger close together)"""
        positions = self.get_finger_positions(landmarks)
        
        if 'thumb_tip' not in positions or 'index_tip' not in positions:
            return False
        
        distance = self.calculate_finger_distance(
            positions['thumb_tip'], 
            positions['index_tip']
        )
        
        return distance < 0.05  # Threshold for pinch
    
    def detect_tap_gesture(self, landmarks) -> bool:
        """Detect tap gesture using finger velocity and position history"""
        if not landmarks:
            return False
        
        index_tip = landmarks[8]
        current_pos = np.array([index_tip.x, index_tip.y, index_tip.z])
        
        # Add to history
        self.tap_history.append(current_pos)
        if len(self.tap_history) > self.max_history:
            self.tap_history.pop(0)
        
        # Need at least 5 frames for velocity calculation
        if len(self.tap_history) < 5:
            return False
        
        # Calculate velocity (change in z-position indicates tap)
        recent_positions = self.tap_history[-5:]
        z_velocities = []
        
        for i in range(1, len(recent_positions)):
            z_vel = recent_positions[i][2] - recent_positions[i-1][2]
            z_velocities.append(z_vel)
        
        # Look for quick forward then backward movement (tap pattern)
        if len(z_velocities) >= 3:
            # Check for forward movement followed by backward movement
            forward_movement = any(vel > self.velocity_threshold for vel in z_velocities[:2])
            backward_movement = any(vel < -self.velocity_threshold for vel in z_velocities[1:])
            
            return forward_movement and backward_movement
        
        return False
    
    def detect_swipe_gesture(self, landmarks) -> Optional[str]:
        """Detect swipe gestures (left, right, up, down)"""
        if len(self.tap_history) < 8:
            return None
        
        # Get start and end positions
        start_pos = self.tap_history[0]
        end_pos = self.tap_history[-1]
        
        # Calculate movement vector
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Minimum movement threshold
        min_movement = 0.1
        
        if abs(dx) > min_movement or abs(dy) > min_movement:
            # Determine primary direction
            if abs(dx) > abs(dy):
                return 'right' if dx > 0 else 'left'
            else:
                return 'down' if dy > 0 else 'up'
        
        return None
    
    def is_hand_open(self, landmarks) -> bool:
        """Check if hand is open (all fingers extended)"""
        positions = self.get_finger_positions(landmarks)
        
        # Check if fingertips are above their respective PIP joints
        fingers_extended = 0
        
        # Index finger
        if positions['index_tip'].y < positions['index_pip'].y:
            fingers_extended += 1
        
        # Add similar checks for other fingers...
        # (Simplified version - you can expand this)
        
        return fingers_extended >= 3  # At least 3 fingers extended
