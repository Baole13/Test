import pygame
import os
import random

class UI:
    """Handles all UI elements like menus, buttons, and HUD"""
    
    def __init__(self, game):
        self.game = game
        self.buttons = {}
        self.professor_image = pygame.image.load(os.path.join('assets', 'images', 'characters', 'professor.png'))
        self.professor_rect = self.professor_image.get_rect(topleft=(20, self.game.height // 2))
        
        # Load icons
        self.life_icon = pygame.image.load(os.path.join('assets', 'images', 'lives', 'white_lives.png'))
        self.lost_life_icon = pygame.image.load(os.path.join('assets', 'images', 'lives', 'red_lives.png'))
        
        # Fruit facts from the original code
        self.fruit_facts = [
            "Did you know that bananas are berries?",
            "Grapes can be used to make wine.",
            "Melons are an excellent choice for staying hydrated.",
            "Guavas are sometimes called 'the poor man's apple'.",
            "Each pomegranate can contain hundreds of juicy seeds, known as arils.",
            "Oranges are a good source of vitamin C.",
            "Cranberries can bounce!",
            "Orange trees can live for up to 100 years and continue to produce fruit throughout their long lives.",
            "Guavas are often referred to as superfruits because of their high nutritional value.",
            "Pomegranates are known as 'nature's candy' due to their sweet and tart flavor.",
            "Some oranges can be fully ripe while still green in color.",
            "The world's heaviest melon on record weighed over 350 pounds!"
        ]
        
        # Track displayed facts
        self.facts_displayed = []
        
    def create_button(self, id, text, x, y, width, height, color, hover_color, text_color, font_size=20):
        """Create a button with the given parameters"""
        self.buttons[id] = {
            'rect': pygame.Rect(x, y, width, height),
            'text': text,
            'color': color,
            'hover_color': hover_color,
            'text_color': text_color,
            'font_size': font_size
        }
        
    def draw_button(self, surface, button_id):
        """Draw a button on the screen"""
        if button_id not in self.buttons:
            return
            
        button = self.buttons[button_id]
        rect = button['rect']
        color = button['color']
        
        # Check if mouse is hovering over button
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            color = button['hover_color']
            
        # Draw button
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)  # Border
        
        # Draw text
        font = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), button['font_size'])
        text = font.render(button['text'], True, button['text_color'])
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
        
    def check_button_click(self, button_id, pos):
        """Check if the given position is on a button"""
        if button_id not in self.buttons:
            return False
            
        return self.buttons[button_id]['rect'].collidepoint(pos)
        
    def draw_lives(self, surface, lives):
        """Draw the player lives icons"""
        for i in range(3):
            img = self.life_icon if i < lives else self.lost_life_icon
            img_rect = img.get_rect(topleft=(self.game.width - 110 + i * 35, 10))
            surface.blit(img, img_rect)
            
    def draw_score(self, surface, score):
        """Draw the score on the screen"""
        font = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 42)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
        
    def draw_timer(self, surface, time_left):
        """Draw the timer on the screen"""
        font = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 27)
        timer_text = font.render(f'Time: {time_left}', True, (255, 255, 255))
        surface.blit(timer_text, (10, 60))
        
    def draw_difficulty(self, surface, difficulty):
        """Draw the current difficulty level"""
        font = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 16)
        difficulty_text = font.render(f'Difficulty: {difficulty.capitalize()}', True, (255, 255, 255))
        text_rect = difficulty_text.get_rect(bottomright=(self.game.width - 10, self.game.height - 10))
        surface.blit(difficulty_text, text_rect)
        
    def draw_start_screen(self, surface):
        """Draw the start screen with theme selection"""
        # Fill with background
        surface.blit(self.game.background, (0, 0))
        
        # Draw title
        font_title = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 70)
        title_text = font_title.render('FRUIT NINJA!', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.width // 2, self.game.height // 4))
        surface.blit(title_text, title_rect)
        
        # Draw subtitle
        font_subtitle = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 35)
        subtitle_text = font_subtitle.render('Select a Theme', True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.game.width // 2, self.game.height // 2 - 45))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Create buttons if they don't exist
        if 'summer' not in self.buttons:
            self.create_button('summer', 'Summer', self.game.width // 4 - 75, self.game.height // 2, 150, 55, 
                               (0, 255, 0), (100, 255, 100), (0, 0, 0))
        if 'winter' not in self.buttons:
            self.create_button('winter', 'Winter', 3 * self.game.width // 4 - 75, self.game.height // 2, 150, 55, 
                               (0, 0, 255), (100, 100, 255), (255, 255, 255))
        
        # Draw buttons
        self.draw_button(surface, 'summer')
        self.draw_button(surface, 'winter')
        
        # Draw professor
        surface.blit(self.professor_image, self.professor_rect)
        
        # Draw instruction text
        font_instruction = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 20)
        instruction_text = font_instruction.render('Click the professor for fruit facts!', True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(
            center=(self.game.width // 2, self.game.height * 3 // 4 + 50))
        surface.blit(instruction_text, instruction_rect)
        
    def draw_game_over_screen(self, surface, score):
        """Draw the game over screen"""
        # Fill with background
        surface.blit(self.game.background, (0, 0))
        
        # Draw title
        font_title = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 70)
        title_text = font_title.render('GAME OVER!', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.width // 2, self.game.height // 4))
        surface.blit(title_text, title_rect)
        
        # Draw score
        font_score = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 35)
        score_text = font_score.render(f'Final Score: {score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.game.width // 2, self.game.height // 2))
        surface.blit(score_text, score_rect)
        
        # Create buttons if they don't exist
        if 'play_again' not in self.buttons:
            self.create_button('play_again', 'Play Again', self.game.width // 2 - 100, self.game.height * 3 // 4, 
                               200, 60, (0, 255, 0), (100, 255, 100), (0, 0, 0), 30)
        
        # Draw button
        self.draw_button(surface, 'play_again')
        
    def display_random_fact(self, surface):
        """Display a random fruit fact"""
        # Shuffle facts
        random.shuffle(self.fruit_facts)
        
        # Find a fact that hasn't been displayed yet
        for fact in self.fruit_facts:
            if fact not in self.facts_displayed:
                fact_font = pygame.font.Font(os.path.join('assets', 'fonts', 'mario.otf'), 20)
                
                # Create text surface with word wrapping
                fact_lines = []
                words = fact.split(' ')
                current_line = words[0]
                for word in words[1:]:
                    test_line = current_line + ' ' + word
                    # Check if the line is too long
                    if fact_font.size(test_line)[0] > self.game.width - 100:
                        fact_lines.append(current_line)
                        current_line = word
                    else:
                        current_line = test_line
                fact_lines.append(current_line)
                
                # Create a surface for the fact box
                padding = 20
                line_height = fact_font.size('A')[1] + 5
                box_height = len(fact_lines) * line_height + 2 * padding
                fact_box = pygame.Surface((self.game.width - 100, box_height))
                fact_box.fill((0, 0, 0))
                fact_box.set_alpha(200)
                
                # Draw the fact text
                for i, line in enumerate(fact_lines):
                    text_surface = fact_font.render(line, True, (255, 255, 255))
                    fact_box.blit(text_surface, (padding, padding + i * line_height))
                
                # Position and draw the fact box
                box_pos = (50, self.game.height // 2 + 100)
                surface.blit(fact_box, box_pos)
                
                # Add to displayed facts
                self.facts_displayed.append(fact)
                
                # Return the box rect for checking when to dismiss
                fact_rect = pygame.Rect(box_pos[0], box_pos[1], self.game.width - 100, box_height)
                return fact_rect
                
        # If all facts have been displayed, reset and start over
        if len(self.facts_displayed) >= len(self.fruit_facts):
            self.facts_displayed = []
            return self.display_random_fact(surface)
            
        return None
            
class EffectManager:
    """Manages visual effects like slices, explosions, etc."""
    
    def __init__(self, game):
        self.game = game
        self.effects = []
        
    def add_effect(self, effect_type, x, y):
        """Add a new effect"""
        if effect_type == 'slice':
            # Slice effect
            self.effects.append({
                'type': 'slice',
                'x': x,
                'y': y,
                'lifetime': 10,
                'rotation': random.randint(0, 360),
                'color': (255, 255, 255)
            })
        elif effect_type == 'explosion':
            # Explosion effect
            self.effects.append({
                'type': 'explosion',
                'x': x,
                'y': y,
                'lifetime': 30,
                'radius': 10
            })
        
    def update(self):
        """Update all effects"""
        for effect in self.effects[:]:
            effect['lifetime'] -= 1
            if effect['lifetime'] <= 0:
                self.effects.remove(effect)
                
    def draw(self, surface):
        """Draw all effects"""
        for effect in self.effects:
            if effect['type'] == 'slice':
                # Draw slice effect (a line)
                angle = effect['rotation']
                length = 50
                end_x = effect['x'] + length * pygame.math.Vector2(1, 0).rotate(angle).x
                end_y = effect['y'] + length * pygame.math.Vector2(1, 0).rotate(angle).y
                
                # Make the effect fade out
                alpha = int((effect['lifetime'] / 10) * 255)
                color = list(effect['color'])
                color.append(alpha)
                
                pygame.draw.line(surface, color, 
                                (effect['x'], effect['y']), 
                                (end_x, end_y), 
                                3)
            elif effect['type'] == 'explosion':
                # Draw explosion effect (expanding circle)
                radius = 10 + (30 - effect['lifetime']) * 3
                alpha = int((effect['lifetime'] / 30) * 255)
                explosion_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(explosion_surface, (255, 100, 0, alpha), (radius, radius), radius)
                surface.blit(explosion_surface, (effect['x'] - radius, effect['y'] - radius))
