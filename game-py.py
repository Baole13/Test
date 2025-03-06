import pygame
import os
import sys
import time
import random

from src.fruit import FruitManager
from src.ui import UI, EffectManager

class FruitNinjaGame:
    """Main game class"""
    
    def __init__(self, fullscreen=False, hand_tracker=None):
        # Initialize pygame
        pygame.init()
        
        # Set up display
        self.fullscreen = fullscreen
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
        else:
            self.width, self.height = 800, 600
            self.screen = pygame.display.set_mode((self.width, self.height))
        
        pygame.display.set_caption('Fruit Ninja by MediaPie')
        
        # Load backgrounds
        self.backgrounds = {
            'summer': pygame.image.load(os.path.join('assets', 'backgrounds', 'summer.jpg')),
            