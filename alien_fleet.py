import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
  
class AlienFleet:
    
    def __init__(self, game: 'AlienInvasion'):

        """Initialize the fleet."""
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed
        self.create_fleet()

    def create_fleet(self):
        """Creates a cross-shaped fleet of aliens."""
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        # Calculate how many aliens fit horizontally and vertically
        fleet_w = screen_w // (alien_w * 2)
        fleet_h = (screen_h // 2) // (alien_h * 2)

        # Ensure an odd number so we have a center row/col
        if fleet_w % 2 == 0:
         fleet_w -= 1
        if fleet_h % 2 == 0:
         fleet_h -= 1

        x_offset = (screen_w - fleet_w * alien_w * 1.2) // 2
        y_offset = (screen_h // 2 - fleet_h * alien_h * 1.2) // 2

        center_col = fleet_w // 2
        center_row = fleet_h // 2

        for row in range(fleet_h):
            for col in range(fleet_w):
                if row == center_row or col == center_col:
                    x = x_offset + 1.2 * col * alien_w
                    y = y_offset + 1.2 * row * alien_h
                    self._create_alien(int(x), int(y))

    def _create_cross_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """Create a cross-shaped fleet of aliens."""
        center_col = fleet_w // 2
        center_row = fleet_h // 2

        for row in range(fleet_h):
            for col in range(fleet_w):
                if row == center_row or col == center_col:
                    current_x = alien_w * col + x_offset
                    current_y = alien_h * row + y_offset
                    self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """Calculate offsets for the fleet based on screen size and alien size."""
        half_screen = self.settings.screen_h//2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h
        x_offset = int((screen_w - fleet_horizontal_space)// 2)
        y_offset = int((half_screen - fleet_vertical_space)// 2)
        return x_offset,y_offset


    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """Calculate the number of aliens that can fit in the fleet."""
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h /2)//alien_h)

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2

        

        return int(fleet_w), int(fleet_h)

    def _create_alien(self, current_x: int, current_y: int):
        """Create an alien at the specified position."""
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """Check if any alien in the fleet has reached the edge of the screen."""
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
                
    def _drop_alien_fleet(self):
        """Drop the entire fleet down by the fleet drop speed."""
        for alien in self.fleet:
           alien.y += self.fleet_drop_speed
                     
    def update_fleet(self):
        """Update the position of the fleet and check for edge collisions."""
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """Draw the aliens in the fleet."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()
    
    def check_collisions(self, other_group):
        """Checks for collisions between the fleet and another group.
        Returns a dictionary of collided aliens and the projectiles."""
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)


    def check_fleet_bottom(self):
        """Check if any alien in the fleet has reached the bottom of the screen."""
        alien: 'Alien'
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False

    def check_destroyed_status(self):
        """Check if the fleet is empty.
        Returns True if the fleet is empty, otherwise False."""
        return not self.fleet