"""
Module World pour BhilQuest - Version Française
Gère la carte du monde, les lieux et le système d'exploration
"""

import random
from typing import Dict, List, Tuple, Optional
from character import create_enemy


class Location:
    """Représente un lieu dans le monde du jeu"""
    
    def __init__(self, name: str, description: str, location_type: str):
        self.name = name
        self.description = description
        self.location_type = location_type  # village, forêt, donjon, ruines
        self.connections = {}  # direction -> nom_lieu
        self.npcs = []
        self.enemies = []
        self.items = []
        self.visited = False
        self.enemy_encounter_chance = 0.3
        
    def add_connection(self, direction: str, location_name: str):
        """Ajoute une connexion vers un autre lieu"""
        self.connections[direction] = location_name
    
    def add_npc(self, npc):
        """Ajoute un PNJ à ce lieu"""
        self.npcs.append(npc)
    
    def add_enemy_spawn(self, enemy_type: str, chance: float = 0.3):
        """Ajoute possibilité d'apparition d'ennemi"""
        self.enemies.append((enemy_type, chance))
        self.enemy_encounter_chance = chance
    
    def add_item(self, item):
        """Ajoute un objet qui peut être trouvé ici"""
        self.items.append(item)
    
    def get_description(self) -> str:
        """Obtient la description formatée du lieu"""
        desc = f"\n📍 {self.name}\n"
        desc += f"{'='*len(self.name)}\n"
        desc += f"{self.description}\n\n"
        
        if self.connections:
            desc += "🧭 Sorties: "
            exits = []
            for direction, location in self.connections.items():
                exits.append(f"{direction.upper()} vers {location}")
            desc += ", ".join(exits) + "\n"
        
        if self.npcs and not self.visited:
            npc_names = [npc.name for npc in self.npcs]
            desc += f"\n👥 Personnes ici: {', '.join(npc_names)}"
        
        if self.items:
            item_names = [item.name for item in self.items]
            desc += f"\n📦 Objets visibles: {', '.join(item_names)}"
        
        return desc
    
    def check_for_enemy_encounter(self) -> Optional[str]:
        """Vérifie si une rencontre d'ennemi se produit"""
        if self.enemies and random.random() < self.enemy_encounter_chance:
            enemy_type, _ = random.choice(self.enemies)
            return enemy_type
        return None


