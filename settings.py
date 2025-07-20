from pathlib import Path
class Settings:
    """A class that overhauls all settings for Alien Invasion."""
    def __init__(self):
        """Prepare the game's settings."""
        self.name: str = "Alien Invasion"
        self.screen_w = 1200
        self.screen_h = 800
        #frames per second
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship.png'
        self.ship_w = 70
        self.ship_h = 95
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        
        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_amount = 5

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w  = 40 #originally 80
        self.alien_h = 40
        self.fleet_speed = 2  #originally 5
        self.fleet_direction = 1 
        self.fleet_drop_speed = 40