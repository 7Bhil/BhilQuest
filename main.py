"""
BhilGame - A Terminal-Based RPG Adventure Game
Main game loop and user interface
"""

import os
import sys
import time
import random
from typing import Optional

# Import game modules
from character import Player, create_enemy
from world import World
from combat import CombatManager
from inventory import Inventory, create_health_potion, generate_loot
from story import StoryManager
from save import SaveManager, AutoSave


class Game:
    """Main game class"""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.world: Optional[World] = None
        self.story_manager: Optional[StoryManager] = None
        self.save_manager = SaveManager()
        self.auto_save = AutoSave(self.save_manager)
        self.running = True
        self.in_combat = False
        
        # Game colors (optional enhancement)
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self):
        """Print game title screen"""
        title = """
    ████████╗ █████╗ ███╗   ██╗██╗  ██╗    ██████╗ ███████╗ █████╗ ████████╗
    ╚══██╔══╝██╔══██╗████╗  ██║██║ ██╔╝    ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
       ██║   ███████║██╔██╗ ██║█████╔╝     ██████╔╝█████╗  ███████║   ██║   
       ██║   ██╔══██║██║╚██╗██║██╔═██╗     ██╔══██╗██╔══╝  ██╔══██║   ██║   
       ██║   ██║  ██║██║ ╚████║██║  ██╗    ██████╔╝███████╗██║  ██║   ██║   
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   
                                                                            
                           ADVENTURE GAME
        """
        print(self.colors['cyan'] + title + self.colors['reset'])
        print(self.colors['yellow'] + "                    A Terminal RPG Adventure" + self.colors['reset'])
        print("\n" + "="*60 + "\n")
    
    def print_with_delay(self, text: str, delay: float = 0.03):
        """Print text with typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def main_menu(self) -> str:
        """Display main menu and get user choice"""
        while True:
            self.clear_screen()
            self.print_title()
            
            print("📋 MAIN MENU")
            print("="*30)
            print("1. New Game")
            print("2. Continue Game")
            print("3. Quit")
            print("="*30)
            
            # Check if save file exists
            if not self.save_manager.has_save_file():
                print("⚠️  No save file found")
            
            choice = input("\nChoose your option (1-3): ").strip()
            
            if choice == "1":
                return "new"
            elif choice == "2":
                if self.save_manager.has_save_file():
                    return "continue"
                else:
                    print("❌ No save file found!")
                    input("Press Enter to continue...")
            elif choice == "3":
                return "quit"
            else:
                print("❌ Invalid choice! Please enter 1-3.")
                input("Press Enter to continue...")
    
    def create_new_game(self):
        """Initialize a new game"""
        self.clear_screen()
        self.print_title()
        
        print("🎮 CHARACTER CREATION")
        print("="*30)
        
        while True:
            name = input("Enter your character's name: ").strip()
            if name and len(name) > 0 and len(name) <= 20:
                break
            else:
                print("❌ Please enter a valid name (1-20 characters)")
        
        print(f"\nWelcome, {name}! Your adventure begins now...")
        input("Press Enter to continue...")
        
        # Initialize game components
        self.player = Player(name)
        self.world = World()
        self.story_manager = StoryManager()
        
        # Give starting items
        self.player.add_item(create_health_potion())
        self.player.add_item(create_health_potion())
        
        # Set starting location
        self.world.current_location_name = "village"
        self.player.current_location = "village"
        self.world.get_current_location().visited = True
        
        print(f"\n🎉 {name} the hero awakens in the peaceful village!")
        time.sleep(2)
    
    def load_game(self):
        """Load saved game"""
        save_data = self.save_manager.load_game()
        
        if save_data is None:
            return False
        
        try:
            self.player = self.save_manager.deserialize_player(save_data["player"])
            self.world = self.save_manager.deserialize_world(save_data["world"])
            self.story_manager = self.save_manager.deserialize_story(save_data["story"])
            
            print(f"\n🎉 Welcome back, {self.player.name}!")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Error loading save file: {e}")
            input("Press Enter to continue...")
            return False
    
    def game_loop(self):
        """Main game loop"""
        while self.running and self.player.is_alive():
            self.clear_screen()
            self.display_game_info()
            self.display_location_info()
            
            # Check for auto-save
            self.auto_save.auto_save(self.player, self.world, self.story_manager)
            
            # Handle exploration encounters
            if not self.in_combat:
                self.handle_exploration()
            
            # Get player action
            action = self.get_player_action()
            
            if action == "quit":
                self.handle_quit()
            elif action == "save":
                self.handle_save()
            elif action == "move":
                self.handle_movement()
            elif action == "explore":
                self.handle_exploration_action()
            elif action == "inventory":
                self.handle_inventory()
            elif action == "quests":
                self.handle_quests()
            elif action == "talk":
                self.handle_talk()
            elif action == "map":
                self.handle_map()
            elif action == "stats":
                self.handle_stats()
            elif action == "help":
                self.handle_help()
            else:
                print("❌ Invalid action!")
                input("Press Enter to continue...")
    
    def display_game_info(self):
        """Display basic game information"""
        print(f"📍 Location: {self.world.get_current_location().name}")
        print(f"⚔️  {self.player.get_stats()}")
        print(f"📦 Inventory: {len(self.player.inventory)}/20 slots")
        
        # Show story status
        story_status = self.story_manager.get_story_status()
        print(f"📖 {story_status}")
    
    def display_location_info(self):
        """Display current location information"""
        location = self.world.get_current_location()
        print(f"\n{location.get_description()}")
        
        # Show NPCs at location
        npcs = self.story_manager.get_npc_at_location(self.world.current_location_name)
        if npcs:
            print(f"\n👥 People here:")
            for npc in npcs:
                print(f"   • {npc.name}")
    
    def handle_exploration(self):
        """Handle random encounters while exploring"""
        if random.random() < 0.15:  # 15% chance of encounter
            enemy_type = self.world.get_current_location().check_for_enemy_encounter()
            if enemy_type:
                self.start_combat(enemy_type)
    
    def start_combat(self, enemy_type: str):
        """Start combat with an enemy"""
        enemy = create_enemy(enemy_type)
        
        print(f"\n⚠️  A wild {enemy.name} appears!")
        input("Press Enter to start combat...")
        
        self.in_combat = True
        victory = CombatManager.start_combat(self.player, enemy)
        self.in_combat = False
        
        if not victory:
            self.game_over()
        else:
            # Update quest progress for kills
            completed_quests = self.story_manager.update_quest_progress(
                self.player, "kill", enemy_type, 1
            )
            
            # Show quest completions
            for quest, rewards in completed_quests:
                print(f"\n🎉 QUEST COMPLETED: {quest.name}")
                if rewards:
                    print(f"🎁 Rewards: {', '.join(rewards)}")
                input("Press Enter to continue...")
            
            # Advance story
            if enemy_type == "goblin":
                self.story_manager.advance_story("first_blood")
    
    def get_player_action(self) -> str:
        """Get player's action choice"""
        print(f"\n🎮 What would you like to do?")
        print("1. Move/Travel")
        print("2. Explore Area")
        print("3. Inventory")
        print("4. Quests")
        print("5. Talk to NPC")
        print("6. View Map")
        print("7. Character Stats")
        print("8. Save Game")
        print("9. Help")
        print("0. Quit Game")
        
        choice = input("\nEnter your choice (0-9): ").strip()
        
        actions = {
            "1": "move",
            "2": "explore", 
            "3": "inventory",
            "4": "quests",
            "5": "talk",
            "6": "map",
            "7": "stats",
            "8": "save",
            "9": "help",
            "0": "quit"
        }
        
        return actions.get(choice, "invalid")
    
    def handle_movement(self):
        """Handle player movement"""
        directions = self.world.get_available_directions()
        
        if not directions:
            print("❌ There are no exits from this location!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🧭 Available directions:")
        for i, direction in enumerate(directions, 1):
            target_location = self.world.get_current_location().connections[direction]
            print(f"{i}. {direction.upper()} to {target_location}")
        
        try:
            choice = int(input(f"\nChoose direction (1-{len(directions)}): ")) - 1
            if 0 <= choice < len(directions):
                direction = directions[choice]
                success, message = self.world.move_to_location(direction)
                
                if success:
                    print(f"✅ {message}")
                    self.player.current_location = self.world.current_location_name
                    
                    # Show new location description
                    new_location = self.world.get_current_location()
                    if not new_location.visited:
                        print(f"\n{new_location.get_description()}")
                        input("Press Enter to continue...")
                else:
                    print(f"❌ {message}")
                    input("Press Enter to continue...")
            else:
                print("❌ Invalid direction!")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a valid number!")
            input("Press Enter to continue...")
    
    def handle_exploration_action(self):
        """Handle active exploration"""
        print(f"\n🔍 Exploring {self.world.get_current_location().name}...")
        
        # Check for enemy encounter
        enemy_type = self.world.get_current_location().check_for_enemy_encounter()
        if enemy_type:
            self.start_combat(enemy_type)
        else:
            # Chance to find items
            if random.random() < 0.3:  # 30% chance
                item = generate_loot("common")
                if item:
                    print(f"💰 You found: {item.name}")
                    if self.player.inventory.add_item(item):
                        print("📦 Item added to inventory!")
                    else:
                        print("❌ Inventory full! Cannot pick up item.")
            else:
                print("🔍 You explore the area but find nothing of interest.")
            
            input("Press Enter to continue...")
    
    def handle_inventory(self):
        """Handle inventory management"""
        self.clear_screen()
        print(self.player.inventory.get_inventory_display())
        
        if self.player.inventory.items:
            print(f"\nOptions:")
            print("1. Use Item")
            print("2. Equip Weapon/Armor")
            print("3. Back to game")
            
            choice = input("\nChoose option (1-3): ").strip()
            
            if choice == "1":
                self.use_inventory_item()
            elif choice == "2":
                self.equip_item()
        
        input("\nPress Enter to continue...")
    
    def use_inventory_item(self):
        """Handle using items from inventory"""
        consumables = self.player.inventory.get_items_by_type("consumable")
        
        if not consumables:
            print("❌ No consumable items available!")
            return
        
        print("\n🧪 Consumable Items:")
        for i, item in enumerate(consumables, 1):
            quantity = f" x{item.quantity}" if item.stackable and item.quantity > 1 else ""
            print(f"{i}. {item.name}{quantity} - {item.get_info()}")
        
        try:
            choice = int(input("\nChoose item to use (0 to cancel): ")) - 1
            if 0 <= choice < len(consumables):
                item = consumables[choice]
                # Find item in inventory and use it
                for i, inv_item in enumerate(self.player.inventory.items):
                    if inv_item.name == item.name:
                        if self.player.use_item(i):
                            print(f"✅ Used {item.name}!")
                        break
            elif choice == -1:
                return
            else:
                print("❌ Invalid item!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def equip_item(self):
        """Handle equipping items"""
        equipment = self.player.inventory.get_items_by_type("weapon") + \
                   self.player.inventory.get_items_by_type("armor")
        
        if not equipment:
            print("❌ No equipment available!")
            return
        
        print("\n⚔️  Equipment:")
        for i, item in enumerate(equipment, 1):
            print(f"{i}. {item.name} - {item.get_info()}")
        
        try:
            choice = int(input("\nChoose item to equip (0 to cancel): ")) - 1
            if 0 <= choice < len(equipment):
                item = equipment[choice]
                if item.item_type == "weapon":
                    self.player.equip_weapon(item)
                elif item.item_type == "armor":
                    self.player.equip_armor(item)
            elif choice == -1:
                return
            else:
                print("❌ Invalid item!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def handle_quests(self):
        """Handle quest interface"""
        self.clear_screen()
        print(self.story_manager.get_quests_display(self.player))
        input("\nPress Enter to continue...")
    
    def handle_talk(self):
        """Handle talking to NPCs"""
        npcs = self.story_manager.get_npc_at_location(self.world.current_location_name)
        
        if not npcs:
            print("❌ There's no one to talk to here!")
            input("Press Enter to continue...")
            return
        
        print(f"\n👥 Who would you like to talk to?")
        for i, npc in enumerate(npcs, 1):
            print(f"{i}. {npc.name}")
        
        try:
            choice = int(input("\nChoose person (0 to cancel): ")) - 1
            if 0 <= choice < len(npcs):
                npc = npcs[choice]
                self.conversation_with_npc(npc)
            elif choice == -1:
                return
            else:
                print("❌ Invalid person!")
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("Press Enter to continue...")
    
    def conversation_with_npc(self, npc):
        """Handle conversation with an NPC"""
        print(f"\n💬 {npc.name}:")
        print(f"   {npc.description}")
        
        # Get appropriate dialogue
        if npc.has_available_quests(self.player):
            dialogue = npc.get_dialogue("greeting")
            print(f"\n{npc.name}: {dialogue}")
            
            # Offer quest
            quest = npc.get_next_quest()
            if quest:
                print(f"\n📜 Quest Offer: {quest.name}")
                print(f"   {quest.description}")
                print(f"   Progress:\n{quest.get_progress_text()}")
                
                accept = input("\nAccept this quest? (y/n): ").strip().lower()
                if accept in ['y', 'yes']:
                    print(f"\n{npc.name}: {npc.get_dialogue('quest_accepted')}")
                    # Note: In a more complex system, we'd track quest acceptance
                else:
                    print(f"\n{npc.name}: Perhaps another time then...")
        else:
            dialogue = npc.get_dialogue("no_quests")
            print(f"\n{npc.name}: {dialogue}")
    
    def handle_map(self):
        """Handle world map display"""
        self.clear_screen()
        print(self.world.get_world_map())
        input("\nPress Enter to continue...")
    
    def handle_stats(self):
        """Handle character stats display"""
        self.clear_screen()
        print(self.player.get_detailed_stats())
        input("\nPress Enter to continue...")
    
    def handle_save(self):
        """Handle game saving"""
        if self.save_manager.save_game(self.player, self.world, self.story_manager):
            print("✅ Game saved successfully!")
        else:
            print("❌ Failed to save game!")
        input("Press Enter to continue...")
    
    def handle_quit(self):
        """Handle quitting the game"""
        print("\nAre you sure you want to quit?")
        print("1. Save and Quit")
        print("2. Quit without Saving")
        print("3. Cancel")
        
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == "1":
            self.handle_save()
            self.running = False
        elif choice == "2":
            self.running = False
        elif choice == "3":
            return
        else:
            print("❌ Invalid choice!")
    
    def handle_help(self):
        """Display help information"""
        help_text = """
🎮 BHILGAME - HELP GUIDE
========================

MOVEMENT:
• Use the Move option to travel between locations
• Choose from available directions (N, S, E, W, etc.)

COMBAT:
• Combat is turn-based and happens automatically during exploration
• Choose actions: Attack, Defend, Use Item, or Flee
• Different enemies have different difficulty levels

INVENTORY:
• Manage your items through the Inventory menu
• Use consumables like health potions
• Equip weapons and armor to improve stats

QUESTS:
• Talk to NPCs to receive quests
• Complete quests by meeting requirements
• Earn experience and rewards for completed quests

EXPLORATION:
• Explore areas to find items and encounter enemies
• Different locations have different dangers and rewards
• Visit all locations to discover the world

TIPS:
• Save your game progress regularly
• Stock up on healing potions before dangerous areas
• Complete quests to gain experience and rewards
• Explore thoroughly to find valuable items

Good luck, hero!
        """
        print(help_text)
        input("\nPress Enter to continue...")
    
    def game_over(self):
        """Handle game over"""
        self.clear_screen()
        print("""
    ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗██╗     ██╗
    ██╔══██╗██╔══██╗████╗ ████║██╔════╝    ██╔════╝██║     ██║
    ██████╔╝███████║██╔████╔██║█████╗      ██║     ██║     ██║
    ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝      ██║     ██║     ██║
    ██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╗███████╗██║
    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝╚══════╝╚═╝
                                                                
                        GAME OVER
        """)
        
        print(f"\n💀 {self.player.name} has fallen in battle...")
        print(f"📊 Final Stats:")
        print(f"   Level: {self.player.level}")
        print(f"   Quests Completed: {len(self.player.quests_completed)}")
        print(f"   Locations Visited: {sum(1 for loc in self.world.locations.values() if loc.visited)}")
        
        input("\nPress Enter to return to main menu...")
        self.running = False
    
    def run(self):
        """Run the game"""
        while True:
            menu_choice = self.main_menu()
            
            if menu_choice == "quit":
                print("\n👋 Thanks for playing BhilGame!")
                break
            elif menu_choice == "new":
                self.create_new_game()
                self.game_loop()
            elif menu_choice == "continue":
                if self.load_game():
                    self.game_loop()
                else:
                    continue
            
            if not self.running:
                self.running = True  # Reset for next game


def main():
    """Main entry point"""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing BhilGame!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
