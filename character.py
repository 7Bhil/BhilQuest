"""
Character module for BhilGame
Handles player and enemy classes with stats and leveling system
"""

import random
from typing import Dict, List


class Character:
    """Base class for all characters in the game"""
    
    def __init__(self, name: str, hp: int, attack: int, defense: int, level: int = 1):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = 0
        self.experience_to_next_level = 100
        
    def take_damage(self, damage: int) -> int:
        """Apply damage to character, return actual damage dealt"""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Heal character, return actual amount healed"""
        actual_heal = min(amount, self.max_hp - self.hp)
        self.hp += actual_heal
        return actual_heal
    
    def is_alive(self) -> bool:
        """Check if character is still alive"""
        return self.hp > 0
    
    def gain_experience(self, exp: int) -> bool:
        """Add experience and check for level up, returns True if leveled up"""
        self.experience += exp
        while self.experience >= self.experience_to_next_level:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """Level up the character and improve stats"""
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        
        # Improve stats
        hp_increase = random.randint(5, 10)
        attack_increase = random.randint(1, 3)
        defense_increase = random.randint(1, 2)
        
        self.max_hp += hp_increase
        self.hp = self.max_hp  # Full heal on level up
        self.attack += attack_increase
        self.defense += defense_increase
        
        print(f"\n🎉 {self.name} leveled up to level {self.level}!")
        print(f"   HP +{hp_increase}, Attack +{attack_increase}, Defense +{defense_increase}")
    
    def get_stats(self) -> str:
        """Return formatted string of character stats"""
        return f"{self.name} (Lv.{self.level}) - HP: {self.hp}/{self.max_hp}, ATK: {self.attack}, DEF: {self.defense}"


class Player(Character):
    """Player character class with inventory and special abilities"""
    
    def __init__(self, name: str):
        super().__init__(name, hp=100, attack=10, defense=5, level=1)
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.quests_completed = []
        self.current_location = "village"
        
    def get_total_attack(self) -> int:
        """Calculate total attack including equipped weapon"""
        total_attack = self.attack
        if self.equipped_weapon:
            total_attack += self.equipped_weapon.attack_bonus
        return total_attack
    
    def get_total_defense(self) -> int:
        """Calculate total defense including equipped armor"""
        total_defense = self.defense
        if self.equipped_armor:
            total_defense += self.equipped_armor.defense_bonus
        return total_defense
    
    def equip_weapon(self, weapon):
        """Equip a weapon"""
        if self.equipped_weapon:
            self.inventory.append(self.equipped_weapon)
        self.equipped_weapon = weapon
        if weapon in self.inventory:
            self.inventory.remove(weapon)
        print(f"🗡️  Equipped {weapon.name}")
    
    def equip_armor(self, armor):
        """Equip armor"""
        if self.equipped_armor:
            self.inventory.append(self.equipped_armor)
        self.equipped_armor = armor
        if armor in self.inventory:
            self.inventory.remove(armor)
        print(f"🛡️  Equipped {armor.name}")
    
    def add_item(self, item):
        """Add item to inventory"""
        self.inventory.append(item)
        print(f"📦 Obtained {item.name}")
    
    def use_item(self, item_index: int) -> bool:
        """Use an item from inventory"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if item.use(self):
                self.inventory.pop(item_index)
                return True
        return False
    
    def get_detailed_stats(self) -> str:
        """Return detailed stats including equipment"""
        weapon_name = self.equipped_weapon.name if self.equipped_weapon else "None"
        armor_name = self.equipped_armor.name if self.equipped_armor else "None"
        
        stats = f"""
╔══════════════════════════════════════╗
║     {self.name} - Level {self.level} Warrior     ║
╠══════════════════════════════════════╣
║ HP: {self.hp}/{self.max_hp}                              ║
║ Attack: {self.get_total_attack()} (Base: {self.attack})                    ║
║ Defense: {self.get_total_defense()} (Base: {self.defense})                   ║
║ EXP: {self.experience}/{self.experience_to_next_level}                        ║
╠══════════════════════════════════════╣
║ Weapon: {weapon_name:<18} ║
║ Armor: {armor_name:<18} ║
╚══════════════════════════════════════╝"""
        return stats


class Enemy(Character):
    """Enemy character class"""
    
    def __init__(self, name: str, hp: int, attack: int, defense: int, level: int, exp_reward: int):
        super().__init__(name, hp, attack, defense, level)
        self.exp_reward = exp_reward
        self.loot_table = []
    
    def get_attack_damage(self) -> int:
        """Calculate attack damage with randomness"""
        base_damage = self.attack
        variance = random.randint(-2, 2)
        return max(1, base_damage + variance)
    
    def choose_action(self, player: Player) -> str:
        """AI chooses action in combat"""
        # Simple AI: attack most of the time, sometimes defend
        if self.hp < self.max_hp * 0.3 and random.random() < 0.3:
            return "defend"
        return "attack"


# Enemy templates
ENEMY_TEMPLATES = {
    "goblin": {
        "name": "Goblin",
        "hp": 30,
        "attack": 8,
        "defense": 2,
        "level": 1,
        "exp_reward": 25
    },
    "wolf": {
        "name": "Wild Wolf",
        "hp": 40,
        "attack": 12,
        "defense": 3,
        "level": 2,
        "exp_reward": 35
    },
    "bandit": {
        "name": "Bandit",
        "hp": 50,
        "attack": 15,
        "defense": 5,
        "level": 3,
        "exp_reward": 50
    },
    "skeleton": {
        "name": "Skeleton",
        "hp": 45,
        "attack": 14,
        "defense": 4,
        "level": 3,
        "exp_reward": 45
    },
    "orc": {
        "name": "Orc Warrior",
        "hp": 80,
        "attack": 20,
        "defense": 8,
        "level": 5,
        "exp_reward": 80
    },
    "dragon": {
        "name": "Ancient Dragon",
        "hp": 200,
        "attack": 35,
        "defense": 15,
        "level": 10,
        "exp_reward": 300
    }
}


def create_enemy(enemy_type: str, level_modifier: int = 0) -> Enemy:
    """Create an enemy from template with optional level modification"""
    if enemy_type not in ENEMY_TEMPLATES:
        enemy_type = "goblin"  # Default fallback
    
    template = ENEMY_TEMPLATES[enemy_type].copy()
    template["level"] += level_modifier
    
    # Scale stats with level
    level_scale = template["level"]
    template["hp"] = int(template["hp"] * (1 + level_scale * 0.1))
    template["attack"] = int(template["attack"] * (1 + level_scale * 0.1))
    template["defense"] = int(template["defense"] * (1 + level_scale * 0.1))
    template["exp_reward"] = int(template["exp_reward"] * (1 + level_scale * 0.1))
    
    return Enemy(**template)
