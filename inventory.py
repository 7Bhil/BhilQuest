"""
Inventory module for BhilGame
Handles items, equipment, and inventory management
"""

from typing import List, Dict, Optional
from character import Player


class Item:
    """Base class for all items"""
    
    def __init__(self, name: str, description: str, item_type: str, value: int = 10):
        self.name = name
        self.description = description
        self.item_type = item_type  # weapon, armor, consumable, quest
        self.value = value
        self.stackable = False
        self.quantity = 1
    
    def use(self, player: Player) -> bool:
        """Use the item, return True if item should be consumed"""
        return False
    
    def get_info(self) -> str:
        """Get formatted item information"""
        return f"{self.name} - {self.description}"


class Weapon(Item):
    """Weapon class that provides attack bonus"""
    
    def __init__(self, name: str, description: str, attack_bonus: int, value: int = 50):
        super().__init__(name, description, "weapon", value)
        self.attack_bonus = attack_bonus
        self.stackable = False
    
    def get_info(self) -> str:
        return f"⚔️  {self.name} - ATK +{self.attack_bonus} - {self.description}"


class Armor(Item):
    """Armor class that provides defense bonus"""
    
    def __init__(self, name: str, description: str, defense_bonus: int, value: int = 40):
        super().__init__(name, description, "armor", value)
        self.defense_bonus = defense_bonus
        self.stackable = False
    
    def get_info(self) -> str:
        return f"🛡️  {self.name} - DEF +{self.defense_bonus} - {self.description}"


class Consumable(Item):
    """Consumable items like potions"""
    
    def __init__(self, name: str, description: str, effect_type: str, effect_value: int, value: int = 20):
        super().__init__(name, description, "consumable", value)
        self.effect_type = effect_type  # heal, buff, etc.
        self.effect_value = effect_value
        self.stackable = True
    
    def use(self, player: Player) -> bool:
        """Use the consumable item"""
        if self.effect_type == "heal":
            actual_heal = player.heal(self.effect_value)
            print(f"💚 Vous avez utilisé {self.name} et récupéré {actual_heal} PV !")
            return True
        elif self.effect_type == "attack_buff":
            player.attack += self.effect_value
            print(f"⚔️  Vous avez utilisé {self.name} ! L'attaque augmente de {self.effect_value} temporairement !")
            return True
        elif self.effect_type == "defense_buff":
            player.defense += self.effect_value
            print(f"🛡️  Vous avez utilisé {self.name} ! La défense augmente de {self.effect_value} temporairement !")
            return True
        return False
    
    def get_info(self) -> str:
        effect_text = ""
        if self.effect_type == "heal":
            effect_text = f"Restaure {self.effect_value} PV"
        elif self.effect_type == "attack_buff":
            effect_text = f"ATK +{self.effect_value}"
        elif self.effect_type == "defense_buff":
            effect_text = f"DEF +{self.effect_value}"
        
        return f"🧪 {self.name} - {effect_text} - {self.description}"


class QuestItem(Item):
    """Special quest items"""
    
    def __init__(self, name: str, description: str, quest_id: str):
        super().__init__(name, description, "quest", value=0)
        self.quest_id = quest_id
        self.stackable = False
    
    def get_info(self) -> str:
        return f"📜 {self.name} - {self.description}"


