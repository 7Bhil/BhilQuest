# BhilGame - Terminal RPG Adventure

A complete terminal-based role-playing game (RPG) built with Python. Embark on an epic adventure, battle monsters, complete quests, and explore a dangerous world!

## 🎮 Features

- **Turn-based Combat System** - Strategic battles with various enemies
- **Character Progression** - Level up, improve stats, and gain experience
- **Inventory Management** - Collect weapons, armor, potions, and quest items
- **World Exploration** - Discover different locations: forests, ruins, villages, dungeons
- **Quest System** - Complete missions given by NPCs to progress the story
- **Save/Load System** - Save your progress and continue later
- **Immersive Text Interface** - Rich descriptions and formatted terminal output

## 📁 Project Structure

```
BhilGame/
├── main.py          # Main game loop and user interface
├── character.py      # Player and enemy classes with stats
├── world.py         # World map and exploration system
├── combat.py        # Turn-based combat system
├── inventory.py     # Inventory and item management
├── story.py         # Quests, dialogues, and story progression
├── save.py          # Save and load system using JSON
└── README.md        # This file
```

## 🚀 How to Run

1. Make sure you have Python 3.6+ installed
2. Navigate to the BhilGame directory
3. Run the game:
   ```bash
   python main.py
   ```

## 🎯 How to Play

### Main Menu
- **New Game** - Start a new adventure
- **Continue Game** - Load a saved game
- **Quit** - Exit the game

### In-Game Actions
1. **Move/Travel** - Navigate between locations
2. **Explore Area** - Search for items and encounter enemies
3. **Inventory** - Manage items, use potions, equip weapons/armor
4. **Quests** - View active and available quests
5. **Talk to NPC** - Interact with non-player characters
6. **View Map** - See the world map
7. **Character Stats** - View detailed character information
8. **Save Game** - Save your progress
9. **Help** - View help information

### Combat
Combat is turn-based with the following options:
- **Attack** - Deal damage to the enemy
- **Defend** - Reduce damage from next attack
- **Use Item** - Use potions or other consumables
- **Flee** - Attempt to escape from combat

### Character Stats
- **HP (Health Points)** - Your life force
- **Attack** - Damage dealt in combat
- **Defense** - Damage reduction
- **Level** - Character progression
- **Experience** - Points toward next level

### World Locations
- **Peaceful Village** - Starting location, safe area with NPCs
- **Mystic Forest** - Dangerous forest with wolves and goblins
- **Ancient Ruins** - Mysterious ruins with skeletons and bandits
- **Dungeon** - Underground areas with orcs and dragons

## 📜 Quests

The game features several quests:

1. **Goblin Trouble** - Defeat 5 goblins to protect the village
2. **Ruins Exploration** - Find an ancient artifact in the ruins
3. **Dungeon Materials** - Collect materials from dungeon creatures
4. **Dragon Slayer** - Defeat the ancient dragon (final quest)

## 🎒 Items

### Weapons
- **Iron Sword** - Basic weapon with +8 attack
- **Steel Sword** - Superior weapon with +12 attack

### Armor
- **Iron Armor** - Basic armor with +6 defense
- **Steel Armor** - Superior armor with +10 defense

### Consumables
- **Health Potion** - Restores 30 HP
- **Large Health Potion** - Restores 60 HP
- **Attack Potion** - Temporary attack boost
- **Defense Potion** - Temporary defense boost

## 💾 Save System

The game automatically creates a `saves/` directory and stores your progress in `bhilquest_save.json`. Your save includes:
- Character stats and level
- Inventory and equipped items
- Current location and visited areas
- Quest progress and completion status
- Story progression

## 🛠️ Technical Details

### Code Architecture
- **Modular Design** - Each system is in its own module
- **Object-Oriented** - Uses classes for characters, items, locations
- **Type Hints** - Includes type annotations for better code clarity
- **Error Handling** - Robust error handling for save/load operations

### Dependencies
- Uses only Python standard library modules
- No external dependencies required
- Cross-platform compatibility (Windows, Linux, macOS)

## 🎨 Game Design

### Progression System
- Start at Level 1 with basic stats
- Gain experience by defeating enemies and completing quests
- Level up to improve stats automatically
- Find better equipment to increase combat effectiveness

### Difficulty Scaling
- Enemy difficulty increases with location danger level
- Boss enemies provide greater rewards
- Quests provide clear progression paths

## 🐛 Known Issues & Future Improvements

- Add more enemy types and behaviors
- Implement more complex quest chains
- Add character creation options (class selection)
- Implement skill system
- Add more visual elements (ASCII art)
- Sound effects support
- Multi-language support

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to contribute to the project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

---

**Enjoy your adventure in BhilGame!** 🎮✨
# BhilQuest
