import os
import sys
import argparse

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.game import FruitNinjaGame
from src.hand_tracker import HandTracker

def main():
    parser = argparse.ArgumentParser(description='Fruit Ninja Game by MediaPie')
    parser.add_argument('--use-camera', action='store_true', help='Use camera for hand tracking')
    parser.add_argument('--fullscreen', action='store_true', help='Run in fullscreen mode')
    
    args = parser.parse_args()
    
    # Initialize hand tracker if requested
    hand_tracker = None
    if args.use_camera:
        try:
            hand_tracker = HandTracker()
            print("Hand tracking enabled!")
        except Exception as e:
            print(f"Could not initialize hand tracking: {e}")
            print("Falling back to mouse control")
    
    # Start the game
    game = FruitNinjaGame(
        fullscreen=args.fullscreen,
        hand_tracker=hand_tracker
    )
    game.run()

if __name__ == "__main__":
    main()
