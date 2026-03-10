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
        print(f"\n⚔️  LE COMBAT COMMENCE !")
        print(f"{'='*50}")
        print(f"{self.player.name} CONTRE {self.enemy.name}")
        print(f"{'='*50}")
        print(f"{self.player.get_stats()}")
        print(f"{self.enemy.get_stats()}")
        print(f"{'='*50}")
        
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn_count += 1
            self.player_defending = False
            self.enemy_defending = False
            
            print(f"\n--- TOUR {self.turn_count} ---")
            
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
        print(f"\nTour de {self.player.name} :")
        print("1. Attaquer")
        print("2. Défendre")
        print("3. Utiliser un objet")
        print("4. Fuir")
        
        while True:
            try:
                choice = input("Choisissez votre action (1-4) : ").strip()
                
                if choice == "1":
                    return self.player_attack()
                elif choice == "2":
                    return self.player_defend()
                elif choice == "3":
                    return self.player_use_item()
                elif choice == "4":
                    return self.player_flee()
                else:
                    print("Choix invalide ! Veuillez entrer 1 à 4.")
            except KeyboardInterrupt:
                print("\nCombat interrompu !")
                return True
        return False  # Should normally not be reached
    
    def player_attack(self) -> bool:
        """Player attacks enemy"""
        damage = self.player.get_total_attack()
        variance = random.randint(-2, 3)
        damage = max(1, damage + variance)
        
        # Apply enemy defense if not defending
        if self.enemy_defending:
            damage = max(1, damage // 2)
            print(f"🛡️  {self.enemy.name} se défend ! Dégâts réduits !")
        
        actual_damage = self.enemy.take_damage(damage)
        
        print(f"⚔️  {self.player.name} attaque {self.enemy.name} pour {actual_damage} dégâts !")
        
        if not self.enemy.is_alive():
            print(f"💀 {self.enemy.name} a été vaincu !")
            return True
        
        return False
    
    def player_defend(self) -> bool:
        """Player defends"""
        self.player_defending = True
        print(f"🛡️  {self.player.name} adopte une posture défensive !")
        return False
    
    def player_use_item(self) -> bool:
        """Player uses an item"""
        if not self.player.inventory.items:
            print("🎒 Vous n'avez aucun objet à utiliser !")
            return self.player_turn()  # Re-prompt
        
        print("\n🎒 Vos Objets :")
        for i, item in enumerate(self.player.inventory.items):
            if item.item_type == "consumable":
                quantity = f" x{item.quantity}" if item.stackable and item.quantity > 1 else ""
                print(f"{i+1}. {item.name}{quantity} - {item.get_info()}")
        
        while True:
            try:
                choice = input("Choisissez l'objet à utiliser (ou 0 pour annuler) : ").strip()
                
                if choice == "0":
                    return self.player_turn()  # Re-prompt
                
                item_index = int(choice) - 1
                if 0 <= item_index < len(self.player.inventory.items):
                    item = self.player.inventory.items[item_index]
                    if item.item_type == "consumable":
                        if self.player.use_item(item_index):
                            return False
                        else:
                            print("❌ Impossible d'utiliser cet objet !")
                    else:
                        print("❌ Cet objet ne peut pas être utilisé en combat !")
                else:
                    print("Numéro d'objet invalide !")
            except ValueError:
                print("Veuillez entrer un numéro valide !")
        return False  # Should normally not be reached
    
    def player_flee(self) -> bool:
        """Player attempts to flee"""
        self.flee_attempts += 1
        
        if self.flee_attempts >= self.max_flee_attempts:
            print("💨 Vous avez tenté de fuir trop de fois ! Vous devez vous battre !")
            return False
        
        flee_chance = 0.4 + (self.flee_attempts * 0.1)  # Increasing chance
        flee_chance = min(0.8, flee_chance)  # Max 80% chance
        
        if random.random() < flee_chance:
            print(f"💨 {self.player.name} a fui le combat avec succès !")
            return True
        else:
            print(f"❌ {self.player.name} n'a pas réussi à fuir !")
            return False
    
    def enemy_turn(self):
        """Handle enemy's turn"""
        action = self.enemy.choose_action(self.player)
        
        print(f"\nTour de {self.enemy.name} :")
        
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
            print(f"🛡️  {self.player.name} se défend ! Dégâts réduits !")
        
        actual_damage = self.player.take_damage(damage)
        
        print(f"⚔️  {self.enemy.name} attaque {self.player.name} pour {actual_damage} dégâts !")
        
        if not self.player.is_alive():
            print(f"💀 {self.player.name} a été vaincu !")
            return True
        
        return False
    
    def enemy_defend(self):
        """Enemy defends"""
        self.enemy_defending = True
        print(f"🛡️  {self.enemy.name} adopte une posture défensive !")
    
    def display_combat_status(self):
        """Display current combat status"""
        print(f"\n📊 STATUT DU COMBAT")
        print(f"{'='*30}")
        print(f"{self.player.name}: {self.player.hp}/{self.player.max_hp} PV")
        print(f"{self.enemy.name}: {self.enemy.hp}/{self.enemy.max_hp} PV")
        
        if self.player_defending:
            print(f"🛡️  {self.player.name} se défend")
        if self.enemy_defending:
            print(f"🛡️  {self.enemy.name} se défend")
    
    def resolve_combat(self) -> bool:
        """Resolve combat outcome and handle rewards"""
        print(f"\n{'='*50}")
        
        if self.player.is_alive():
            print(f"🎉 VICTOIRE ! {self.player.name} a vaincu {self.enemy.name} !")
            
            # Experience reward
            exp_gained = self.enemy.exp_reward
            leveled_up = self.player.gain_experience(exp_gained)
            
            print(f"📈 Vous avez gagné {exp_gained} points d'expérience !")
            
            # Loot drops
            loot = self.generate_loot()
            if loot:
                print(f"💰 {self.enemy.name} a fait tomber :")
                for item in loot:
                    if self.player.inventory.add_item(item):
                        print(f"   📦 {item.name}")
                    else:
                        print(f"   ❌ Inventaire plein ! Impossible de ramasser {item.name}")
            
            return True
        else:
            print(f"💀 DÉFAITE ! {self.player.name} a été vaincu par {self.enemy.name} !")
            print("💔 Vous avez perdu le combat...")
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
