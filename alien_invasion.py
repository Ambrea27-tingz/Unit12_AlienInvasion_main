""" 
Lab13_awilliams2_2.py / CSCI 1511

Title: Alien Invasion

Discription: Alien Invasion is a creative game where the player controls a spaceship
and tries to annihilate neigboring enemies by shooting down the invading aliens. 
The game is built using Pygame.

Author: Ambrea Williams

Date: 2025-04-13
"""
import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
#from alien import Alien 
from alien_fleet import AlienFleet
from time import sleep

class AlienInvasion:
    """Main class that manages the game assets and behavior.""" 
    def __init__(self):
        """Prepare the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.game_stats = GameStats(self.settings.starting_ship_count)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w,self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
                (self.settings.screen_w, self.settings.screen_h)
                )

        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        self.ship_group = pygame.sprite.Group()
        self.ship = Ship(self, Arsenal(self), self.ship_group)
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.game_active = True

        self.game_stats = GameStats(self.settings.starting_ship_count)


        

    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            self._check_events()   
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)



    def _check_collisions(self):
        """Check for collisions between the ship, aliens, and projectiles."""
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            #subtract one life if possible

         #check collisions for aliens an bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
        #check collisions for projectiles and ship
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
        
        if self.alien_fleet.check_destroyed_status():  
            self._reset_level()
           
        
        
    def _check_game_status(self):

        """Check the game status and update lives or end the game.
        If the ship collides with an alien, reduce lives or end game."""

        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

        
           

      
        
    def _reset_level(self):

        """Reset the level by clearing the ship's arsenal 
        and recreating the alien fleet."""

        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()


    def _update_screen(self):
        """Update images on the screen, and flips to the new screen."""
        self.screen.blit(self.bg, (0, 0)) 
        self.ship.draw()  
        self.alien_fleet.draw()
        pygame.display.flip()

    def _check_events(self):
        """React to keypresses and mouse events."""  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)

            #play the laser sound
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()
            
        
       

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()