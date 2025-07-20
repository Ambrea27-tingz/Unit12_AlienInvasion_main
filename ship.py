import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship(pygame.sprite.Sprite):
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal', *groups):
        """Initialize the ship and set its starting position."""
        # Call the parent class (Sprite) constructor from pygame
        super().__init__(*groups) 
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(
            self.image,
            (self.settings.ship_w, self.settings.ship_h)
        )
        
        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_right = False
        self.moving_left = False
        self.arsenal = arsenal

    def _center_ship(self):
        """Center the ship at the bottom of the screen."""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position based on movement flags."""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Update the ship's position based on movement flags."""
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
        self.rect.x = int(self.x)  # prevents float assignment error

    def draw(self):
        """Draw the ship and its arsenal to the screen."""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        """Fires a bullet if the arsenal limit is not reached."""
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group):
        """Checks for collisions between the ship and another group."""
        if pygame.sprite.spritecollideany(self, other_group):  # type: ignore[arg-type] error
            self._center_ship()
            return True
        return False