class World:
    """Classe principale du monde gérant tous les lieux et l'exploration"""
    
    def __init__(self):
        self.locations = {}
        self.current_location_name = "village"
        self.create_world()
    
    def create_world(self):
        """Crée le monde du jeu avec tous les lieux"""
        # Village - Lieu de départ
        village = Location(
            "Village Paisible",
            "Un petit village paisible entouré de palissades en bois. Vous pouvez voir quelques maisons, une forge et un puits au centre. Les villageois vaquent à leurs occupations quotidiennes, et l'atmosphère est calme et accueillante.",
            "village"
        )
        village.add_connection("nord", "foret")
        village.add_connection("est", "ruines")
        village.add_connection("ouest", "entree_donjon")
        
        # Forêt
        foret = Location(
            "Forêt Mystique",
            "Une forêt dense et ancienne avec de grands arbres qui bloquent la plupart de la lumière du soleil. L'air est épais de l'odeur de mousse et de terre humide. Vous pouvez entendre des oiseaux chanter et occasionnellement du bruit dans les buissons. Les chemins serpentent entre les arbres, mais il est facile de se perdre si on ne fait pas attention.",
            "foret"
        )
        foret.add_connection("sud", "village")
        foret.add_connection("nord", "foret_profonde")
        foret.add_connection("est", "ruines")
        foret.add_enemy_spawn("loup", 0.4)
        foret.add_enemy_spawn("gobelin", 0.3)
        
        # Forêt Profonde
        foret_profonde = Location(
            "Forêt Profonde",
            "La partie plus profonde de la forêt où les arbres sont plus anciens et les ombres plus longues. Des champignons lumineux poussent sur les troncs tombés, et vous ressentez une présence surnaturelle. Cette zone est connue pour être dangereuse, avec beaucoup de créatures qui se cachent dans l'obscurité.",
            "foret"
        )
        foret_profonde.add_connection("sud", "foret")
        foret_profonde.add_connection("nord", "passage_montagne")
        foret_profonde.add_enemy_spawn("loup", 0.5)
        foret_profonde.add_enemy_spawn("bandit", 0.3)
        foret_profonde.add_enemy_spawn("orque", 0.1)
        
        # Ruines
        ruines = Location(
            "Ruines Anciennes",
            "Les restes effondrés d'une civilisation antique. Des colonnes brisées et des structures en pierre usée parsèment le paysage. Des symboles étranges sont gravés dans les pierres, et vous pouvez sentir le poids de l'histoire en ce lieu. Les chasseurs de trésors explorent souvent ici, mais de nombreux dangers se cachent dans les ombres.",
            "ruines"
        )
        ruines.add_connection("ouest", "village")
        ruines.add_connection("sud", "foret")
        ruines.add_connection("est", "temple_abandonne")
        ruines.add_enemy_spawn("squelette", 0.4)
        ruines.add_enemy_spawn("bandit", 0.3)
        
        # Temple Abandonné
        temple_abandonne = Location(
            "Temple Abandonné",
            "Un temple sacré maintenant tombé en désuétude. Les murs en pierre sont couverts de vignes, et l'autel est fissuré et taché. Des échos étranges semblent rebondir sur les murs, et vous ressentez une présence inquiétante. Des artéfacts anciens pourraient encore être cachés à l'intérieur.",
            "ruines"
        )
        temple_abandonne.add_connection("ouest", "ruines")
        temple_abandonne.add_enemy_spawn("squelette", 0.6)
        temple_abandonne.add_enemy_spawn("orque", 0.2)
        
        # Entrée du Donjon
        entree_donjon = Location(
            "Entrée du Donjon",
            "Une entrée sombre et menaçante vers ce qui semble être un donjon souterrain. L'arche en pierre est couverte de symboles d'avertissement, et un air frais s'échappe d'en dessous. Vous pouvez entendre de l'eau qui goutte et des sons lointains et non identifiés. Seuls les braves oseraient entrer.",
            "donjon"
        )
        entree_donjon.add_connection("est", "village")
        entree_donjon.add_connection("bas", "salles_donjon")
        entree_donjon.add_enemy_spawn("gobelin", 0.3)
        entree_donjon.add_enemy_spawn("squelette", 0.2)
        
        # Salles du Donjon
        salles_donjon = Location(
            "Salles du Donjon",
            "Salles souterraines avec des murs en pierre et des corridors éclairés par des torches. L'air est humide et froid, et vos pas résonnent dans le silence. Des cellules de prison tapissent certains murs, et vous pouvez voir des preuves de batailles passées. Cet endroit est clairement dangereux.",
            "donjon"
        )
        salles_donjon.add_connection("haut", "entree_donjon")
        salles_donjon.add_connection("nord", "profondeurs_donjon")
        salles_donjon.add_enemy_spawn("squelette", 0.5)
        salles_donjon.add_enemy_spawn("orque", 0.3)
        
        # Profondeurs du Donjon
        profondeurs_donjon = Location(
            "Profondeurs du Donjon",
            "La partie la plus profonde du donjon où les créatures les plus dangereuses habitent. Les murs sont couverts de taches sombres, et vous pouvez entendre des grognements en avant. Une chambre massive s'ouvre, et au centre, vous pouvez voir le silhouette de quelque chose de grand et puissant.",
            "donjon"
        )
        profondeurs_donjon.add_connection("sud", "salles_donjon")
        profondeurs_donjon.add_enemy_spawn("orque", 0.4)
        profondeurs_donjon.add_enemy_spawn("dragon", 0.1)
        
        # Passage Montagne
        passage_montagne = Location(
            "Passage Montagneux",
            "Un chemin de montagne étroit avec des falaises abruptes des deux côtés. Le vent hurle à travers le passage, et vous pouvez voir de la neige sur les pics au-dessus. Ce chemin mène à d'autres régions, mais il est périlleux et seuls les voyageurs expérimentés devraient tenter.",
            "foret"
        )
        passage_montagne.add_connection("sud", "foret_profonde")
        passage_montagne.add_enemy_spawn("loup", 0.3)
        passage_montagne.add_enemy_spawn("orque", 0.2)
        
        # Ajoute tous les lieux au monde
        self.locations = {
            "village": village,
            "foret": foret,
            "foret_profonde": foret_profonde,
            "ruines": ruines,
            "temple_abandonne": temple_abandonne,
            "entree_donjon": entree_donjon,
            "salles_donjon": salles_donjon,
            "profondeurs_donjon": profondeurs_donjon,
            "passage_montagne": passage_montagne
        }
    
    def get_current_location(self) -> Location:
        """Obtient l'objet du lieu actuel"""
        return self.locations[self.current_location_name]
    
    def move_to_location(self, direction: str) -> Tuple[bool, str]:
        """Tente de se déplacer dans une direction"""
        current = self.get_current_location()
        
        if direction.lower() in current.connections:
            self.current_location_name = current.connections[direction.lower()]
            new_location = self.get_current_location()
            new_location.visited = True
            return True, f"Vous voyagez {direction.lower()} vers {new_location.name}"
        else:
            return False, f"Vous ne pouvez pas aller {direction.lower()} d'ici"
    
    def explore_current_location(self) -> Tuple[bool, Optional[str]]:
        """Explore le lieu actuel pour des rencontres potentielles"""
        current = self.get_current_location()
        enemy_type = current.check_for_enemy_encounter()
        
        if enemy_type:
            return True, enemy_type
        return False, None
    
    def get_available_directions(self) -> List[str]:
        """Obtient la liste des directions disponibles depuis le lieu actuel"""
        current = self.get_current_location()
        return list(current.connections.keys())
    
    def get_world_map(self) -> str:
        """Retourne une représentation textuelle simple de la carte du monde"""
        map_text = """
🗺️  CARTE DU MONDE
===============================

Village (Départ)
│
├─ Nord → Forêt Mystique
│   │
│   └─ Nord → Forêt Profonde
│       │
│       └─ Nord → Passage Montagneux
│
├─ Est → Ruines Anciennes
│   │
│   └─ Est → Temple Abandonné
│
└─ Ouest → Entrée du Donjon
    │
    └─ Bas → Salles du Donjon
        │
        └─ Nord → Profondeurs du Donjon

Lieu Actuel: {}
                """.format(self.current_location_name.replace("_", " ").title())
        return map_text
    
    def get_location_info(self) -> str:
        """Obtient des informations détaillées sur le lieu actuel"""
        current = self.get_current_location()
        info = current.get_description()
        
        # Ajoute un indicateur de niveau de danger
        danger_level = "🟢 Sûr"
        if current.enemy_encounter_chance > 0.4:
            danger_level = "🔴 Dangereux"
        elif current.enemy_encounter_chance > 0.2:
            danger_level = "🟡 Modéré"
        
        info += f"\n⚠️  Niveau de Danger: {danger_level}"
        return info
