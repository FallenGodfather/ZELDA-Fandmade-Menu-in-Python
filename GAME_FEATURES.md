# Zelda The Lich King Tales - First Level Features

## Game Overview
A complete playable first level featuring Link's adventure on a deserted island.

## Story
Link opens his eyes on a mysterious deserted island. An old man named Jude approaches and explains that the Lich King's curse has brought Link here. To escape and continue his quest, Link must find the sacred Chalice hidden in the Old Palace to the northeast. But the path is treacherous - dark creatures patrol the island, and a mighty King Kong-like beast guards the palace!

## Controls
- **WASD / Arrow Keys**: Move Link in all directions
- **SPACE**: Attack enemies / Talk to NPCs
- **ESC**: Return to main menu

## Gameplay Features

### Player (Link)
- Health: 100 HP
- Attack Damage: 10
- Movement Speed: 200 units/sec
- Attack cooldown: 0.5 seconds
- Invincibility frames after taking damage
- Visual feedback when attacking (sword animation)
- Directional facing based on movement

### NPCs
- **Jude**: Old guide located near spawn point
- 6 dialogue lines explaining the quest
- Interact with SPACE when nearby

### Enemies

**Mobs (5 total):**
- Health: 30 HP each
- Damage: 5 per hit
- Patrol behavior when idle
- Chase behavior when player is nearby (150 unit range)
- Patrol range: 100 units from spawn point

**Boss (Palace Guardian):**
- Health: 200 HP
- Damage: 15 per hit
- King Kong-like appearance (large brown ape)
- Slower movement but higher damage
- Spawns only after collecting the Chalice
- Health bar displayed above boss

### Level Design
- **Island Size**: 1400 x 800 units
- **Player View**: Scrolling camera follows Link
- **Boundaries**: Stone walls around entire island
- **Old Palace**: Located in northeast corner (stone structure)
- **Terrain**: Sandy beach with color variations
- **Water**: Surrounding ocean with wave effects
- **Environment**: 5 palm trees for atmosphere

### Objectives
1. Talk to Jude to learn about the quest
2. Navigate through the island avoiding/fighting mobs
3. Reach the Old Palace in the northeast
4. Collect the golden Chalice
5. Defeat the Palace Guardian boss
6. Victory!

### Visual Effects
- **Particle System**: 
  - Hit effects when attacking enemies
  - Death particles when enemies are defeated
  - Damage particles when player takes damage
  - Celebration particles when collecting chalice
- **Chalice Glow**: Multiple animated glow layers
- **Health Bar**: Color changes based on health (green > yellow > red)
- **Boss Health Bar**: Prominent display during boss fight
- **Invincibility Flash**: Player flashes when invincible
- **Water Waves**: Animated wave effect around island

### Game States
- **Intro**: Opening dialogue sequence
- **Playing**: Active gameplay
- **Dialogue**: Conversation with NPCs (pauses game)
- **Win**: Victory screen after defeating boss
- **Lose**: Game over screen if health reaches 0

### UI Elements
- Health bar (top left)
- Objective text (top center)
- Controls reminder (bottom center)
- Dialogue box (bottom, when active)
- NPC interaction prompt
- Boss label and health bar

## Technical Details

### Classes
- **Player**: Link character with combat and movement
- **Enemy**: Mob and boss enemy types
- **NPC**: Non-player characters with dialogue
- **Particle**: Visual effect particles
- **GameScreen**: Main game view with all logic

### Collision Detection
- Wall collision prevents movement through obstacles
- Enemy collision deals damage to player
- Attack range collision for combat
- Proximity detection for NPC interaction
- Collection radius for chalice

### Camera System
- Follows player smoothly
- Clamped to world boundaries
- All objects offset by camera position when drawing

## Art Style
16-bit inspired with simple geometric shapes:
- Characters: Rectangles and circles
- Link: Green with blue shield, golden hat
- Enemies: Red/brown rectangles with simple faces
- Boss: Large brown with detailed features (arms, face)
- Environment: Colored rectangles for walls and terrain
- Effects: Colored particles

## Win Condition
Defeat the Palace Guardian boss (reduce its health to 0)

## Lose Condition
Player health reaches 0

## Future Expansion Possibilities
- More levels
- Additional enemy types
- Power-ups and collectibles
- More bosses
- Save system
- Sound effects
- Better animations
- Inventory system
