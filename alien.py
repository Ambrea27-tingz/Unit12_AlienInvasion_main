import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """Initialize the alien and set its starting position."""
        # Call the parent class (Sprite) constructor from pygame
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings
        
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
             (self.settings.alien_w, self.settings.alien_h)
             )
        
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.x = int(x) 
        self.rect.y = self.rect.y = int(y)
        
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Update the alien's position."""
        temp_speed = self.settings.fleet_speed
                
        self.x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.rect.x = int(self.y)
        self.rect.y = self.rect.y = int(self.y)

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        return (self.rect.right >= self.boundaries.right or
                self.rect.left <= self.boundaries.left)

    def draw_alien(self):
        """Draw the alien at its current position."""
        self.screen.blit(self.image, self.rect)
        