class Inventory:
    """Inventory management class"""
    
    def __init__(self, max_slots: int = 20):
        self.items: List[Item] = []
        self.max_slots = max_slots
    
    def add_item(self, item: Item) -> bool:
        """Add item to inventory, return False if full"""
        # Check if item is stackable and already exists
        if item.stackable:
            for existing_item in self.items:
                if existing_item.name == item.name:
                    existing_item.quantity += item.quantity
                    return True
        
        # Check inventory space
        if len(self.items) >= self.max_slots:
            return False
        
        self.items.append(item)
        return True
    
    def remove_item(self, item_index: int) -> Optional[Item]:
        """Remove item from inventory"""
        if 0 <= item_index < len(self.items):
            item = self.items[item_index]
            
            # Handle stackable items
            if item.stackable and item.quantity > 1:
                item.quantity -= 1
                # Create a copy for return
                removed_item = Item(item.name, item.description, item.item_type, item.value)
                removed_item.quantity = 1
                return removed_item
            else:
                return self.items.pop(item_index)
        
        return None
    
    def get_item(self, item_index: int) -> Optional[Item]:
        """Get item without removing it"""
        if 0 <= item_index < len(self.items):
            return self.items[item_index]
        return None
    
    def use_item(self, item_index: int, player: Player) -> bool:
        """Use item from inventory"""
        item = self.get_item(item_index)
        if item and item.item_type == "consumable":
            if item.use(player):
                # Remove item if consumed
                if item.stackable:
                    item.quantity -= 1
                    if item.quantity <= 0:
                        self.remove_item(item_index)
                else:
                    self.remove_item(item_index)
                return True
        return False
    
    def get_inventory_display(self) -> str:
        """Get formatted inventory display"""
        if not self.items:
            return "🎒 Votre inventaire est vide"
        
        display = "🎒 INVENTAIRE\n"
        display += "=" * 40 + "\n"
        
        for i, item in enumerate(self.items):
            quantity_text = f" x{item.quantity}" if item.stackable and item.quantity > 1 else ""
            display += f"{i+1:2d}. {item.name}{quantity_text}\n"
            display += f"     {item.get_info()}\n"
        
        display += f"\nEmplacements : {len(self.items)}/{self.max_slots}"
        return display
    
    def get_empty_slots(self) -> int:
        """Get number of empty inventory slots"""
        return self.max_slots - len(self.items)
    
    def is_full(self) -> bool:
        """Check if inventory is full"""
        return len(self.items) >= self.max_slots
    
    def search_by_name(self, name: str) -> List[int]:
        """Find items by name, return list of indices"""
        found_indices = []
        for i, item in enumerate(self.items):
            if name.lower() in item.name.lower():
                found_indices.append(i)
        return found_indices
    
    def get_items_by_type(self, item_type: str) -> List[Item]:
        """Get all items of a specific type"""
        return [item for item in self.items if item.item_type == item_type]


# Item templates and creation functions
def create_health_potion() -> Consumable:
    """Create a health potion"""
    return Consumable(
        "Potion de Soin",
        "Un liquide rouge magique qui restaure la santé",
        "heal",
        30,
        25
    )


def create_large_health_potion() -> Consumable:
    """Create a large health potion"""
    return Consumable(
        "Grande Potion de Soin",
        "Un puissant élixir magique qui restaure beaucoup de santé",
        "heal",
        60,
        50
    )


def create_attack_potion() -> Consumable:
    """Create an attack potion"""
    return Consumable(
        "Potion d'Attaque",
        "Un breuvage ardent qui augmente temporairement la force d'attaque",
        "attack_buff",
        5,
        30
    )


def create_defense_potion() -> Consumable:
    """Create a defense potion"""
    return Consumable(
        "Potion de Défense",
        "Un tonique fortifiant qui augmente temporairement la défense",
        "defense_buff",
        3,
        30
    )


def create_iron_sword() -> Weapon:
    """Create an iron sword"""
    return Weapon(
        "Épée en Fer",
        "Une épée en fer bien forgée, fiable et efficace",
        8,
        75
    )


def create_steel_sword() -> Weapon:
    """Create a steel sword"""
    return Weapon(
        "Épée en Acier",
        "Une épée en acier supérieure qui frappe avec une force mortelle",
        12,
        150
    )


def create_iron_armor() -> Armor:
    """Create iron armor"""
    return Armor(
        "Armure en Fer",
        "Une armure en fer lourde qui offre une protection solide",
        6,
        80
    )


def create_steel_armor() -> Armor:
    """Create steel armor"""
    return Armor(
        "Armure en Acier",
        "Une armure en acier bien ajustée offrant une excellente protection",
        10,
        160
    )


def create_quest_item(name: str, description: str, quest_id: str) -> QuestItem:
    """Create a quest item"""
    return QuestItem(name, description, quest_id)


# Random loot tables
LOOT_TABLES = {
    "common": [
        (create_health_potion, 0.6),
        (create_attack_potion, 0.2),
        (create_defense_potion, 0.2),
    ],
    "uncommon": [
        (create_large_health_potion, 0.4),
        (create_iron_sword, 0.3),
        (create_iron_armor, 0.3),
    ],
    "rare": [
        (create_steel_sword, 0.4),
        (create_steel_armor, 0.4),
        (create_large_health_potion, 0.2),
    ]
}


def generate_loot(rarity: str = "common") -> Optional[Item]:
    """Generate random loot based on rarity"""
    if rarity not in LOOT_TABLES:
        rarity = "common"
    
    loot_table = LOOT_TABLES[rarity]
    
    # Random selection based on weights
    rand = random.random()
    cumulative = 0
    
    for item_func, weight in loot_table:
        cumulative += weight
        if rand <= cumulative:
            return item_func()
    
    # Fallback to first item
    return loot_table[0][0]()


import random
