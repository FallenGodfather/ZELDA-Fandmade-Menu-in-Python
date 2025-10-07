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

class MenuScreen(arcade.View):
    def __init__(self):
        super().__init__()

        # My menu stuff
        self.raindrops = None
        self.selected = 0
        self.timer = 0.0
        self.sparkles = []
        self.background_texture = None
        self.music = None

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

        self.play_menu_theme_song()



    # def make_sparkles(self):
    #     # Add some magic sparkles floating around
    #     for i in range(20):
    #         sparkle = {'x': random.randint(0, WINDOW_WIDTH), 'y': random.randint(0, WINDOW_HEIGHT),
    #                    'speed': random.randint(10, 40), 'size': random.randint(2, 4)}
    #         self.sparkles.append(sparkle)
    def play_menu_theme_song(self):
        if self.music is not None:
            arcade.sound.stop_sound(self.music)
        elif self.music is None:
            self.music = arcade.load_sound(MUSIC_FILE)
            arcade.play_sound(self.music, 0.4, loop=True)
            print(f"Playing music: {self.music}")
        else:
            pass


    def make_raindrops(self):
        """Create a list of raindrop dictionaries."""
        self.raindrops = []
        for _ in range(120):  # how many raindrops on screen
            drop = {
                "x": random.randint(0, WINDOW_WIDTH),
                "y": random.randint(0, WINDOW_HEIGHT),
                "speed": random.uniform(200, 400),  # pixels per second
                "length": random.randint(12, 20)
            }
            self.raindrops.append(drop)

    def on_show_view(self):
        arcade.set_background_color((10, 10, 25, 0))

        # Load my cool background if I have one
        if os.path.exists("generated_image.png"):
            self.background_texture = arcade.load_texture("generated_image.png")
            print("Sweet! Found the background image")
        else:
            print("No background image found, using default")

        # Try to play some epic music


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
                (150, 150, 200), 2)

        # Game title with cool red glow
        title_text = "ZELDA THE LICH KING TALES"

        # Red glow effect
        glow = 0.7 + 0.3 * math.sin(self.timer * 1.2)
        for i in range(5, 0, -1):
            red = int(200 * glow)
            arcade.draw_text(title_text, WINDOW_WIDTH//2 + i, 580 + i,
                           (red, 0, 0), 40, anchor_x="center")

        # Main title
        arcade.draw_text(title_text, WINDOW_WIDTH//2, 580,
                        (255, 215, 0), 40, anchor_x="center")

        # Subtitle
        arcade.draw_text("~ The Dark Lord Awaits ~", WINDOW_WIDTH//2, 540,
                        (180, 180, 255), 16, anchor_x="center")

        # Menu options
        for i, choice in enumerate(self.choices):
            y = 400 - i * 50

            # Highlight selected option
            if i == self.selected:
                # Selection box
                pulse = 130 + int(30 * math.sin(self.timer * 4))
                color = (70, 70, pulse)

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
            arcade.close_window()

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
            arcade.close_window()


class GameScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.time = 0

    def on_show_view(self):
        arcade.set_background_color((15, 40, 15, 0))

    def on_update(self, dt):
        self.time += dt

    def on_draw(self):
        self.clear()

        arcade.draw_text("🗡️ THE ADVENTURE BEGINS! 🗡️",
                        WINDOW_WIDTH//2, 450, (255, 255, 255), 32, anchor_x="center")

        arcade.draw_text("You stand before the dark castle...",
                        WINDOW_WIDTH//2, 380, (150, 255, 150), 18, anchor_x="center")

        arcade.draw_text("The Lich King's power grows stronger each day.",
                        WINDOW_WIDTH//2, 350, (150, 255, 150), 18, anchor_x="center")

        arcade.draw_text("Will you be the hero Hyrule needs?",
                        WINDOW_WIDTH//2, 320, (255, 200, 100), 18, anchor_x="center")

        # Some floating orbs
        for i in range(7):
            x = WINDOW_WIDTH//2 - 200 + i * 70
            y = 250 + math.sin(self.time * 2 + i) * 20
            arcade.draw_circle_filled(x, y, 5, (100, 255, 100))

        arcade.draw_text("Press ESC to go back",
                        WINDOW_WIDTH//2, 150, (120, 120, 120), 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu = MenuScreen()
            self.window.show_view(menu)


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
            menu = MenuScreen()
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
            menu = MenuScreen()
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
