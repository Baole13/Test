import pygame
import random
import os
import math

class Fruit:
    """Base class for all game entities (fruits and bombs)"""
    
    def __init__(self, game, name, is_bomb=False):
        self.game = game
        self.name = name
        self.is_bomb = is_bomb
        
        # Load images
        img_path = os.path.join('assets', 'images', 'fruits', f'{name}.png')
        self.image = pygame.image.load(img_path)
        
        # Half fruit is the sliced version
        if is_bomb:
            half_img_path = os.path.join('assets', 'images', 'fruits', 'explosion.png')
        else:
            half_img_path = os.path.join('assets', 'images', 'fruits', f'half_{name}.png')
        self.half_image = pygame.image.load(half_img_path)
        
        # Initialize properties
        self.reset()
        
    def reset(self):
        """Reset fruit to its initial state"""
        # Position and velocity
        self.x = random.randint(100, self.game.width - 100)
        self.y = self.game.height + 50
        self.speed_x = random.randint(-10, 10)
        self.speed_y = random.randint(-80, -60)
        
        # State
        self.active = True
        self.hit = False
        self.time = 0
        
        # For smooth rotation
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.randint(-6, 6)
        
        # For trail effect
        self.positions = []
        
    def update(self):
        """Update fruit position and state"""
        if not self.active:
            return False
            
        # Physics
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += (1 * self.time)
        self.time += 1
        
        # Rotation
        self.rotation += self.rotation_speed
        
        # Store positions for trail effect (store only every 3 frames)
        if self.game.frame_count % 3 == 0:
            self.positions.append((self.x, self.y))
            if len(self.positions) > 5:  # Keep only last 5 positions
                self.positions.pop(0)
        
        # Check if fruit has gone off-screen
        if self.y > self.game.height + 100:
            self.active = False
            return False
            
        return True
        
    def draw(self, surface):
        """Draw the fruit on the screen"""
        if not self.active:
            return
            
        # Draw trail effect
        if self.game.settings['show_trails'] and not self.hit:
            for i, pos in enumerate(self.positions):
                alpha = 100 - i * 20  # Fade out older positions
                size_reduction = i * 5  # Make older positions smaller
                
                # Create a surface with per-pixel alpha
                trail_img = self.image.copy()
                trail_img.set_alpha(alpha)
                trail_img = pygame.transform.scale(
                    trail_img, 
                    (self.image.get_width() - size_reduction, 
                     self.image.get_height() - size_reduction)
                )
                trail_rect = trail_img.get_rect(center=(pos[0], pos[1]))
                surface.blit(trail_img, trail_rect)
        
        # Draw the fruit
        img = self.half_image if self.hit else self.image
        # Rotate image
        rotated_img = pygame.transform.rotate(img, self.rotation)
        img_rect = rotated_img.get_rect(center=(self.x, self.y))
        surface.blit(rotated_img, img_rect)
        
    def check_collision(self, pos):
        """Check if the given position collides with this fruit"""
        if not self.active or self.hit:
            return False
            
        # Simple circle collision
        distance = math.sqrt((pos[0] - self.x)**2 + (pos[1] - self.y)**2)
        return distance < 40  # Collision radius
        
    def slice(self):
        """Slice the fruit"""
        if not self.active or self.hit:
            return False
            
        self.hit = True
        
        # Change physics for sliced fruit
        self.speed_x += random.randint(-5, 5)
        self.speed_y -= 5
        
        return True
        
class FruitManager:
    """Manages all fruits in the game"""
    
    def __init__(self, game):
        self.game = game
        self.fruits = []
        self.fruit_types = ['melon', 'orange', 'pomegranate', 'guava']
        self.spawn_timer = 0
        self.combo_counter = 0
        self.combo_timer = 0
        
    def update(self):
        """Update all fruits and spawn new ones"""
        # Update spawn timer
        self.spawn_timer -= 1
        
        # Spawn new fruits if timer expired
        if self.spawn_timer <= 0:
            self._spawn_fruits()
            
        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_counter = 0
            
        # Update all active fruits
        for fruit in self.fruits[:]:
            if not fruit.update():
                self.fruits.remove(fruit)
                
    def draw(self, surface):
        """Draw all fruits"""
        for fruit in self.fruits:
            fruit.draw(surface)
            
        # Draw combo counter if active
        if self.combo_counter > 1 and self.combo_timer > 0:
            font = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 36)
            combo_text = font.render(f'Combo x{self.combo_counter}!', True, (255, 255, 255))
            text_rect = combo_text.get_rect(center=(self.game.width // 2, 100))
            # Draw shadow
            shadow_text = font.render(f'Combo x{self.combo_counter}!', True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(self.game.width // 2 + 2, 102))
            surface.blit(shadow_text, shadow_rect)
            surface.blit(combo_text, text_rect)
            
    def check_collisions(self, pos):
        """Check collisions with all fruits"""
        hit_fruit = False
        hit_bomb = False
        
        for fruit in self.fruits:
            if fruit.check_collision(pos):
                if fruit.slice():
                    if fruit.is_bomb:
                        hit_bomb = True
                        # Create explosion effect
                        self.game.effects.add_effect('explosion', fruit.x, fruit.y)
                    else:
                        hit_fruit = True
                        # Create slice effect
                        self.game.effects.add_effect('slice', pos[0], pos[1])
                        # Add score
                        self.game.score += 1 + self.combo_counter // 2
                        # Update combo
                        self.combo_counter += 1
                        self.combo_timer = 60  # 1 second at 60 FPS
                        
        return hit_fruit, hit_bomb
        
    def _spawn_fruits(self):
        """Spawn a random number of fruits"""
        difficulty = self.game.difficulty
        
        # Determine how many fruits to spawn
        base_count = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }[difficulty]
        
        count = base_count + random.randint(0, 1)
        
        # Spawn fruits
        for _ in range(count):
            fruit_type = random.choice(self.fruit_types)
            self.fruits.append(Fruit(self.game, fruit_type))
            
        # Maybe spawn a bomb
        bomb_chance = {
            'easy': 0.1,
            'medium': 0.2,
            'hard': 0.3
        }[difficulty]
        
        if random.random() < bomb_chance:
            self.fruits.append(Fruit(self.game, 'bomb', is_bomb=True))
            
        # Reset spawn timer
        base_timer = {
            'easy': 90,
            'medium': 60,
            'hard': 45
        }[difficulty]
        
        self.spawn_timer = base_timer + random.randint(-10, 10)
