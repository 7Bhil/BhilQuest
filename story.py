"""
Story module for BhilGame
Handles quests, dialogues, and story progression
"""

from typing import Dict, List, Optional, Tuple
from character import Player
from inventory import create_quest_item, generate_loot


class Quest:
    """Represents a quest in the game"""
    
    def __init__(self, quest_id: str, name: str, description: str, 
                 quest_giver: str, requirements: Dict, rewards: Dict):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.quest_giver = quest_giver
        self.requirements = requirements  # e.g., {"kill": {"goblin": 5}, "item": "ancient_key"}
        self.rewards = rewards  # e.g., {"exp": 100, "gold": 50, "item": "iron_sword"}
        self.completed = False
        self.progress = {}  # Track progress toward requirements
        
        # Initialize progress
        for req_type, req_data in self.requirements.items():
            if req_type == "kill":
                for enemy_type in req_data:
                    self.progress[f"kill_{enemy_type}"] = 0
            elif req_type == "item":
                self.progress["has_item"] = False
    
    def update_progress(self, progress_type: str, target: str, amount: int = 1):
        """Update quest progress"""
        if progress_type == "kill":
            key = f"kill_{target}"
            if key in self.progress:
                self.progress[key] += amount
                return self.check_completion()
        elif progress_type == "item":
            if target == self.requirements.get("item", ""):
                self.progress["has_item"] = True
                return self.check_completion()
        return False
    
    def check_completion(self) -> bool:
        """Check if quest requirements are met"""
        for req_type, req_data in self.requirements.items():
            if req_type == "kill":
                for enemy_type, required_count in req_data.items():
                    current = self.progress.get(f"kill_{enemy_type}", 0)
                    if current < required_count:
                        return False
            elif req_type == "item":
                if not self.progress.get("has_item", False):
                    return False
        return True
    
    def complete_quest(self, player: Player):
        """Complete the quest and give rewards"""
        if not self.completed and self.check_completion():
            self.completed = True
            player.quests_completed.append(self.quest_id)
            
            # Give rewards
            reward_text = []
            
            if "exp" in self.rewards:
                exp = self.rewards["exp"]
                player.gain_experience(exp)
                reward_text.append(f"{exp} EXP")
            
            if "gold" in self.rewards:
                # Assuming player has gold attribute
                gold = self.rewards["gold"]
                if not hasattr(player, 'gold'):
                    player.gold = 0
                player.gold += gold
                reward_text.append(f"{gold} gold")
            
            if "item" in self.rewards:
                item_name = self.rewards["item"]
                # Create item based on name (simplified)
                if item_name == "health_potion":
                    from inventory import create_health_potion
                    item = create_health_potion()
                elif item_name == "iron_sword":
                    from inventory import create_iron_sword
                    item = create_iron_sword()
                else:
                    item = create_quest_item(item_name, "Quest reward item", self.quest_id)
                
                player.add_item(item)
                reward_text.append(item.name)
            
            return reward_text
        return []
    
    def get_progress_text(self) -> str:
        """Get formatted progress text"""
        progress_lines = []
        
        for req_type, req_data in self.requirements.items():
            if req_type == "kill":
                for enemy_type, required_count in req_data.items():
                    current = self.progress.get(f"kill_{enemy_type}", 0)
                    progress_lines.append(f"Defeat {enemy_type}s: {current}/{required_count}")
            elif req_type == "item":
                item_name = req_data
                has_item = self.progress.get("has_item", False)
                status = "✓" if has_item else "✗"
                progress_lines.append(f"Obtain {item_name}: {status}")
        
        return "\n".join(progress_lines)


class NPC:
    """Non-Player Character"""
    
    def __init__(self, name: str, description: str, location: str):
        self.name = name
        self.description = description
        self.location = location
        self.dialogues = {}  # situation -> dialogue
        self.quests = []  # List of quests this NPC offers
        self.current_quest_index = 0
        
    def add_dialogue(self, situation: str, text: str):
        """Add dialogue for a situation"""
        self.dialogues[situation] = text
    
    def add_quest(self, quest: Quest):
        """Add a quest that this NPC offers"""
        self.quests.append(quest)
    
    def get_dialogue(self, situation: str = "greeting") -> str:
        """Get dialogue for a situation"""
        return self.dialogues.get(situation, "I have nothing to say.")
    
    def has_available_quests(self, player: Player) -> bool:
        """Check if NPC has quests available for player"""
        for quest in self.quests:
            if quest.quest_id not in player.quests_completed:
                return True
        return False
    
    def get_next_quest(self) -> Optional[Quest]:
        """Get next available quest"""
        for quest in self.quests:
            if not quest.completed:
                return quest
        return None


