# Zelda The Lich King Tales
# My awesome game menu inspired by Zelda
# Made by FallenGodfather

import arcade
import random
import math
import os

from config import MUSIC_FILE

# Game settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TITLE = "Zelda The Lich King Tales"

# Global music player to prevent multiple instances
music_player = None

class MenuScreen(arcade.View):
    def __init__(self, initial_selected=0):
        super().__init__()

        # My menu stuff
        self.raindrops = None
        self.selected = initial_selected  # Remember which option was selected
        self.timer = 0.0
        self.sparkles = []
        self.background_texture = None
        self.pulse = 130 + int(30 * math.sin(self.timer * 4))

        # What can the player choose?
        self.choices = [
            "Start",
            "Settings",
            "About",
            "Quit"
        ]

        # Make some cool sparkly effects
        # self.make_sparkles()
        self.make_raindrops()

    # def make_sparkles(self):
    #     # Add some magic sparkles floating around
    #     for i in range(20):
    #         sparkle = {'x': random.randint(0, WINDOW_WIDTH), 'y': random.randint(0, WINDOW_HEIGHT),
    #                    'speed': random.randint(10, 40), 'size': random.randint(2, 4)}
    #         self.sparkles.append(sparkle)

    def make_raindrops(self):
        """Create a list of raindrop dictionaries."""
        self.raindrops = []
        for _ in range(120):  # how many raindrops on screen
            drop = {
                "x": random.randint(0, WINDOW_WIDTH),
                "y": random.randint(0, WINDOW_HEIGHT),
                "speed": random.uniform(600, 1200),  # pixels per second
                "length": random.randint(12, 20)
            }
            self.raindrops.append(drop)

    def on_show_view(self):
        global music_player

        arcade.set_background_color((10, 10, 25, 0))

        # Load my cool background if I have one
        if os.path.exists("generated_image.png"):
            self.background_texture = arcade.load_texture("generated_image.png")
            print("Sweet! Found the background image")
        else:
            print("No background image found, using default")

        # Try to play some epic music (only if not already playing)
        if music_player is None:
            if os.path.exists(MUSIC_FILE):
                sound = arcade.load_sound(MUSIC_FILE)
                music_player = arcade.play_sound(sound, volume=0.4, loop=True)
                print(f"Playing music: {MUSIC_FILE}")

    def on_update(self, dt):
        self.timer += dt

        # Move sparkles around
        # for sparkle in self.sparkles:
        #     sparkle['y'] -= sparkle['speed'] * dt
        #     sparkle['x'] += math.sin(self.timer + sparkle['x'] * 0.01) * 15 * dt
        #
        #     if sparkle['y'] < 0:
        #         sparkle['y'] = WINDOW_HEIGHT
        #         sparkle['x'] = random.randint(0, WINDOW_WIDTH)

        for drop in self.raindrops:
            drop["y"] -= drop["speed"] * dt
            # simple wind: drift a little to the right
            drop["x"] += 60 * dt
            if drop["y"] < -drop["length"] or drop["x"] > WINDOW_WIDTH + 10:
                # restart raindrop at top with random x
                drop["y"] = WINDOW_HEIGHT + random.randint(0, 100)
                drop["x"] = random.randint(-50, WINDOW_WIDTH)

    def on_draw(self):
        self.clear()

        # Draw my background
        if self.background_texture:
            # Figure out how to make it fit nicely
            scale_x = WINDOW_WIDTH / self.background_texture.width
            scale_y = WINDOW_HEIGHT / self.background_texture.height
            scale = max(scale_x, scale_y)

            # Draw it centered
            arcade.draw_texture_rect(
                self.background_texture,
                arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
            )
        else:
            # Make a cool animated background
            for y in range(0, WINDOW_HEIGHT, 6):
                wave = math.sin(self.timer * 0.5 + y * 0.01)
                r = int(10 + 8 * wave)
                g = int(10 + 12 * math.sin(self.timer * 0.3 + y * 0.008))
                b = int(25 + 15 * math.cos(self.timer * 0.2 + y * 0.006))
                arcade.draw_line(0, y, WINDOW_WIDTH, y, (r, g, b), 6)


        # Draw sparkles
        # for sparkle in self.sparkles:
        #     twinkle = math.sin(self.timer * 3 + sparkle['x'] * 0.01)
        #     if twinkle > 0.3:
        #         arcade.draw_circle_filled(
        #             sparkle['x'], sparkle['y'], sparkle['size'],
        #             (255, 255, 255)
        #         )

        for drop in self.raindrops:
            # draw the drop as a short diagonal line (rain slant)
            drop_end_x = drop["x"] + 4  # small slant to the right
            drop_end_y = drop["y"] - drop["length"]
            arcade.draw_line(
                drop["x"], drop["y"],
                drop_end_x, drop_end_y,
                (150, 150, 200), 1)

        # Game title with cool red glow
        title_text = "ZELDA THE LICH KING TALES"

        # Red glow effect
        glow = 0.7 + 0.3 * math.sin(self.timer * 1.2)
        for i in range(5, 0, -1):
            red = int(200 * glow)
            arcade.draw_text(title_text, WINDOW_WIDTH//2 + i, 460 + i,
                           (red, 0, 0), 40, anchor_x="center")

        # Main title
        pulse = 130 + int(30 * math.sin(self.timer * 4))
        arcade.draw_text(title_text, WINDOW_WIDTH//2, 460,
                        (255, 215, pulse), 40, anchor_x="center")

        # Subtitle
        pulse = 130 + int(30 * math.sin(self.timer * 4))
        arcade.draw_text("~ The Dark Lord Awaits ~", WINDOW_WIDTH//2, 440,
                        (180, 180, pulse), 16, anchor_x="center")

        # Menu options
        for i, choice in enumerate(self.choices):
            y = 380 - i * 50

            # Highlight selected option
            if i == self.selected:
                # Selection box
                pulse = 130 + int(30 * math.sin(self.timer * 4))
                color = (70, 70, pulse)
                # color = (255, 255, 255)

                # Draw box outline
                w, h = 300, 35
                x = WINDOW_WIDTH//2
                arcade.draw_line(x-w//2, y+h//2, x+w//2, y+h//2, color, 2)
                arcade.draw_line(x-w//2, y-h//2, x+w//2, y-h//2, color, 2)
                arcade.draw_line(x-w//2, y-h//2, x-w//2, y+h//2, color, 2)
                arcade.draw_line(x+w//2, y-h//2, x+w//2, y+h//2, color, 2)

                text_color = (255, 255, 255)
            else:
                text_color = (160, 160, 160)

            arcade.draw_text(choice, WINDOW_WIDTH//2, y, text_color, 22, anchor_x="center")

        # Instructions
        arcade.draw_text("Use ↑↓ to navigate, ENTER to select",
                        WINDOW_WIDTH//2, 80, (120, 120, 120), 12, anchor_x="center")

        # My name
        arcade.draw_text("Made by FallenGodfather",
                        WINDOW_WIDTH//2, 50, (100, 100, 100), 11, anchor_x="center")


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected = (self.selected - 1) % len(self.choices)
        elif key == arcade.key.DOWN:
            self.selected = (self.selected + 1) % len(self.choices)
        elif key == arcade.key.ENTER:
            self.handle_choice()
        elif key == arcade.key.ESCAPE:
            # Only stop music if ESC means quitting the game
            global music_player
            arcade.close_window()
            if music_player is not None:
                arcade.stop_sound(music_player)
                music_player = None

    def handle_choice(self):
        if self.selected == 0:  # Start Adventure
            game = GameScreen()
            self.window.show_view(game)
        elif self.selected == 1:  # Settings  
            settings = SettingsScreen()
            self.window.show_view(settings)
        elif self.selected == 2:  # About
            about = AboutScreen()
            self.window.show_view(about)
        elif self.selected == 3:  # Quit
            global music_player
            arcade.close_window()
            if music_player is not None:
                arcade.stop_sound(music_player)
                music_player = None


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 32
        self.height = 32
        self.color = (50, 200, 50)
        self.health = 100
        self.max_health = 100
        self.damage = 10
        self.speed = 200
        self.attack_cooldown = 0
        self.invincible_timer = 0
        
    def draw(self):
        # Draw Link as a simple character
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)
        # Draw face
        arcade.draw_circle_filled(self.center_x - 5, self.center_y + 8, 2, (255, 255, 255))
        arcade.draw_circle_filled(self.center_x + 5, self.center_y + 8, 2, (255, 255, 255))
        # Shield
        arcade.draw_triangle_filled(
            self.center_x - 18, self.center_y + 10,
            self.center_x - 18, self.center_y - 10,
            self.center_x - 8, self.center_y,
            (100, 150, 255)
        )
        
    def update(self, delta_time):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time


class Enemy(arcade.Sprite):
    def __init__(self, x, y, enemy_type="mob"):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.enemy_type = enemy_type
        
        if enemy_type == "mob":
            self.width = 24
            self.height = 24
            self.color = (200, 50, 50)
            self.health = 30
            self.speed = 80
            self.damage = 5
            self.patrol_range = 100
            self.start_x = x
        elif enemy_type == "boss":
            self.width = 80
            self.height = 80
            self.color = (100, 50, 25)
            self.health = 200
            self.max_health = 200
            self.speed = 60
            self.damage = 15
            self.attack_timer = 0
            
        self.direction = 1
        self.chase_range = 150
        
    def draw(self):
        if self.invincible_timer > 0 and int(self.invincible_timer * 10) % 2:
            return
            
        if self.enemy_type == "mob":
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)
            # Eyes
            arcade.draw_circle_filled(self.center_x - 4, self.center_y + 4, 2, (255, 200, 0))
            arcade.draw_circle_filled(self.center_x + 4, self.center_y + 4, 2, (255, 200, 0))
        elif self.enemy_type == "boss":
            # King Kong-like boss
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)
            # Face
            arcade.draw_circle_filled(self.center_x - 12, self.center_y + 15, 5, (50, 20, 10))
            arcade.draw_circle_filled(self.center_x + 12, self.center_y + 15, 5, (50, 20, 10))
            # Mouth
            arcade.draw_rectangle_filled(self.center_x, self.center_y - 5, 25, 8, (150, 100, 75))
            # Arms
            arcade.draw_rectangle_filled(self.center_x - 50, self.center_y, 20, 60, (120, 70, 35))
            arcade.draw_rectangle_filled(self.center_x + 50, self.center_y, 20, 60, (120, 70, 35))
    
    def update(self, delta_time, player_x, player_y):
        if hasattr(self, 'invincible_timer'):
            if self.invincible_timer > 0:
                self.invincible_timer -= delta_time
        
        dist_to_player = math.sqrt((self.center_x - player_x)**2 + (self.center_y - player_y)**2)
        
        if self.enemy_type == "mob":
            if dist_to_player < self.chase_range:
                # Chase player
                if player_x > self.center_x:
                    self.center_x += self.speed * delta_time
                else:
                    self.center_x -= self.speed * delta_time
                    
                if player_y > self.center_y:
                    self.center_y += self.speed * delta_time
                else:
                    self.center_y -= self.speed * delta_time
            else:
                # Patrol
                self.center_x += self.speed * delta_time * self.direction
                if abs(self.center_x - self.start_x) > self.patrol_range:
                    self.direction *= -1
                    
        elif self.enemy_type == "boss":
            if hasattr(self, 'attack_timer'):
                self.attack_timer += delta_time
                
            # Boss slowly follows player
            if dist_to_player > 100:
                if player_x > self.center_x:
                    self.center_x += self.speed * delta_time
                else:
                    self.center_x -= self.speed * delta_time
                    
                if player_y > self.center_y:
                    self.center_y += self.speed * delta_time
                else:
                    self.center_y -= self.speed * delta_time


class NPC(arcade.Sprite):
    def __init__(self, x, y, name, dialogue):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = 30
        self.height = 30
        self.name = name
        self.dialogue = dialogue
        self.color = (100, 100, 200)
        
    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)
        # Beard for old Jude
        arcade.draw_triangle_filled(
            self.center_x - 10, self.center_y - 8,
            self.center_x + 10, self.center_y - 8,
            self.center_x, self.center_y - 20,
            (200, 200, 200)
        )
        # Hat
        arcade.draw_triangle_filled(
            self.center_x - 12, self.center_y + 15,
            self.center_x + 12, self.center_y + 15,
            self.center_x, self.center_y + 28,
            (150, 100, 50)
        )


class GameScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.time = 0
        self.player = Player()
        self.player.center_x = 150
        self.player.center_y = 150
        
        # Game state
        self.game_state = "intro"  # intro, playing, dialogue, win, lose
        self.dialogue_text = []
        self.dialogue_index = 0
        self.show_dialogue = False
        self.dialogue_timer = 0
        
        # Level objects
        self.walls = []
        self.enemies = []
        self.npcs = []
        self.chalice_pos = None
        self.has_chalice = False
        self.boss_spawned = False
        self.boss = None
        
        # Camera offset for scrolling
        self.camera_x = 0
        self.camera_y = 0
        
        # Controls
        self.keys_pressed = set()
        
        self.setup_level()
        
    def setup_level(self):
        # Create island walls (boundaries)
        wall_color = (101, 67, 33)  # Brown for rocks
        
        # Top wall
        for x in range(0, 1400, 40):
            wall = arcade.SpriteSolidColor(40, 40, wall_color)
            wall.center_x = x
            wall.center_y = 800
            self.walls.append(wall)
            
        # Bottom wall  
        for x in range(0, 1400, 40):
            wall = arcade.SpriteSolidColor(40, 40, wall_color)
            wall.center_x = x
            wall.center_y = 0
            self.walls.append(wall)
            
        # Left wall
        for y in range(40, 800, 40):
            wall = arcade.SpriteSolidColor(40, 40, wall_color)
            wall.center_x = 0
            wall.center_y = y
            self.walls.append(wall)
            
        # Right wall
        for y in range(40, 800, 40):
            wall = arcade.SpriteSolidColor(40, 40, wall_color)
            wall.center_x = 1400
            wall.center_y = y
            self.walls.append(wall)
        
        # Palace structure (top right)
        for x in range(1000, 1300, 40):
            for y in range(600, 750, 40):
                wall = arcade.SpriteSolidColor(40, 40, (150, 150, 150))
                wall.center_x = x
                wall.center_y = y
                self.walls.append(wall)
                
        # Palace entrance
        for x in range(1080, 1180, 40):
            wall = arcade.SpriteSolidColor(40, 40, (150, 150, 150))
            wall.center_x = x
            wall.center_y = 600
            if wall in self.walls:
                self.walls.remove(wall)
        
        # Chalice position (inside palace)
        self.chalice_pos = (1150, 680)
        
        # Add NPC Jude near starting position
        jude_dialogue = [
            "Jude: Ah, you're awake! Welcome to the Deserted Island.",
            "Jude: The Lich King's curse has brought you here.",
            "Jude: You must find the Chalice of the Old Palace.",
            "Jude: It lies to the northeast, but beware...",
            "Jude: Dark creatures guard the path!",
            "Jude: Good luck, young hero!"
        ]
        self.npcs.append(NPC(200, 200, "Jude", jude_dialogue))
        
        # Add enemy mobs
        self.enemies.append(Enemy(400, 300, "mob"))
        self.enemies.append(Enemy(600, 400, "mob"))
        self.enemies.append(Enemy(800, 250, "mob"))
        self.enemies.append(Enemy(700, 600, "mob"))
        self.enemies.append(Enemy(500, 500, "mob"))
        
    def spawn_boss(self):
        if not self.boss_spawned:
            self.boss_spawned = True
            self.boss = Enemy(900, 650, "boss")
            self.enemies.append(self.boss)
            self.dialogue_text = ["A mighty beast appears!", "It's the Palace Guardian - a King Kong-like creature!"]
            self.dialogue_index = 0
            self.show_dialogue = True
            self.dialogue_timer = 0

    def on_show_view(self):
        arcade.set_background_color((194, 178, 128))  # Sandy beach color
        # Show intro dialogue
        self.dialogue_text = [
            "Link slowly opens his eyes...",
            "He finds himself on a deserted island.",
            "An old man approaches..."
        ]
        self.dialogue_index = 0
        self.show_dialogue = True
        self.game_state = "intro"

    def on_update(self, dt):
        self.time += dt
        
        if self.game_state == "intro" or self.game_state == "dialogue":
            self.dialogue_timer += dt
            return
            
        if self.game_state == "win" or self.game_state == "lose":
            return
        
        # Update player
        self.player.update(dt)
        
        # Player movement
        move_x = 0
        move_y = 0
        
        if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
            move_x -= self.player.speed * dt
        if arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
            move_x += self.player.speed * dt
        if arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed:
            move_y += self.player.speed * dt
        if arcade.key.DOWN in self.keys_pressed or arcade.key.S in self.keys_pressed:
            move_y -= self.player.speed * dt
            
        # Apply movement with collision detection
        self.player.center_x += move_x
        if arcade.check_for_collision_with_list(self.player, self.walls):
            self.player.center_x -= move_x
            
        self.player.center_y += move_y
        if arcade.check_for_collision_with_list(self.player, self.walls):
            self.player.center_y -= move_y
        
        # Update camera to follow player
        self.camera_x = self.player.center_x - WINDOW_WIDTH // 2
        self.camera_y = self.player.center_y - WINDOW_HEIGHT // 2
        
        # Clamp camera
        self.camera_x = max(0, min(self.camera_x, 1400 - WINDOW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, 800 - WINDOW_HEIGHT))
        
        # Update enemies
        for enemy in self.enemies[:]:
            if hasattr(enemy, 'health') and enemy.health <= 0:
                self.enemies.remove(enemy)
                continue
            enemy.update(dt, self.player.center_x, self.player.center_y)
            
            # Enemy collision with player
            if arcade.check_for_collision(self.player, enemy):
                if self.player.invincible_timer <= 0:
                    self.player.health -= enemy.damage
                    self.player.invincible_timer = 1.0
                    if self.player.health <= 0:
                        self.game_state = "lose"
        
        # Check NPC interaction
        for npc in self.npcs:
            dist = math.sqrt((self.player.center_x - npc.center_x)**2 + (self.player.center_y - npc.center_y)**2)
            if dist < 60 and arcade.key.SPACE in self.keys_pressed:
                self.dialogue_text = npc.dialogue
                self.dialogue_index = 0
                self.show_dialogue = True
                self.game_state = "dialogue"
                self.dialogue_timer = 0
                
        # Check chalice collection
        if self.chalice_pos and not self.has_chalice:
            dist = math.sqrt((self.player.center_x - self.chalice_pos[0])**2 + 
                           (self.player.center_y - self.chalice_pos[1])**2)
            if dist < 40:
                self.has_chalice = True
                self.spawn_boss()
        
        # Check win condition (defeat boss)
        if self.boss_spawned and self.boss and self.boss.health <= 0:
            self.game_state = "win"

    def on_draw(self):
        self.clear()
        
        # Draw ground/sand
        for x in range(int(self.camera_x // 50) * 50, int(self.camera_x + WINDOW_WIDTH), 50):
            for y in range(int(self.camera_y // 50) * 50, int(self.camera_y + WINDOW_HEIGHT), 50):
                color_var = (hash((x, y)) % 20) - 10
                sand_color = (194 + color_var, 178 + color_var, 128 + color_var)
                arcade.draw_rectangle_filled(x - self.camera_x, y - self.camera_y, 50, 50, sand_color)
        
        # Draw water around island
        arcade.draw_rectangle_filled(700 - self.camera_x, -50 - self.camera_y, 1400, 100, (70, 130, 180))
        arcade.draw_rectangle_filled(700 - self.camera_x, 850 - self.camera_y, 1400, 100, (70, 130, 180))
        arcade.draw_rectangle_filled(-50 - self.camera_x, 400 - self.camera_y, 100, 800, (70, 130, 180))
        arcade.draw_rectangle_filled(1450 - self.camera_x, 400 - self.camera_y, 100, 800, (70, 130, 180))
        
        # Draw walls
        for wall in self.walls:
            wall.draw()
            wall.center_x -= self.camera_x
            wall.center_y -= self.camera_y
            wall.draw()
            wall.center_x += self.camera_x
            wall.center_y += self.camera_y
            
        # Draw chalice
        if self.chalice_pos and not self.has_chalice:
            x, y = self.chalice_pos
            arcade.draw_circle_filled(x - self.camera_x, y - self.camera_y, 15, (255, 215, 0))
            arcade.draw_circle_outline(x - self.camera_x, y - self.camera_y, 15, (200, 170, 0), 3)
            # Glow effect
            glow = 0.5 + 0.5 * math.sin(self.time * 3)
            arcade.draw_circle_filled(x - self.camera_x, y - self.camera_y, 20 * glow, (255, 215, 0, 100))
            
        # Draw NPCs
        for npc in self.npcs:
            npc.center_x -= self.camera_x
            npc.center_y -= self.camera_y
            npc.draw()
            npc.center_x += self.camera_x
            npc.center_y += self.camera_y
            
            # Show interaction hint
            dist = math.sqrt((self.player.center_x - npc.center_x)**2 + (self.player.center_y - npc.center_y)**2)
            if dist < 60:
                arcade.draw_text("Press SPACE to talk", 
                               npc.center_x - self.camera_x, 
                               npc.center_y - self.camera_y + 25, 
                               (255, 255, 255), 10, anchor_x="center")
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.center_x -= self.camera_x
            enemy.center_y -= self.camera_y
            enemy.draw()
            enemy.center_x += self.camera_x
            enemy.center_y += self.camera_y
            
            # Draw boss health bar
            if enemy.enemy_type == "boss" and hasattr(enemy, 'max_health'):
                health_ratio = enemy.health / enemy.max_health
                bar_width = 100
                arcade.draw_rectangle_filled(
                    enemy.center_x - self.camera_x, 
                    enemy.center_y - self.camera_y + 60,
                    bar_width, 8, (100, 100, 100))
                arcade.draw_rectangle_filled(
                    enemy.center_x - self.camera_x - bar_width//2 + (bar_width * health_ratio)//2, 
                    enemy.center_y - self.camera_y + 60,
                    bar_width * health_ratio, 8, (200, 50, 50))
        
        # Draw player
        self.player.center_x -= self.camera_x
        self.player.center_y -= self.camera_y
        if self.player.invincible_timer <= 0 or int(self.player.invincible_timer * 10) % 2:
            self.player.draw()
        self.player.center_x += self.camera_x
        self.player.center_y += self.camera_y
        
        # Draw HUD
        # Health bar
        arcade.draw_rectangle_filled(100, WINDOW_HEIGHT - 30, 200, 20, (100, 100, 100))
        health_ratio = max(0, self.player.health / self.player.max_health)
        arcade.draw_rectangle_filled(100 - 100 + 100 * health_ratio, WINDOW_HEIGHT - 30, 
                                    200 * health_ratio, 20, (50, 200, 50))
        arcade.draw_text(f"HP: {int(self.player.health)}/{self.player.max_health}", 
                        100, WINDOW_HEIGHT - 35, (255, 255, 255), 12, anchor_x="center")
        
        # Objective
        if not self.has_chalice:
            arcade.draw_text("Objective: Find the Chalice in the Old Palace", 
                           WINDOW_WIDTH//2, WINDOW_HEIGHT - 20, (255, 255, 255), 14, anchor_x="center")
        elif self.boss_spawned and self.boss and self.boss.health > 0:
            arcade.draw_text("Objective: Defeat the Palace Guardian!", 
                           WINDOW_WIDTH//2, WINDOW_HEIGHT - 20, (255, 200, 100), 14, anchor_x="center")
        
        # Controls hint
        arcade.draw_text("WASD/Arrows: Move  SPACE: Attack/Talk  ESC: Menu", 
                        WINDOW_WIDTH//2, 20, (200, 200, 200), 10, anchor_x="center")
        
        # Dialogue box
        if self.show_dialogue and self.dialogue_index < len(self.dialogue_text):
            box_height = 120
            arcade.draw_rectangle_filled(WINDOW_WIDTH//2, box_height//2 + 20, 
                                        WINDOW_WIDTH - 100, box_height, (20, 20, 40))
            arcade.draw_rectangle_outline(WINDOW_WIDTH//2, box_height//2 + 20, 
                                         WINDOW_WIDTH - 100, box_height, (255, 255, 255), 3)
            
            text = self.dialogue_text[self.dialogue_index]
            arcade.draw_text(text, WINDOW_WIDTH//2, box_height//2 + 30, 
                           (255, 255, 255), 14, anchor_x="center", width=WINDOW_WIDTH - 150, 
                           align="center", multiline=True)
            
            arcade.draw_text("Press SPACE to continue", WINDOW_WIDTH//2, 30, 
                           (150, 150, 150), 10, anchor_x="center")
        
        # Game over screens
        if self.game_state == "win":
            arcade.draw_rectangle_filled(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 
                                        WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))
            arcade.draw_text("VICTORY!", WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50, 
                           (255, 215, 0), 48, anchor_x="center")
            arcade.draw_text("You defeated the Palace Guardian!", 
                           WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 
                           (255, 255, 255), 20, anchor_x="center")
            arcade.draw_text("The Chalice is yours!", 
                           WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40, 
                           (255, 255, 255), 20, anchor_x="center")
            arcade.draw_text("Press ESC to return to menu", 
                           WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100, 
                           (200, 200, 200), 14, anchor_x="center")
                           
        elif self.game_state == "lose":
            arcade.draw_rectangle_filled(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 
                                        WINDOW_WIDTH, WINDOW_HEIGHT, (0, 0, 0, 200))
            arcade.draw_text("GAME OVER", WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50, 
                           (200, 50, 50), 48, anchor_x="center")
            arcade.draw_text("You were defeated...", 
                           WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 
                           (255, 255, 255), 20, anchor_x="center")
            arcade.draw_text("Press ESC to return to menu", 
                           WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60, 
                           (200, 200, 200), 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
        if key == arcade.key.ESCAPE:
            menu = MenuScreen(initial_selected=0)
            self.window.show_view(menu)
            
        if key == arcade.key.SPACE:
            if self.show_dialogue:
                self.dialogue_index += 1
                if self.dialogue_index >= len(self.dialogue_text):
                    self.show_dialogue = False
                    if self.game_state == "intro":
                        self.game_state = "playing"
                    elif self.game_state == "dialogue":
                        self.game_state = "playing"
                self.dialogue_timer = 0
            elif self.game_state == "playing" and self.player.attack_cooldown <= 0:
                # Attack nearby enemies
                self.player.attack_cooldown = 0.5
                for enemy in self.enemies:
                    dist = math.sqrt((self.player.center_x - enemy.center_x)**2 + 
                                   (self.player.center_y - enemy.center_y)**2)
                    if dist < 60:
                        if not hasattr(enemy, 'invincible_timer'):
                            enemy.invincible_timer = 0
                        if enemy.invincible_timer <= 0:
                            enemy.health -= self.player.damage
                            enemy.invincible_timer = 0.3
                            
    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)


class SettingsScreen(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((20, 20, 40, 0))

    def on_draw(self):
        self.clear()

        arcade.draw_text("SETTINGS",
                        WINDOW_WIDTH//2, 600, (255, 200, 0), 30, anchor_x="center")

        # My settings list
        settings = [
            "🔊 Music Volume: 60%",
            "🔊 Sound Effects: 80%", 
            "🖥️ Resolution: 1000x700",
            "🎮 Controls: Arrow Keys + Enter",
            "✨ Effects: On",
            "",
            "Background: Custom AI Image",
            "Music: Gerudo Valley Metal Version",
            "Theme: Dark Fantasy"
        ]

        y = 480
        for setting in settings:
            if setting:
                arcade.draw_text(setting, WINDOW_WIDTH//2, y,
                               (170, 170, 255), 15, anchor_x="center")
            y -= 30

        arcade.draw_text("Press ESC to go back",
                        WINDOW_WIDTH//2, 100, (120, 120, 120), 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu = MenuScreen(initial_selected=1)  # Return to Settings option
            self.window.show_view(menu)


class AboutScreen(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((40, 25, 15, 0))

    def on_draw(self):
        self.clear()

        arcade.draw_text("ABOUT",
                        WINDOW_WIDTH//2, 600, (255, 200, 0), 30, anchor_x="center")

        # Story and credits
        info = [
            "Game: Zelda The Lich King Tales",
            "Created by: FallenGodfather",
            "",
            "🏰 The Story:",
            "Long ago, an evil sorcerer known as the Lich King",
            "cast a dark spell over the peaceful land of Hyrule.",
            "Ancient heroes have failed to stop him.",
            "Now it's up to you to save the kingdom!",
            "",
            "🎵 Music: Gerudo Valley (Metal Version)",
            "   Original by Nintendo/Koji Kondo",
            "   Metal version by Machinae Supremacy",
            "",
            "🎮 Built with Python Arcade",
            "🎨 Background: AI Generated Art",
            "💡 Inspired by The Legend of Zelda series",
            "",
            "Thanks for playing my game!"
        ]

        y = 520
        for line in info:
            if line:
                if line.startswith("Game:") or line.startswith("Created by:"):
                    color = (255, 200, 50)
                    size = 16
                elif line.startswith("🏰") or line.startswith("🎵"):
                    color = (255, 150, 150)
                    size = 15
                else:
                    color = (190, 190, 190)
                    size = 14

                arcade.draw_text(line, WINDOW_WIDTH//2, y, color, size, anchor_x="center")
            y -= 25

        arcade.draw_text("Press ESC to go back",
                        WINDOW_WIDTH//2, 60, (120, 120, 120), 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu = MenuScreen(initial_selected=2)  # Return to About option
            self.window.show_view(menu)


def main():
    # Start up my game
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)

    print("Starting up Zelda The Lich King Tales...")
    print("Hope you enjoy the game!")

    # Show the main menu
    menu = MenuScreen()
    window.show_view(menu)
    arcade.run()


# Run the game when this file is executed
if __name__ == "__main__":
    main()
