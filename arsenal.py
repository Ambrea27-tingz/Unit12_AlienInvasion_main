import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
   

class Arsenal:
    def __init__(self, game: 'AlienInvasion'):
        """Initialize the arsenal."""
        # Arsenal is a group of bullets
        # that the ship can fire
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """Update the position of bullets in the arsenal."""
        self.arsenal.update()
        self._remove_bullet_offscreen()


    def _remove_bullet_offscreen(self):
        """Remove bullets that have gone off the screen."""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self):
        """Draw the bullets in the arsenal."""
        for bullet in self.arsenal:
            bullet.draw()
    
    def fire_bullet(self):
        """Fires bullets if the limit is not reached.
        An checks if the arsenal has reached the bullet limit."""
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False
          
       