class StoryManager:
    """Manages the game's story and quests"""
    
    def __init__(self):
        self.npcs = {}
        self.quests = {}
        self.create_story_content()
        self.main_story_progress = 0
        self.flags = {}  # Story flags for tracking events
    
    def create_story_content(self):
        """Create NPCs and quests for the game"""
        
        # Village Elder
        elder = NPC(
            "Village Elder Marcus",
            "A wise old man with a long white beard and kind eyes. He has lived in the village his entire life and knows many secrets.",
            "village"
        )
        elder.add_dialogue("greeting", 
            "Greetings, young adventurer! I am Marcus, the village elder. Our peaceful village is facing troubles lately. "
            "Goblins have been raiding our supplies, and strange creatures emerge from the nearby ruins. "
            "We need brave warriors like you to help us.")
        elder.add_dialogue("quest_accepted",
            "Excellent! Your courage gives us hope. Return to me when you have completed your tasks, "
            "and I shall reward you generously.")
        elder.add_dialogue("quest_completed",
            "Wonderful work! You have saved our village from these threats. The people can sleep peacefully now. "
            "As promised, here is your reward. But... I fear greater dangers await you in the world.")
        elder.add_dialogue("no_quests",
            "You have already helped us so much. Rest well, brave hero. Perhaps speak to others in the village "
            "for new adventures.")
        
        # Blacksmith
        blacksmith = NPC(
            "Blacksmith Thorin",
            "A muscular dwarf with a thick beard and soot-covered hands. He's always working at his forge.",
            "village"
        )
        blacksmith.add_dialogue("greeting",
            "Ah, a new face! I'm Thorin, the village blacksmith. I forge the finest weapons and armor in these lands. "
            "If you bring me rare materials from your adventures, I can craft you something special.")
        blacksmith.add_dialogue("quest_accepted",
            "Perfect! These materials will allow me to create masterwork equipment. Be careful in the dungeons - "
            "they're not for the faint of heart!")
        blacksmith.add_dialogue("quest_completed",
            "By my hammer, you did it! Here, take this masterwork weapon I forged for you. "
            "It should serve you well in the battles ahead.")
        
        # Mysterious Stranger
        stranger = NPC(
            "Mysterious Stranger",
            "A hooded figure with an air of mystery about them. Their face is hidden in shadow.",
            "ruins"
        )
        stranger.add_dialogue("greeting",
            "So, another warrior seeks the secrets of these ruins... I am but a humble scholar of ancient times. "
            "The ruins hold great power, but also great danger. Perhaps you can help me uncover their secrets?")
        stranger.add_dialogue("quest_accepted",
            "Wisdom choice. The ancient artifacts must be recovered before they fall into wrong hands. "
            "The dungeon depths hold what we seek.")
        stranger.add_dialogue("quest_completed",
            "Incredible! You have recovered the artifact! This will help protect the realm from darkness. "
            "Your destiny is greater than you imagine...")
        
        # Create quests
        # Quest 1: Goblin Trouble
        goblin_quest = Quest(
            "goblin_trouble",
            "Goblin Trouble",
            "The village is being raided by goblins. Help us by defeating 5 goblins to make our village safe again.",
            "Village Elder Marcus",
            {"kill": {"goblin": 5}},
            {"exp": 50, "gold": 25, "item": "health_potion"}
        )
        
        # Quest 2: Ancient Ruins Exploration
        ruins_quest = Quest(
            "ruins_exploration",
            "Ruins Exploration",
            "Explore the ancient ruins and find the mysterious artifact that the stranger seeks.",
            "Mysterious Stranger",
            {"item": "ancient_artifact"},
            {"exp": 100, "gold": 75, "item": "iron_sword"}
        )
        
        # Quest 3: Dungeon Materials
        dungeon_quest = Quest(
            "dungeon_materials",
            "Dungeon Materials",
            "Venture into the dungeon depths and collect rare materials for the blacksmith.",
            "Blacksmith Thorin",
            {"kill": {"skeleton": 3, "orc": 2}},
            {"exp": 150, "gold": 100, "item": "steel_sword"}
        )
        
        # Quest 4: Dragon Slayer (final quest)
        dragon_quest = Quest(
            "dragon_slayer",
            "Dragon Slayer",
            "The ancient dragon in the dungeon depths threatens the entire realm. You must defeat it!",
            "Village Elder Marcus",
            {"kill": {"dragon": 1}},
            {"exp": 500, "gold": 500, "item": "dragon_scale"}
        )
        
        # Assign quests to NPCs
        elder.add_quest(goblin_quest)
        elder.add_quest(dragon_quest)
        blacksmith.add_quest(dungeon_quest)
        stranger.add_quest(ruins_quest)
        
        # Store NPCs and quests
        self.npcs = {
            "elder": elder,
            "blacksmith": blacksmith,
            "stranger": stranger
        }
        
        self.quests = {
            "goblin_trouble": goblin_quest,
            "ruins_exploration": ruins_quest,
            "dungeon_materials": dungeon_quest,
            "dragon_slayer": dragon_quest
        }
    
    def get_npc_at_location(self, location: str) -> List[NPC]:
        """Get all NPCs at a specific location"""
        return [npc for npc in self.npcs.values() if npc.location == location]
    
    def update_quest_progress(self, player: Player, progress_type: str, target: str, amount: int = 1):
        """Update progress for all relevant quests"""
        completed_quests = []
        
        for quest in self.quests.values():
            if quest.quest_id not in player.quests_completed:
                if quest.update_progress(progress_type, target, amount):
                    # Quest just completed
                    rewards = quest.complete_quest(player)
                    completed_quests.append((quest, rewards))
        
        return completed_quests
    
    def get_available_quests(self, player: Player) -> List[Quest]:
        """Get all quests available to player"""
        available = []
        for quest in self.quests.values():
            if quest.quest_id not in player.quests_completed:
                # Check if player has met the quest giver
                for npc in self.npcs.values():
                    if quest.quest_giver == npc.name and npc.location == player.current_location:
                        available.append(quest)
                        break
        return available
    
    def get_active_quests(self, player: Player) -> List[Quest]:
        """Get all active (accepted but not completed) quests"""
        active = []
        for quest in self.quests.values():
            if quest.quest_id not in player.quests_completed and not quest.completed:
                # Check if player has this quest (simplified - assume they do if not completed)
                active.append(quest)
        return active
    
    def get_quest_by_id(self, quest_id: str) -> Optional[Quest]:
        """Get quest by ID"""
        return self.quests.get(quest_id)
    
    def advance_story(self, event: str):
        """Advance main story based on events"""
        if event == "first_blood":
            self.main_story_progress = 1
        elif event == "first_quest_complete":
            self.main_story_progress = 2
        elif event == "dragon_defeated":
            self.main_story_progress = 3
            self.flags["hero_of_realm"] = True
    
    def get_story_status(self) -> str:
        """Get current story status"""
        if self.main_story_progress == 0:
            return "You are a new adventurer, ready to prove your worth."
        elif self.main_story_progress == 1:
            return "You have tasted combat and survived. The path of a hero opens before you."
        elif self.main_story_progress == 2:
            return "You have proven yourself as a capable warrior. Greater challenges await."
        elif self.main_story_progress == 3:
            return "You are a true hero of the realm! The dragon is defeated and peace restored."
        else:
            return "Your legend continues to grow..."
    
    def get_quests_display(self, player: Player) -> str:
        """Get formatted display of quests"""
        display = "📜 QUESTS\n"
        display += "=" * 40 + "\n"
        
        # Active quests
        active_quests = self.get_active_quests(player)
        if active_quests:
            display += "🔄 ACTIVE QUESTS:\n"
            for quest in active_quests:
                display += f"\n• {quest.name}\n"
                display += f"  {quest.description}\n"
                display += f"  Progress:\n"
                progress_text = quest.get_progress_text()
                for line in progress_text.split('\n'):
                    display += f"    {line}\n"
        else:
            display += "🔄 ACTIVE QUESTS: None\n"
        
        # Available quests
        available_quests = self.get_available_quests(player)
        if available_quests:
            display += "\n📋 AVAILABLE QUESTS:\n"
            for quest in available_quests:
                display += f"\n• {quest.name} (from {quest.quest_giver})\n"
                display += f"  {quest.description}\n"
        
        return display
