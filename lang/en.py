"""
English Language Pack for BhilQuest
All text strings in English
"""

# Game Title and Branding
GAME_TITLE = "BHILQUEST"
GAME_SUBTITLE = "A Terminal RPG Adventure"
CREATED_BY = "Created by: Bhilal CHITOU (Bhil€)"
EMAIL_CONTACT = "Email: 7bhilal.chitou7@gmail.com"
GITHUB_LINK = "GitHub: https://github.com/7Bhil"

# Main Menu
MAIN_MENU_TITLE = "MAIN MENU"
NEW_GAME = "New Game"
CONTINUE_GAME = "Continue Game"
QUIT_GAME = "Quit"
NO_SAVE_FOUND = "No save file found"
CHOOSE_OPTION = "Choose your option (1-3):"
INVALID_CHOICE = "Invalid choice! Please enter 1-3."

# Character Creation
CHARACTER_CREATION = "CHARACTER CREATION"
ENTER_NAME = "Enter your character's name:"
VALID_NAME = "Please enter a valid name (1-20 characters)"
WELCOME_MESSAGE = "Welcome, {name}! Your adventure begins now..."
PRESS_ENTER = "Press Enter to continue..."
HERO_AWAKENS = "{name} the hero awakens in the peaceful village!"

# Game Actions
WHAT_DO = "What would you like to do?"
MOVE_TRAVEL = "Move/Travel"
EXPLORE_AREA = "Explore Area"
INVENTORY = "Inventory"
QUESTS = "Quests"
TALK_NPC = "Talk to NPC"
VIEW_MAP = "View Map"
CHARACTER_STATS = "Character Stats"
SAVE_GAME = "Save Game"
HELP = "Help"
QUIT = "Quit Game"
ENTER_CHOICE = "Enter your choice (0-9):"

# Movement
AVAILABLE_DIRECTIONS = "Available directions:"
CHOOSE_DIRECTION = "Choose direction (1-{count}):"
TRAVEL_SUCCESS = "You travel {direction} to {location}"
CANNOT_GO = "You cannot go {direction} from here"
NO_EXITS = "There are no exits from this location!"
INVALID_DIRECTION = "Invalid direction!"
ENTER_NUMBER = "Please enter a valid number!"

# Exploration
EXPLORING = "Exploring {location}..."
FOUND_ITEM = "You found: {item_name}"
ITEM_ADDED = "Item added to inventory!"
INVENTORY_FULL = "Inventory full! Cannot pick up item."
NOTHING_FOUND = "You explore the area but find nothing of interest."

# Combat
ENEMY_APPEARS = "A wild {enemy_name} appears!"
START_COMBAT = "Press Enter to start combat..."
COMBAT_BEGINS = "COMBAT BEGINS!"
PLAYER_TURN = "{player_name}'s Turn:"
ATTACK = "Attack"
DEFEND = "Defend"
USE_ITEM = "Use Item"
FLEE = "Flee"
CHOOSE_ACTION = "Choose your action (1-4):"
INVALID_ACTION = "Invalid choice! Please enter 1-4."
ATTACKS_FOR = "attacks {target} for {damage} damage!"
TAKES_DAMAGE = "{target} takes {damage} damage!"
IS_DEFENDING = "{target} is defending! Damage reduced!"
DEFENSIVE_STANCE = "takes a defensive stance!"
FAILED_TO_FLEE = "failed to flee!"
SUCCESSFULLY_FLED = "successfully fled from combat!"
TOO_MANY_ATTEMPTS = "You've attempted to flee too many times! You must fight!"
USE_CONSUMABLE = "Use consumable items"
NO_CONSUMABLES = "No consumable items available!"
CHOOSE_ITEM_USE = "Choose item to use (or 0 to cancel):"
CANNOT_USE_ITEM = "Cannot use this item!"
INVALID_ITEM = "Invalid item number!"
VICTORY = "VICTORY!"
DEFEATED_ENEMY = "{player_name} has defeated {enemy_name}!"
GAINED_EXP = "Gained {exp} EXP!"
DROPPED = "{enemy_name} dropped:"
CANNOT_PICKUP = "Inventory full! Cannot pick up {item_name}."
DEFEAT = "DEFEAT!"
DEFEATED_BY = "{player_name} has been defeated by {enemy_name}!"
LOST_BATTLE = "You have lost the battle..."

# Inventory
INVENTORY_DISPLAY = "INVENTORY"
INVENTORY_EMPTY = "Your inventory is empty"
SLOTS = "Slots"
AVAILABLE_QUESTS = "AVAILABLE QUESTS"
ACTIVE_QUESTS = "ACTIVE QUESTS"
USE_ITEM_OPTION = "Use Item"
EQUIP_OPTION = "Equip Weapon/Armor"
BACK_GAME = "Back to game"
CONSUMABLE_ITEMS = "Consumable Items"
CHOOSE_ITEM_EQUIP = "Choose item to equip (0 to cancel):"
EQUIPMENT = "Equipment"
NO_EQUIPMENT = "No equipment available!"
USED_ITEM = "Used {item_name}!"

