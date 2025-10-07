# Create a simple run script
run_script = '''#!/usr/bin/env python3
# Quick launcher for my Zelda game
# Just run this if you don't want to type the full command

import os
import sys

print("🎮 Launching Zelda The Lich King Tales...")
print("Made by FallenGodfather")
print()

# Check if the main game file exists
if not os.path.exists("my_zelda_game.py"):
    print("❌ Oops! Can't find my_zelda_game.py")
    print("Make sure you're in the right folder!")
    sys.exit(1)

# Check for background image
if os.path.exists("generated_image.png"):
    print("✅ Found background image")
else:
    print("⚠️ No background image found (will use default)")

# Check for music
if os.path.exists("gerudo_valley.wav"):
    print("✅ Found music file")
else:
    print("⚠️ No music file found (will be silent)")

print()
print("Starting game...")

# Import and run the game
try:
    from my_zelda_game import main
    main()
except ImportError:
    print("❌ Missing arcade library!")
    print("Install with: pip install arcade")
except KeyboardInterrupt:
    print("\\nThanks for playing!")
except Exception as e:
    print(f"❌ Something went wrong: {e}")
'''

# Save run script
with open("run_game.py", "w") as f:
    f.write(run_script)

print("✅ RUN SCRIPT CREATED!")
print("📁 File: run_game.py")