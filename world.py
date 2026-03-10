"""
World module for BhilGame
Handles world map, locations, and exploration system
"""

import random
from typing import Dict, List, Tuple, Optional
from character import create_enemy


class Location:
    """Represents a location in the game world"""
    
    def __init__(self, name: str, description: str, location_type: str):
        self.name = name
        self.description = description
        self.location_type = location_type  # village, forest, dungeon, ruins
        self.connections = {}  # direction -> location_name
        self.npcs = []
        self.enemies = []
        self.items = []
        self.visited = False
        self.enemy_encounter_chance = 0.3
        
    def add_connection(self, direction: str, location_name: str):
        """Add a connection to another location"""
        self.connections[direction] = location_name
    
    def add_npc(self, npc):
        """Add an NPC to this location"""
        self.npcs.append(npc)
    
    def add_enemy_spawn(self, enemy_type: str, chance: float = 0.3):
        """Add enemy spawn possibility"""
        self.enemies.append((enemy_type, chance))
        self.enemy_encounter_chance = chance
    
    def add_item(self, item):
        """Add an item that can be found here"""
        self.items.append(item)
    
    def get_description(self) -> str:
        """Get formatted description of location"""
        desc = f"\n📍 {self.name}\n"
        desc += f"{'='*len(self.name)}\n"
        desc += f"{self.description}\n\n"
        
        if self.connections:
            desc += "🧭 Exits: "
            exits = []
            for direction, location in self.connections.items():
                exits.append(f"{direction.upper()} to {location}")
            desc += ", ".join(exits) + "\n"
        
        if self.npcs and not self.visited:
            npc_names = [npc.name for npc in self.npcs]
            desc += f"\n👥 People here: {', '.join(npc_names)}"
        
        if self.items:
            item_names = [item.name for item in self.items]
            desc += f"\n📦 Items visible: {', '.join(item_names)}"
        
        return desc
    
    def check_for_enemy_encounter(self) -> Optional[str]:
        """Check if enemy encounter happens"""
        if self.enemies and random.random() < self.enemy_encounter_chance:
            enemy_type, _ = random.choice(self.enemies)
            return enemy_type
        return None