# Quests
QUEST_COMPLETED = "QUEST COMPLETED"
QUEST_REWARDS = "Rewards"
QUEST_OFFER = "Quest Offer"
QUEST_PROGRESS = "Progress"
ACCEPT_QUEST = "Accept this quest? (y/n):"
QUEST_ACCEPTED = "Perhaps another time then..."
NO_AVAILABLE_QUESTS = "No save file to delete!"

# NPCs
TALK_TO = "Who would you like to talk to?"
CHOOSE_PERSON = "Choose person (0 to cancel):"
INVALID_PERSON = "Invalid person!"
NO_ONE_TALK = "There's no one to talk to here!"
CONVERSATION_WITH = "Conversation with {npc_name}"
DESCRIPTION = "{npc_name}: {description}"
GREETING = "{npc_name}: {dialogue}"
PERHAPS_ANOTHER_TIME = "Perhaps another time then..."

# Map and Stats
WORLD_MAP = "WORLD MAP"
CURRENT_LOCATION = "Current Location"
PRESS_ENTER_CONTINUE = "Press Enter to continue..."

# Save System
SAVE_SUCCESS = "Game saved successfully!"
SAVE_FAILED = "Failed to save game!"
LOAD_SUCCESS = "Game loaded successfully! (Saved: {timestamp})"
LOAD_FAILED = "Failed to load game: {error}"
SAVE_FILE_INFO = "SAVE FILE INFO"
PLAYER_NAME = "Player"
LEVEL = "Level"
LOCATION = "Location"
QUESTS_COMPLETED = "Quests Completed"
SAVED = "Saved"
NO_SAVE_FILE = "No save file found!"

# Game Over
GAME_OVER_TITLE = "GAME OVER"
HAS_FALLEN = "{name} has fallen in battle..."
FINAL_STATS = "Final Stats"
QUESTS_COMPLETED_STAT = "Quests Completed"
LOCATIONS_VISITED = "Locations Visited"
RETURN_MENU = "Press Enter to return to main menu..."

# Help System
HELP_GUIDE = "HELP GUIDE"
MOVEMENT_SECTION = "MOVEMENT"
MOVEMENT_TEXT = "• Use the Move option to travel between locations\n• Choose from available directions (N, S, E, W, etc.)"
COMBAT_SECTION = "COMBAT"
COMBAT_TEXT = "• Combat is turn-based and happens automatically during exploration\n• Choose actions: Attack, Defend, Use Item, or Flee\n• Different enemies have different difficulty levels"
INVENTORY_SECTION = "INVENTORY"
INVENTORY_TEXT = "• Manage your items through the Inventory menu\n• Use consumables like health potions\n• Equip weapons and armor to improve stats"
QUESTS_SECTION = "QUESTS"
QUESTS_TEXT = "• Talk to NPCs to receive quests\n• Complete quests by meeting requirements\n• Earn experience and rewards for completed quests"
EXPLORATION_SECTION = "EXPLORATION"
EXPLORATION_TEXT = "• Explore areas to find items and encounter enemies\n• Different locations have different dangers and rewards\n• Visit all locations to discover the world"
TIPS_SECTION = "TIPS"
TIPS_TEXT = "• Save your game progress regularly\n• Stock up on healing potions before dangerous areas\n• Complete quests to gain experience and rewards\n• Explore thoroughly to find valuable items"
GOOD_LUCK = "Good luck, hero!"

# Quit Game
SURE_QUIT = "Are you sure you want to quit?"
SAVE_AND_QUIT = "Save and Quit"
QUIT_WITHOUT_SAVING = "Quit without Saving"
CANCEL = "Cancel"
CHOOSE_OPTION_QUIT = "Choose option (1-3):"

# Messages
THANKS_PLAYING = "Thanks for playing BhilQuest!"
ERROR_OCCURRED = "An error occurred: {error}"

# Location Names
VILLAGE = "Peaceful Village"
MYSTIC_FOREST = "Mystic Forest"
DEEP_FOREST = "Deep Forest"
ANCIENT_RUINS = "Ancient Ruins"
ABANDONED_TEMPLE = "Abandoned Temple"
DUNGEON_ENTRANCE = "Dungeon Entrance"
DUNGEON_HALLS = "Dungeon Halls"
DUNGEON_DEPTHS = "Dungeon Depths"
MOUNTAIN_PASS = "Mountain Pass"

