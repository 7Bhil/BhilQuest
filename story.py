"""
Module Histoire pour BhilQuest
Gère les quêtes, les dialogues et la progression de l'histoire
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
                reward_text.append(f"{gold} pièces d'or")
            
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
                    item = create_quest_item(item_name, "Objet de récompense de quête", self.quest_id)
                
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
                    progress_lines.append(f"Vaincre {enemy_type}s : {current}/{required_count}")
            elif req_type == "item":
                item_name = req_data
                has_item = self.progress.get("has_item", False)
                status = "✓" if has_item else "✗"
                progress_lines.append(f"Obtenir {item_name} : {status}")
        
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
        return self.dialogues.get(situation, "Je n'ai rien à vous dire.")
    
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
            "Ancien Marcus",
            "Un vieil homme sage avec une longue barbe blanche et des yeux bienveillants. Il a vécu dans le village toute sa vie.",
            "village"
        )
        elder.add_dialogue("greeting", 
            "Salutations, jeune aventurier ! Je suis Marcus, l'ancien du village. Notre village fait face à des problèmes. "
            "Les gobelins pillent nos réserves, et d'étranges créatures sortent des ruines proches. "
            "Nous avons besoin de braves guerriers comme vous.")
        elder.add_dialogue("quest_accepted",
            "Excellent ! Votre courage nous donne espoir. Revenez me voir quand vous aurez fini vos tâches, "
            "et je vous récompenserai généreusement.")
        elder.add_dialogue("quest_completed",
            "Magnifique travail ! Vous avez sauvé notre village. Les gens peuvent dormir paisiblement. "
            "Comme promis, voici votre récompense. Mais... je crains que de plus grands dangers ne vous attendent.")
        elder.add_dialogue("no_quests",
            "Vous nous avez déjà tant aidés. Reposez-vous bien, héros. Parlez aux autres pour de nouvelles aventures.")
        
        # Blacksmith
        blacksmith = NPC(
            "Thorin le Forgeron",
            "Un nain musclé avec une barbe épaisse et des mains couvertes de suie. Il travaille toujours à sa forge.",
            "village"
        )
        blacksmith.add_dialogue("greeting",
            "Ah, un nouveau visage ! Je suis Thorin. Je forge les meilleures armes et armures du pays. "
            "Si vous m'apportez des matériaux rares, je pourrai vous fabriquer quelque chose de spécial.")
        blacksmith.add_dialogue("quest_accepted",
            "Parfait ! Ces matériaux me permettront de créer un équipement exceptionnel. Soyez prudent dans les donjons !")
        blacksmith.add_dialogue("quest_completed",
            "Par mon marteau, vous l'avez fait ! Tenez, prenez cette arme de maître que j'ai forgée pour vous.")
        
        # Mysterious Stranger
        stranger = NPC(
            "L'Étranger Mystérieux",
            "Une silhouette encapuchonnée entourée de mystère. Son visage est caché dans l'ombre.",
            "ruins"
        )
        stranger.add_dialogue("greeting",
            "Alors, un autre guerrier cherche les secrets de ces ruines... Je ne suis qu'un humble érudit. "
            "Ces ruines cachent un grand pouvoir, mais aussi un grand danger. M'aiderez-vous à découvrir leurs secrets ?")
        stranger.add_dialogue("quest_accepted",
            "Choix judicieux. Les anciens artefacts doivent être récupérés avant de tomber entre de mauvaises mains.")
        stranger.add_dialogue("quest_completed",
            "Incroyable ! Vous avez récupéré l'artefact ! Cela aidera à protéger le royaume des ténèbres. "
            "Votre destin est plus grand que vous ne l'imaginez...")
        
        # Create quests
        # Quest 1: Problème de Gobelins
        goblin_quest = Quest(
            "goblin_trouble",
            "Problème de Gobelins",
            "Le village est attaqué par des gobelins. Aidez-nous en battant 5 gobelins.",
            "Ancien Marcus",
            {"kill": {"goblin": 5}},
            {"exp": 50, "gold": 25, "item": "health_potion"}
        )
        
        # Quest 2: Exploration des Ruines
        ruins_quest = Quest(
            "ruins_exploration",
            "Exploration des Ruines",
            "Explorez les ruines antiques et trouvez l'artefact mystérieux.",
            "L'Étranger Mystérieux",
            {"item": "ancient_artifact"},
            {"exp": 100, "gold": 75, "item": "iron_sword"}
        )
        
        # Quest 3: Matériaux du Donjon
        dungeon_quest = Quest(
            "dungeon_materials",
            "Matériaux du Donjon",
            "Aventurez-vous dans les profondeurs du donjon et ramassez des matériaux rares pour le forgeron.",
            "Thorin le Forgeron",
            {"kill": {"skeleton": 3, "orc": 2}},
            {"exp": 150, "gold": 100, "item": "steel_sword"}
        )
        
        # Quest 4: Tueur de Dragon (quête finale)
        dragon_quest = Quest(
            "dragon_slayer",
            "Tueur de Dragon",
            "Le dragon ancien dans les profondeurs du donjon menace tout le royaume. Vous devez le vaincre !",
            "Ancien Marcus",
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
            return "Vous êtes un nouvel aventurier, prêt à prouver sa valeur."
        elif self.main_story_progress == 1:
            return "Vous avez goûté au combat et survécu. Le chemin du héros s'ouvre à vous."
        elif self.main_story_progress == 2:
            return "Vous avez prouvé vos capacités de guerrier. De plus grands défis vous attendent."
        elif self.main_story_progress == 3:
            return "Vous êtes un véritable héros du royaume ! Le dragon est vaincu et la paix restaurée."
        else:
            return "Votre légende continue de grandir..."
    
    def get_quests_display(self, player: Player) -> str:
        """Get formatted display of quests"""
        display = "📜 QUÊTES\n"
        display += "=" * 40 + "\n"
        
        # Active quests
        active_quests = self.get_active_quests(player)
        if active_quests:
            display += "🔄 QUÊTES ACTIVES :\n"
            for quest in active_quests:
                display += f"\n• {quest.name}\n"
                display += f"  {quest.description}\n"
                display += f"  Progression :\n"
                progress_text = quest.get_progress_text()
                for line in progress_text.split('\n'):
                    display += f"    {line}\n"
        else:
            display += "🔄 QUÊTES ACTIVES : Aucune\n"
        
        # Available quests
        available_quests = self.get_available_quests(player)
        if available_quests:
            display += "\n📋 QUÊTES DISPONIBLES :\n"
            for quest in available_quests:
                display += f"\n• {quest.name} (de {quest.quest_giver})\n"
                display += f"  {quest.description}\n"
        
        return display
