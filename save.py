"""
Save module for BhilGame
Handles save and load system using JSON
"""

import json
import os
from typing import Dict, Any, Optional, List
from character import Player, Enemy
from world import World
from inventory import Inventory, Item, Weapon, Armor, Consumable, QuestItem
from story import StoryManager, Quest


class SaveManager:
    """Manages saving and loading game state"""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = save_directory
        self.save_file = os.path.join(save_directory, "bhilgame_save.json")
        self.ensure_save_directory()
    
    def ensure_save_directory(self):
        """Create save directory if it doesn't exist"""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def save_game(self, player: Player, world: World, story_manager: StoryManager) -> bool:
        """Save the current game state"""
        try:
            save_data = {
                "version": "1.0",
                "timestamp": self.get_timestamp(),
                "player": self.serialize_player(player),
                "world": self.serialize_world(world),
                "story": self.serialize_story(story_manager)
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print(f"✅ Game saved successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save game: {e}")
            return False
    
    def load_game(self) -> Optional[Dict[str, Any]]:
        """Load game state from file"""
        try:
            if not os.path.exists(self.save_file):
                print("❌ No save file found!")
                return None
            
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            print(f"✅ Game loaded successfully! (Saved: {save_data.get('timestamp', 'Unknown')})")
            return save_data
            
        except Exception as e:
            print(f"❌ Failed to load game: {e}")
            return None
    
    def has_save_file(self) -> bool:
        """Check if a save file exists"""
        return os.path.exists(self.save_file)
    
    def delete_save(self) -> bool:
        """Delete the save file"""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                print("✅ Save file deleted!")
                return True
            else:
                print("❌ No save file to delete!")
                return False
        except Exception as e:
            print(f"❌ Failed to delete save file: {e}")
            return False
    
    def serialize_player(self, player: Player) -> Dict[str, Any]:
        """Serialize player object to dictionary"""
        return {
            "name": player.name,
            "level": player.level,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "attack": player.attack,
            "defense": player.defense,
            "experience": player.experience,
            "experience_to_next_level": player.experience_to_next_level,
            "inventory": self.serialize_inventory(player.inventory),
            "equipped_weapon": self.serialize_item(player.equipped_weapon),
            "equipped_armor": self.serialize_item(player.equipped_armor),
            "quests_completed": player.quests_completed,
            "current_location": player.current_location,
            "gold": getattr(player, 'gold', 0)
        }
    
    def serialize_world(self, world: World) -> Dict[str, Any]:
        """Serialize world object to dictionary"""
        return {
            "current_location_name": world.current_location_name,
            "visited_locations": [name for name, loc in world.locations.items() if loc.visited]
        }
    
    def serialize_story(self, story_manager: StoryManager) -> Dict[str, Any]:
        """Serialize story manager to dictionary"""
        return {
            "main_story_progress": story_manager.main_story_progress,
            "flags": story_manager.flags,
            "quests": self.serialize_quests(story_manager.quests)
        }
    
    def serialize_inventory(self, inventory: Inventory) -> List[Dict[str, Any]]:
        """Serialize inventory to list of dictionaries"""
        serialized_items = []
        for item in inventory.items:
            serialized_items.append(self.serialize_item(item))
        return serialized_items
    
    def serialize_item(self, item: Optional[Item]) -> Optional[Dict[str, Any]]:
        """Serialize item to dictionary"""
        if item is None:
            return None
        
        base_data = {
            "name": item.name,
            "description": item.description,
            "item_type": item.item_type,
            "value": item.value,
            "quantity": getattr(item, 'quantity', 1)
        }
        
        # Add type-specific data
        if isinstance(item, Weapon):
            base_data["attack_bonus"] = item.attack_bonus
        elif isinstance(item, Armor):
            base_data["defense_bonus"] = item.defense_bonus
        elif isinstance(item, Consumable):
            base_data["effect_type"] = item.effect_type
            base_data["effect_value"] = item.effect_value
        elif isinstance(item, QuestItem):
            base_data["quest_id"] = item.quest_id
        
        return base_data
    
    def serialize_quests(self, quests: Dict[str, Quest]) -> Dict[str, Any]:
        """Serialize quests to dictionary"""
        serialized_quests = {}
        for quest_id, quest in quests.items():
            serialized_quests[quest_id] = {
                "completed": quest.completed,
                "progress": quest.progress
            }
        return serialized_quests
    
    def deserialize_player(self, player_data: Dict[str, Any]) -> Player:
        """Deserialize player from dictionary"""
        player = Player(player_data["name"])
        player.level = player_data["level"]
        player.hp = player_data["hp"]
        player.max_hp = player_data["max_hp"]
        player.attack = player_data["attack"]
        player.defense = player_data["defense"]
        player.experience = player_data["experience"]
        player.experience_to_next_level = player_data["experience_to_next_level"]
        player.quests_completed = player_data.get("quests_completed", [])
        player.current_location = player_data.get("current_location", "village")
        player.gold = player_data.get("gold", 0)
        
        # Restore inventory
        player.inventory = self.deserialize_inventory(player_data.get("inventory", []))
        
        # Restore equipped items
        player.equipped_weapon = self.deserialize_item(player_data.get("equipped_weapon"))
        player.equipped_armor = self.deserialize_item(player_data.get("equipped_armor"))
        
        return player
    
    def deserialize_world(self, world_data: Dict[str, Any]) -> World:
        """Deserialize world from dictionary"""
        world = World()
        world.current_location_name = world_data.get("current_location_name", "village")
        
        # Mark visited locations
        visited_locations = world_data.get("visited_locations", [])
        for location_name in visited_locations:
            if location_name in world.locations:
                world.locations[location_name].visited = True
        
        return world
    
    def deserialize_story(self, story_data: Dict[str, Any]) -> StoryManager:
        """Deserialize story manager from dictionary"""
        story_manager = StoryManager()
        story_manager.main_story_progress = story_data.get("main_story_progress", 0)
        story_manager.flags = story_data.get("flags", {})
        
        # Restore quest progress
        quests_data = story_data.get("quests", {})
        for quest_id, quest_info in quests_data.items():
            if quest_id in story_manager.quests:
                quest = story_manager.quests[quest_id]
                quest.completed = quest_info.get("completed", False)
                quest.progress = quest_info.get("progress", {})
        
        return story_manager
    
    def deserialize_inventory(self, inventory_data: List[Dict[str, Any]]) -> Inventory:
        """Deserialize inventory from list of dictionaries"""
        inventory = Inventory()
        
        for item_data in inventory_data:
            item = self.deserialize_item(item_data)
            if item:
                inventory.add_item(item)
        
        return inventory
    
    def deserialize_item(self, item_data: Optional[Dict[str, Any]]) -> Optional[Item]:
        """Deserialize item from dictionary"""
        if item_data is None:
            return None
        
        item_type = item_data["item_type"]
        name = item_data["name"]
        description = item_data["description"]
        value = item_data["value"]
        quantity = item_data.get("quantity", 1)
        
        if item_type == "weapon":
            item = Weapon(name, description, item_data["attack_bonus"], value)
        elif item_type == "armor":
            item = Armor(name, description, item_data["defense_bonus"], value)
        elif item_type == "consumable":
            item = Consumable(
                name, description, 
                item_data["effect_type"], 
                item_data["effect_value"], 
                value
            )
        elif item_type == "quest":
            item = QuestItem(name, description, item_data["quest_id"])
        else:
            # Base item as fallback
            item = Item(name, description, item_type, value)
        
        item.quantity = quantity
        return item
    
    def get_timestamp(self) -> str:
        """Get current timestamp as string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_save_info(self) -> Optional[Dict[str, str]]:
        """Get information about the save file"""
        if not self.has_save_file():
            return None
        
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            player_data = save_data.get("player", {})
            return {
                "player_name": player_data.get("name", "Unknown"),
                "level": str(player_data.get("level", 1)),
                "location": player_data.get("current_location", "Unknown"),
                "timestamp": save_data.get("timestamp", "Unknown"),
                "quests_completed": str(len(player_data.get("quests_completed", [])))
            }
        except Exception:
            return None
    
    def display_save_info(self):
        """Display formatted save information"""
        save_info = self.get_save_info()
        if save_info:
            print("\n📁 SAVE FILE INFO")
            print("=" * 30)
            print(f"Player: {save_info['player_name']}")
            print(f"Level: {save_info['level']}")
            print(f"Location: {save_info['location']}")
            print(f"Quests Completed: {save_info['quests_completed']}")
            print(f"Saved: {save_info['timestamp']}")
        else:
            print("\n❌ No save file found!")


# Auto-save functionality
class AutoSave:
    """Handles automatic saving"""
    
    def __init__(self, save_manager: SaveManager, auto_save_interval: int = 300):
        self.save_manager = save_manager
        self.auto_save_interval = auto_save_interval  # seconds
        self.last_save_time = 0
    
    def should_auto_save(self) -> bool:
        """Check if it's time to auto-save"""
        import time
        current_time = time.time()
        return (current_time - self.last_save_time) >= self.auto_save_interval
    
    def auto_save(self, player: Player, world: World, story_manager: StoryManager):
        """Perform auto-save"""
        if self.should_auto_save():
            if self.save_manager.save_game(player, world, story_manager):
                import time
                self.last_save_time = time.time()
                print("💾 Game auto-saved!")
                return True
        return False
