"""
Combat module for BhilGame
Handles turn-based combat system between player and enemies
"""

import random
import time
from typing import Optional, Tuple
from character import Player, Enemy
from inventory import generate_loot


class Combat:
    """Turn-based combat system"""
    
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
        self.combat_log = []
        self.player_defending = False
        self.enemy_defending = False
        self.flee_attempts = 0
        self.max_flee_attempts = 3
    
    def start_combat(self) -> bool:
        """Start combat, return True if player wins, False if player loses"""
        print(f"\n⚔️  COMBAT BEGINS!")
        print(f"{'='*50}")
        print(f"{self.player.name} VS {self.enemy.name}")
        print(f"{'='*50}")
        print(f"{self.player.get_stats()}")
        print(f"{self.enemy.get_stats()}")
        print(f"{'='*50}")
        
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn_count += 1
            self.player_defending = False
            self.enemy_defending = False
            
            print(f"\n--- TURN {self.turn_count} ---")
            
            # Player turn
            if self.player_turn():
                # Combat ended (player fled or enemy defeated)
                continue
            
            # Check if enemy is still alive
            if not self.enemy.is_alive():
                break
            
            # Enemy turn
            self.enemy_turn()
            
            # Display status after both turns
            self.display_combat_status()
        
        return self.resolve_combat()
    
    def player_turn(self) -> bool:
        """Handle player's turn, return True if combat ended"""
        print(f"\n{self.player.name}'s Turn:")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Item")
        print("4. Flee")
        
        while True:
            try:
                choice = input("Choose your action (1-4): ").strip()
                
                if choice == "1":
                    return self.player_attack()
                elif choice == "2":
                    return self.player_defend()
                elif choice == "3":
                    return self.player_use_item()
                elif choice == "4":
                    return self.player_flee()
                else:
                    print("Invalid choice! Please enter 1-4.")
            except KeyboardInterrupt:
                print("\nCombat interrupted!")
                return True
    
    def player_attack(self) -> bool:
        """Player attacks enemy"""
        damage = self.player.get_total_attack()
        variance = random.randint(-2, 3)
        damage = max(1, damage + variance)
        
        # Apply enemy defense if not defending
        if self.enemy_defending:
            damage = max(1, damage // 2)
            print(f"🛡️  {self.enemy.name} is defending! Damage reduced!")
        
        actual_damage = self.enemy.take_damage(damage)
        
        print(f"⚔️  {self.player.name} attacks {self.enemy.name} for {actual_damage} damage!")
        
        if not self.enemy.is_alive():
            print(f"💀 {self.enemy.name} has been defeated!")
            return True
        
        return False
    
    def player_defend(self) -> bool:
        """Player defends"""
        self.player_defending = True
        print(f"🛡️  {self.player.name} takes a defensive stance!")
        return False
    
    def player_use_item(self) -> bool:
        """Player uses an item"""
        if not self.player.inventory:
            print("🎒 You have no items to use!")
            return self.player_turn()  # Re-prompt
        
        print("\n🎒 Your Items:")
        for i, item in enumerate(self.player.inventory):
            if item.item_type == "consumable":
                quantity = f" x{item.quantity}" if item.stackable and item.quantity > 1 else ""
                print(f"{i+1}. {item.name}{quantity} - {item.get_info()}")
        
        while True:
            try:
                choice = input("Choose item to use (or 0 to cancel): ").strip()
                
                if choice == "0":
                    return self.player_turn()  # Re-prompt
                
                item_index = int(choice) - 1
                if 0 <= item_index < len(self.player.inventory):
                    item = self.player.inventory[item_index]
                    if item.item_type == "consumable":
                        if self.player.use_item(item_index):
                            return False
                        else:
                            print("❌ Cannot use this item!")
                    else:
                        print("❌ This item cannot be used in combat!")
                else:
                    print("Invalid item number!")
            except ValueError:
                print("Please enter a valid number!")
    
    def player_flee(self) -> bool:
        """Player attempts to flee"""
        self.flee_attempts += 1
        
        if self.flee_attempts >= self.max_flee_attempts:
            print("💨 You've attempted to flee too many times! You must fight!")
            return False
        
        flee_chance = 0.4 + (self.flee_attempts * 0.1)  # Increasing chance
        flee_chance = min(0.8, flee_chance)  # Max 80% chance
        
        if random.random() < flee_chance:
            print(f"💨 {self.player.name} successfully fled from combat!")
            return True
        else:
            print(f"❌ {self.player.name} failed to flee!")
            return False
    
    def enemy_turn(self):
        """Handle enemy's turn"""
        action = self.enemy.choose_action(self.player)
        
        print(f"\n{self.enemy.name}'s Turn:")
        
        if action == "attack":
            self.enemy_attack()
        elif action == "defend":
            self.enemy_defend()
    
    def enemy_attack(self) -> bool:
        """Enemy attacks player"""
        damage = self.enemy.get_attack_damage()
        
        # Apply player defense if defending
        if self.player_defending:
            damage = max(1, damage // 2)
            print(f"🛡️  {self.player.name} is defending! Damage reduced!")
        
        actual_damage = self.player.take_damage(damage)
        
        print(f"⚔️  {self.enemy.name} attacks {self.player.name} for {actual_damage} damage!")
        
        if not self.player.is_alive():
            print(f"💀 {self.player.name} has been defeated!")
            return True
        
        return False
    
    def enemy_defend(self):
        """Enemy defends"""
        self.enemy_defending = True
        print(f"🛡️  {self.enemy.name} takes a defensive stance!")
    
    def display_combat_status(self):
        """Display current combat status"""
        print(f"\n📊 COMBAT STATUS")
        print(f"{'='*30}")
        print(f"{self.player.name}: {self.player.hp}/{self.player.max_hp} HP")
        print(f"{self.enemy.name}: {self.enemy.hp}/{self.enemy.max_hp} HP")
        
        if self.player_defending:
            print(f"🛡️  {self.player.name} is defending")
        if self.enemy_defending:
            print(f"🛡️  {self.enemy.name} is defending")
    
    def resolve_combat(self) -> bool:
        """Resolve combat outcome and handle rewards"""
        print(f"\n{'='*50}")
        
        if self.player.is_alive():
            print(f"🎉 VICTORY! {self.player.name} has defeated {self.enemy.name}!")
            
            # Experience reward
            exp_gained = self.enemy.exp_reward
            leveled_up = self.player.gain_experience(exp_gained)
            
            print(f"📈 Gained {exp_gained} EXP!")
            
            # Loot drops
            loot = self.generate_loot()
            if loot:
                print(f"💰 {self.enemy.name} dropped:")
                for item in loot:
                    if self.player.inventory.add_item(item):
                        print(f"   📦 {item.name}")
                    else:
                        print(f"   ❌ Inventory full! Cannot pick up {item.name}")
            
            return True
        else:
            print(f"💀 DEFEAT! {self.player.name} has been defeated by {self.enemy.name}!")
            print("💔 You have lost the battle...")
            return False
    
    def generate_loot(self) -> list:
        """Generate loot based on enemy"""
        loot = []
        
        # Base chance for loot drop
        if random.random() < 0.7:  # 70% chance for something
            # Determine loot rarity based on enemy level
            if self.enemy.level >= 8:
                rarity = random.choices(["rare", "uncommon", "common"], weights=[0.3, 0.4, 0.3])[0]
            elif self.enemy.level >= 4:
                rarity = random.choices(["uncommon", "common"], weights=[0.4, 0.6])[0]
            else:
                rarity = "common"
            
            # Generate 1-2 items
            num_items = random.randint(1, 2)
            for _ in range(num_items):
                item = generate_loot(rarity)
                if item:
                    loot.append(item)
        
        return loot


class CombatManager:
    """Manages combat encounters"""
    
    @staticmethod
    def start_combat(player: Player, enemy: Enemy) -> bool:
        """Start and manage a combat encounter"""
        combat = Combat(player, enemy)
        return combat.start_combat()
    
    @staticmethod
    def simulate_combat(player: Player, enemy: Enemy) -> Tuple[bool, str]:
        """Simulate combat without user input (for testing)"""
        combat = Combat(player, enemy)
        
        while player.is_alive() and enemy.is_alive():
            # Simple AI vs AI simulation
            if random.random() < 0.7:  # Player attacks 70% of time
                damage = max(1, player.get_total_attack() + random.randint(-2, 3))
                enemy.take_damage(damage)
            else:
                player_defending = True
            
            if enemy.is_alive():
                if random.random() < 0.8:  # Enemy attacks 80% of time
                    damage = max(1, enemy.get_attack_damage())
                    if player_defending:
                        damage = damage // 2
                    player.take_damage(damage)
        
        if player.is_alive():
            return True, "Victory"
        else:
            return False, "Defeat"
