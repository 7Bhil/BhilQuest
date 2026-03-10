"""
Module Monde pour BhilQuest
Gère la carte du monde, les lieux et le système d'exploration
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
            desc += "🧭 Sorties : "
            exits = []
            for direction, location in self.connections.items():
                exits.append(f"{direction.upper()} vers {location}")
            desc += ", ".join(exits) + "\n"
        
        if self.npcs and not self.visited:
            npc_names = [npc.name for npc in self.npcs]
            desc += f"\n👥 Personnes ici : {', '.join(npc_names)}"
        
        if self.items:
            item_names = [item.name for item in self.items]
            desc += f"\n📦 Objets visibles : {', '.join(item_names)}"
        
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
            "Village Paisible",
            "Un petit village paisible entouré de palissades en bois. Vous pouvez voir quelques maisons, une forge et un puits au centre. Les villageois vaquent à leurs occupations quotidiennes, et l'atmosphère est calme et accueillante.",
            "village"
        )
        village.add_connection("nord", "forest")
        village.add_connection("est", "ruins")
        village.add_connection("ouest", "dungeon_entrance")
        
        # Forest
        forest = Location(
            "Forêt Mystique",
            "Une forêt dense et ancienne avec de grands arbres qui bloquent la majeure partie de la lumière du soleil. L'air est chargé de l'odeur de mousse et de terre humide. Vous entendez des oiseaux gazouiller et parfois des bruits dans les buissons.",
            "forest"
        )
        forest.add_connection("sud", "village")
        forest.add_connection("nord", "deep_forest")
        forest.add_connection("est", "ruins")
        forest.add_enemy_spawn("wolf", 0.4)
        forest.add_enemy_spawn("goblin", 0.3)
        
        # Deep Forest
        deep_forest = Location(
            "Forêt Profonde",
            "La partie la plus profonde de la forêt où les arbres sont plus vieux et les ombres plus longues. Des champignons luisants poussent sur les troncs tombés. Cette zone est réputée dangereuse.",
            "forest"
        )
        deep_forest.add_connection("sud", "forest")
        deep_forest.add_connection("nord", "mountain_pass")
        deep_forest.add_enemy_spawn("wolf", 0.5)
        deep_forest.add_enemy_spawn("bandit", 0.3)
        deep_forest.add_enemy_spawn("orc", 0.1)
        
        # Ruins
        ruins = Location(
            "Ruines Antiques",
            "Les restes s'effondrant d'une ancienne civilisation. Des colonnes brisées et des structures en pierre érodées parsèment le paysage. Des symboles étranges sont gravés dans la pierre.",
            "ruins"
        )
        ruins.add_connection("ouest", "village")
        ruins.add_connection("sud", "forest")
        ruins.add_connection("est", "abandoned_temple")
        ruins.add_enemy_spawn("skeleton", 0.4)
        ruins.add_enemy_spawn("bandit", 0.3)
        
        # Abandoned Temple
        abandoned_temple = Location(
            "Temple Abandonné",
            "Un temple autrefois sacré, aujourd'hui tombé en désuétude. Les murs en pierre sont couverts de lierre et l'autel est fissuré. Des échos étranges semblent rebondir sur les murs.",
            "ruins"
        )
        abandoned_temple.add_connection("ouest", "ruins")
        abandoned_temple.add_enemy_spawn("skeleton", 0.6)
        abandoned_temple.add_enemy_spawn("orc", 0.2)
        
        # Dungeon Entrance
        dungeon_entrance = Location(
            "Entrée du Donjon",
            "Une entrée sombre et menaçante vers ce qui semble être un donjon souterrain. L'arche en pierre est couverte de symboles d'avertissement. Seuls les braves oseraient entrer.",
            "dungeon"
        )
        dungeon_entrance.add_connection("est", "village")
        dungeon_entrance.add_connection("bas", "dungeon_halls")
        dungeon_entrance.add_enemy_spawn("goblin", 0.3)
        dungeon_entrance.add_enemy_spawn("skeleton", 0.2)
        
        # Dungeon Halls
        dungeon_halls = Location(
            "Couloirs du Donjon",
            "Des salles souterraines avec des murs en pierre et des couloirs éclairés à la torche. L'air est humide et froid, et vos pas résonnent dans le silence.",
            "dungeon"
        )
        dungeon_halls.add_connection("haut", "dungeon_entrance")
        dungeon_halls.add_connection("nord", "dungeon_depths")
        dungeon_halls.add_enemy_spawn("skeleton", 0.5)
        dungeon_halls.add_enemy_spawn("orc", 0.3)
        
        # Dungeon Depths
        dungeon_depths = Location(
            "Profondeurs du Donjon",
            "La partie la plus profonde du donjon où résident les créatures les plus dangereuses. Un vaste hall s'ouvre, et au centre, vous voyez une silhouette massive et puissante.",
            "dungeon"
        )
        dungeon_depths.add_connection("sud", "dungeon_halls")
        dungeon_depths.add_enemy_spawn("orc", 0.4)
        dungeon_depths.add_enemy_spawn("dragon", 0.1)
        
        # Mountain Pass
        mountain_pass = Location(
            "Col de la Montagne",
            "Un sentier de montagne étroit avec des falaises abruptes des deux côtés. Le vent hurle à travers le col, et vous pouvez voir de la neige sur les sommets au-dessus.",
            "forest"
        )
        mountain_pass.add_connection("sud", "deep_forest")
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
            return True, f"Vous voyagez vers le {direction.lower()} jusqu'à : {new_location.name}"
        else:
            return False, f"Vous ne pouvez pas aller vers le {direction.lower()} depuis ici"
    
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
🗺️  CARTE DU MONDE
================

Village (Départ)
│
├─ Nord → Forêt Mystique
│   │
│   └─ Nord → Forêt Profonde
│       │
│       └─ Nord → Col de la Montagne
│
├─ Est → Ruines Antiques
│   │
│   └─ Est → Temple Abandonné
│
└─ Ouest → Entrée du Donjon
    │
    └─ Bas → Couloirs du Donjon
        │
        └─ Nord → Profondeurs du Donjon

Lieu Actuel : {}
        """.format(self.get_current_location().name)
        return map_text
    
    def get_location_info(self) -> str:
        """Get detailed information about current location"""
        current = self.get_current_location()
        info = current.get_description()
        
        # Add danger level indicator
        danger_level = "🟢 Sûr"
        if current.enemy_encounter_chance > 0.4:
            danger_level = "🔴 Dangereux"
        elif current.enemy_encounter_chance > 0.2:
            danger_level = "🟡 Modéré"
        
        info += f"\n⚠️  Niveau de Danger : {danger_level}"
        return info
