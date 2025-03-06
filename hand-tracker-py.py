import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import threading
import time

class HandTracker:
    """Tracks hand movements using webcam and controls the game cursor"""
    
    def __init__(self):
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cam_w, self.cam_h = 640, 480
        self.cap.set(3, self.cam_w)
        self.cap.set(4, self.cam_h)
        
        # Initialize hand detector
        self.detector = HandDetector(detectionCon=0.65, maxHands=1)
        
        # Screen dimensions (will be updated by the game)
        self.screen_w, self.screen_h = 800, 600
        
        # Current hand position
        self.cursor_pos = (0, 0)
        self.is_clicking = False
        
        # Start tracking in a separate thread
        self.running = True
        self.thread = threading.Thread(target=self._track_hands)
        self.thread.daemon = True
        self.thread.start()
        
    def _track_hands(self):
        """Track hands in a separate thread"""
        while self.running:
            success, img = self.cap.read()
            if not success:
                # If camera read fails, try again
                time.sleep(0.1)
                continue
                
            # Flip image for mirror effect
            img = cv2.flip(img, 1)
            
            # Find hands
            hands, img = self.detector.findHands(img)
            
            if hands:
                # Get position of index finger tip
                hand = hands[0]
                lmlist = hand['lmList']
                ind_x, ind_y = lmlist[8][0], lmlist[8][1]
                
                # Convert coordinates to screen space
                conv_x = int(np.interp(ind_x, (0, self.cam_w), (0, self.screen_w)))
                conv_y = int(np.interp(ind_y, (0, self.cam_h), (0, self.screen_h)))
                
                # Update cursor position
                self.cursor_pos = (conv_x, conv_y)
                
                # Check if thumb is up (for clicking)
                fingers = self.detector.fingersUp(hand)
                if fingers and len(fingers) >= 5:
                    self.is_clicking = fingers[4] == 1
                else:
                    self.is_clicking = False
            
            # Display window (debug mode)
            cv2.imshow("Hand Tracker", img)
            cv2.waitKey(1)
            
    def get_cursor_position(self):
        """Get the current cursor position"""
        return self.cursor_pos
        
    def is_cursor_down(self):
        """Check if the cursor is clicking"""
        return self.is_clicking
        
    def set_screen_dimensions(self, width, height):
        """Update screen dimensions for coordinate conversion"""
        self.screen_w = width
        self.screen_h = height
        
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.thread.is_alive():
            self.thread.join(1.0)  # Wait for thread to finish
        self.cap.release()
        cv2.destroyAllWindows()