class World:
    """Main world class managing all locations and exploration"""
    
    def __init__(self):
        self.locations = {}
        self.current_location_name = "village"
        self.create_world()
    
    def create_world(self):
        """Create the game world with all locations"""
        # Village - Starting location
        village = Location(
            "Peaceful Village",
            "A small, peaceful village surrounded by wooden palisades. You can see a few houses, a blacksmith shop, and a well in the center. The villagers go about their daily routines, and the atmosphere is calm and welcoming.",
            "village"
        )
        village.add_connection("north", "forest")
        village.add_connection("east", "ruins")
        village.add_connection("west", "dungeon_entrance")
        
        # Forest
        forest = Location(
            "Mystic Forest",
            "A dense, ancient forest with tall trees that block out most sunlight. The air is thick with the smell of moss and damp earth. You can hear birds chirping and occasionally rustling in the bushes. Pathways wind between the trees, but it's easy to get lost if you're not careful.",
            "forest"
        )
        forest.add_connection("south", "village")
        forest.add_connection("north", "deep_forest")
        forest.add_connection("east", "ruins")
        forest.add_enemy_spawn("wolf", 0.4)
        forest.add_enemy_spawn("goblin", 0.3)
        
        # Deep Forest
        deep_forest = Location(
            "Deep Forest",
            "The deeper part of the forest where the trees are older and the shadows are longer. Strange glowing mushrooms grow on fallen logs, and you feel an otherworldly presence. This area is known to be dangerous, with many creatures lurking in the darkness.",
            "forest"
        )
        deep_forest.add_connection("south", "forest")
        deep_forest.add_connection("north", "mountain_pass")
        deep_forest.add_enemy_spawn("wolf", 0.5)
        deep_forest.add_enemy_spawn("bandit", 0.3)
        deep_forest.add_enemy_spawn("orc", 0.1)
        
        # Ruins
        ruins = Location(
            "Ancient Ruins",
            "The crumbling remains of an ancient civilization. Broken columns and weathered stone structures dot the landscape. Strange symbols are carved into the stones, and you can feel the weight of history in this place. Treasure hunters often explore here, but many dangers lurk in the shadows.",
            "ruins"
        )
        ruins.add_connection("west", "village")
        ruins.add_connection("south", "forest")
        ruins.add_connection("east", "abandoned_temple")
        ruins.add_enemy_spawn("skeleton", 0.4)
        ruins.add_enemy_spawn("bandit", 0.3)
        
        # Abandoned Temple
        abandoned_temple = Location(
            "Abandoned Temple",
            "A once-sacred temple now fallen into disrepair. The stone walls are covered in vines, and the altar is cracked and stained. Strange echoes seem to bounce off the walls, and you feel an unsettling presence. Ancient artifacts might still be hidden within.",
            "ruins"
        )
        abandoned_temple.add_connection("west", "ruins")
        abandoned_temple.add_enemy_spawn("skeleton", 0.6)
        abandoned_temple.add_enemy_spawn("orc", 0.2)
        
        # Dungeon Entrance
        dungeon_entrance = Location(
            "Dungeon Entrance",
            "A dark, foreboding entrance to what appears to be an underground dungeon. The stone archway is covered in warning symbols, and cold air wafts up from below. You can hear dripping water and distant, unidentifiable sounds. Only the brave would dare enter.",
            "dungeon"
        )
        dungeon_entrance.add_connection("east", "village")
        dungeon_entrance.add_connection("down", "dungeon_halls")
        dungeon_entrance.add_enemy_spawn("goblin", 0.3)
        dungeon_entrance.add_enemy_spawn("skeleton", 0.2)
        
        # Dungeon Halls
        dungeon_halls = Location(
            "Dungeon Halls",
            "Underground halls with stone walls and torch-lit corridors. The air is damp and cold, and your footsteps echo in the silence. Prison cells line some walls, and you can see evidence of past battles. This place is clearly dangerous.",
            "dungeon"
        )
        dungeon_halls.add_connection("up", "dungeon_entrance")
        dungeon_halls.add_connection("north", "dungeon_depths")
        dungeon_halls.add_enemy_spawn("skeleton", 0.5)
        dungeon_halls.add_enemy_spawn("orc", 0.3)
        
        # Dungeon Depths
        dungeon_depths = Location(
            "Dungeon Depths",
            "The deepest part of the dungeon where the most dangerous creatures dwell. The walls are covered in dark stains, and you can hear growling from ahead. A massive chamber opens up, and in the center, you can see the silhouette of something large and powerful.",
            "dungeon"
        )
        dungeon_depths.add_connection("south", "dungeon_halls")
        dungeon_depths.add_enemy_spawn("orc", 0.4)
        dungeon_depths.add_enemy_spawn("dragon", 0.1)
        
        # Mountain Pass
        mountain_pass = Location(
            "Mountain Pass",
            "A narrow mountain path with steep cliffs on both sides. The wind howls through the pass, and you can see snow on the peaks above. This path connects to other regions, but it's treacherous and only experienced travelers should attempt it.",
            "forest"
        )
        mountain_pass.add_connection("south", "deep_forest")
        mountain_pass.add_enemy_spawn("wolf", 0.3)
        mountain_pass.add_enemy_spawn("orc", 0.2)
        
        # Add all locations to the world
        self.locations = {
            "village": village,
            "forest": forest,
            "deep_forest": deep_forest,
            "ruins": ruins,
            "abandoned_temple": abandoned_temple,
            "dungeon_entrance": dungeon_entrance,
            "dungeon_halls": dungeon_halls,
            "dungeon_depths": dungeon_depths,
            "mountain_pass": mountain_pass
        }
    
    def get_current_location(self) -> Location:
        """Get the current location object"""
        return self.locations[self.current_location_name]
    
    def move_to_location(self, direction: str) -> Tuple[bool, str]:
        """Attempt to move in a direction"""
        current = self.get_current_location()
        
        if direction.lower() in current.connections:
            self.current_location_name = current.connections[direction.lower()]
            new_location = self.get_current_location()
            new_location.visited = True
            return True, f"You travel {direction.lower()} to {new_location.name}"
        else:
            return False, f"You cannot go {direction.lower()} from here"
    
    def explore_current_location(self) -> Tuple[bool, Optional[str]]:
        """Explore current location for potential encounters"""
        current = self.get_current_location()
        enemy_type = current.check_for_enemy_encounter()
        
        if enemy_type:
            return True, enemy_type
        return False, None
    
    def get_available_directions(self) -> List[str]:
        """Get list of available directions from current location"""
        current = self.get_current_location()
        return list(current.connections.keys())
    
    def get_world_map(self) -> str:
        """Return a simple text representation of the world map"""
        map_text = """
🗺️  WORLD MAP
================

Village (Start)
│
├─ North → Mystic Forest
│   │
│   └─ North → Deep Forest
│       │
│       └─ North → Mountain Pass
│
├─ East → Ancient Ruins
│   │
│   └─ East → Abandoned Temple
│
└─ West → Dungeon Entrance
    │
    └─ Down → Dungeon Halls
        │
        └─ North → Dungeon Depths

Current Location: {}
        """.format(self.current_location_name.replace("_", " ").title())
        return map_text
    
    def get_location_info(self) -> str:
        """Get detailed information about current location"""
        current = self.get_current_location()
        info = current.get_description()
        
        # Add danger level indicator
        danger_level = "🟢 Safe"
        if current.enemy_encounter_chance > 0.4:
            danger_level = "🔴 Dangerous"
        elif current.enemy_encounter_chance > 0.2:
            danger_level = "🟡 Moderate"
        
        info += f"\n⚠️  Danger Level: {danger_level}"
        return info