# Location Descriptions
VILLAGE_DESC = "A small, peaceful village surrounded by wooden palisades. You can see a few houses, a blacksmith shop, and a well in the center. The villagers go about their daily routines, and the atmosphere is calm and welcoming."
FOREST_DESC = "A dense, ancient forest with tall trees that block out most sunlight. The air is thick with the smell of moss and damp earth. You can hear birds chirping and occasionally rustling in the bushes. Pathways wind between the trees, but it's easy to get lost if you're not careful."
DEEP_FOREST_DESC = "The deeper part of the forest where the trees are older and the shadows are longer. Strange glowing mushrooms grow on fallen logs, and you feel an otherworldly presence. This area is known to be dangerous, with many creatures lurking in the darkness."
RUINS_DESC = "The crumbling remains of an ancient civilization. Broken columns and weathered stone structures dot the landscape. Strange symbols are carved into the stones, and you can feel the weight of history in this place. Treasure hunters often explore here, but many dangers lurk in the shadows."
TEMPLE_DESC = "A once-sacred temple now fallen into disrepair. The stone walls are covered in vines, and the altar is cracked and stained. Strange echoes seem to bounce off the walls, and you feel an unsettling presence. Ancient artifacts might still be hidden within."
DUNGEON_ENTRANCE_DESC = "A dark, foreboding entrance to what appears to be an underground dungeon. The stone archway is covered in warning symbols, and cold air wafts up from below. You can hear dripping water and distant, unidentifiable sounds. Only the brave would dare enter."
DUNGEON_HALLS_DESC = "Underground halls with stone walls and torch-lit corridors. The air is damp and cold, and your footsteps echo in the silence. Prison cells line some walls, and you can see evidence of past battles. This place is clearly dangerous."
DUNGEON_DEPTHS_DESC = "The deepest part of the dungeon where the most dangerous creatures dwell. The walls are covered in dark stains, and you can hear growling from ahead. A massive chamber opens up, and in the center, you can see the silhouette of something large and powerful."
MOUNTAIN_PASS_DESC = "A narrow mountain path with steep cliffs on both sides. The wind howls through the pass, and you can see snow on the peaks above. This path connects to other regions, but it's treacherous and only experienced travelers should attempt it."

# Directions
NORTH = "NORTH"
SOUTH = "SOUTH"
EAST = "EAST"
WEST = "WEST"
UP = "UP"
DOWN = "DOWN"

# Navigation
EXITS = "Exits"
TO = "to"
PEOPLE_HERE = "People here"
ITEMS_VISIBLE = "Items visible"

# Danger Levels
DANGER_LEVEL = "Danger Level"
SAFE = "Safe"
MODERATE = "Moderate"
DANGEROUS = "Dangerous"

# Story Messages
NEW_ADVENTURER = "You are a new adventurer, ready to prove your worth."
TASTED_COMBAT = "You have tasted combat and survived. The path of a hero opens before you."
CAPABLE_WARRIOR = "You have proven yourself as a capable warrior. Greater challenges await."
TRUE_HERO = "You are a true hero of the realm! The dragon is defeated and peace restored."
LEGEND_GROWS = "Your legend continues to grow..."

# NPC Names
ELDER_MARCUS = "Village Elder Marcus"
BLACKSMITH_THORIN = "Blacksmith Thorin"
MYSTERIOUS_STRANGER = "Mysterious Stranger"

# NPC Descriptions
ELDER_DESC = "A wise old man with a long white beard and kind eyes. He has lived in the village his entire life and knows many secrets."
BLACKSMITH_DESC = "A muscular dwarf with a thick beard and soot-covered hands. He's always working at his forge."
STRANGER_DESC = "A hooded figure with an air of mystery about them. Their face is hidden in shadow."

# Quest Names
GOBLIN_TROUBLE = "Goblin Trouble"
RUINS_EXPLORATION = "Ruins Exploration"
DUNGEON_MATERIALS = "Dungeon Materials"
DRAGON_SLAYER = "Dragon Slayer"

# Quest Descriptions
GOBLIN_TROUBLE_DESC = "The village is being raided by goblins. Help us by defeating 5 goblins to make our village safe again."
RUINS_EXPLORATION_DESC = "Explore the ancient ruins and find the mysterious artifact that the stranger seeks."
DUNGEON_MATERIALS_DESC = "Venture into the dungeon depths and collect rare materials for the blacksmith."
DRAGON_SLAYER_DESC = "The ancient dragon in the dungeon depths threatens the entire realm. You must defeat it!"

# Quest Progress
DEFEAT_GOBLINS = "Defeat goblins: {current}/{required}"
OBTAIN_ARTIFACT = "Obtain ancient_artifact: {status}"
COLLECT_MATERIALS = "Defeat skeletons: {current}/{required}"
DEFEAT_DRAGON = "Defeat dragon: {current}/{required}"

# Status Indicators
CHECK = "✓"
CROSS = "✗"
