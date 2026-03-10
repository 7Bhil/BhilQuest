"""
BhilQuest - Jeu RPG d'Aventure Terminal avec Système i18n
Version multilingue professionnelle avec gestion centralisée des traductions

Créé par: Bhilal CHITOU (Bhil€)
Email: 7bhilal.chitou7@gmail.com
GitHub: https://github.com/7Bhil
"""

import os
import sys
import time
import random
from typing import Optional

# Import du système de langue
from lang import set_language, t, get_language

# Import des modules de jeu
from character import Player, create_enemy
from world import World
from combat import CombatManager
from inventory import Inventory, create_health_potion, generate_loot
from story import StoryManager
from save import SaveManager, AutoSave


class Game:
    """Classe principale du jeu avec support i18n"""
    
    def __init__(self, language: str = "en"):
        # Configure la langue
        set_language(language)
        
        self.player: Optional[Player] = None
        self.world: Optional[World] = None
        self.story_manager: Optional[StoryManager] = None
        self.save_manager = SaveManager()
        self.auto_save = AutoSave(self.save_manager)
        self.running = True
        self.in_combat = False
        
        # Couleurs du jeu
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
        """Efface l'écran du terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self):
        """Affiche l'écran-titre du jeu"""
        title = """
██████╗ ██╗  ██╗██╗██╗      ██████╗  ██╗   ██╗███████╗███████╗████████╗
██╔══██╗██║  ██║██║██║     ██╔═══██╗ ██║   ██║██╔════╝██╔════╝╚══██╔══╝
██████╔╝███████║██║██║     ██║   ██║ ██║   ██║█████╗  ███████╗   ██║   
██╔══██╗██╔══██║██║██║     ██║▄▄ ██║ ██║   ██║██╔══╝  ╚════██║   ██║   
██████╔╝██║  ██║██║███████╗╚██████╔╝ ╚██████╔╝███████╗███████║   ██║   
╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝ ╚══▀▀═╝   ╚═════╝ ╚══════╝╚══════╝   ╚═╝    
                                                                                                                 
                           {created_by}
        
                    {game_subtitle}
        """.format(
            created_by=t('CREATED_BY'),
            game_subtitle=t('GAME_SUBTITLE')
        )
        
        print(self.colors['cyan'] + title + self.colors['reset'])
        print(self.colors['yellow'] + f"                    {t('GAME_SUBTITLE')}" + self.colors['reset'])
        print("\n" + "="*60 + "\n")
    
    def print_with_delay(self, text: str, delay: float = 0.03):
        """Affiche le texte avec effet machine à écrire"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def main_menu(self) -> str:
        """Affiche le menu principal et obtient le choix de l'utilisateur"""
        while True:
            self.clear_screen()
            self.print_title()
            
            print(f"📋 {t('MAIN_MENU_TITLE')}")
            print("="*30)
            print(f"1. {t('NEW_GAME')}")
            print(f"2. {t('CONTINUE_GAME')}")
            print(f"3. {t('QUIT_GAME')}")
            print("="*30)
            
            # Vérifie si un fichier de sauvegarde existe
            if not self.save_manager.has_save_file():
                print(f"⚠️  {t('NO_SAVE_FOUND')}")
            
            choice = input(f"\n{t('CHOOSE_OPTION')}").strip()
            
            if choice == "1":
                return "new"
            elif choice == "2":
                if self.save_manager.has_save_file():
                    return "continue"
                else:
                    print(f"❌ {t('NO_SAVE_FOUND')} !")
                    input(t('PRESS_ENTER'))
            elif choice == "3":
                return "quit"
            else:
                print(f"❌ {t('INVALID_CHOICE')}")
                input(t('PRESS_ENTER'))
    
    def create_new_game(self):
        """Initialise une nouvelle partie"""
        self.clear_screen()
        self.print_title()
        
        print(f"🎮 {t('CHARACTER_CREATION')}")
        print("="*30)
        
        while True:
            name = input(t('ENTER_NAME')).strip()
            if name and len(name) > 0 and len(name) <= 20:
                break
            else:
                print(f"❌ {t('VALID_NAME')}")
        
        print(f"\n{t('WELCOME_MESSAGE', name=name)}")
        input(t('PRESS_ENTER'))
        
        # Initialise les composants du jeu
        self.player = Player(name)
        self.world = World()
        self.story_manager = StoryManager()
        
        # Donne les objets de départ
        self.player.add_item(create_health_potion())
        self.player.add_item(create_health_potion())
        
        # Définit le lieu de départ
        self.world.current_location_name = "village"
        self.player.current_location = "village"
        self.world.get_current_location().visited = True
        
        print(f"\n🎉 {t('HERO_AWAKENS', name=name)}")
        time.sleep(2)
    
    def load_game(self):
        """Charge une partie sauvegardée"""
        save_data = self.save_manager.load_game()
        
        if save_data is None:
            return False
        
        try:
            self.player = self.save_manager.deserialize_player(save_data["player"])
            self.world = self.save_manager.deserialize_world(save_data["world"])
            self.story_manager = self.save_manager.deserialize_story(save_data["story"])
            
            print(f"\n🎉 {t('LOAD_SUCCESS', timestamp=save_data.get('timestamp', 'Unknown'))}")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ {t('LOAD_FAILED', error=e)}")
            input(t('PRESS_ENTER'))
            return False
    
    def game_loop(self):
        """Boucle de jeu principale"""
        while self.running and self.player.is_alive():
            self.clear_screen()
            self.display_game_info()
            self.display_location_info()
            
            # Vérifie la sauvegarde automatique
            self.auto_save.auto_save(self.player, self.world, self.story_manager)
            
            # Gère les rencontres d'exploration
            if not self.in_combat:
                self.handle_exploration()
            
            # Obtient l'action du joueur
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
                print("❌ Action invalide !")
                input(t('PRESS_ENTER'))
    
    def display_game_info(self):
        """Affiche les informations de base du jeu"""
        location = self.world.get_current_location()
        print(f"📍 {t('LOCATION')}: {location.name}")
        print(f"⚔️  {self.player.get_stats()}")
        print(f"📦 {t('INVENTORY')}: {len(self.player.inventory.items)}/20 {t('SLOTS')}")
        
        # Affiche le statut de l'histoire
        story_status = self.story_manager.get_story_status()
        print(f"📖 {story_status}")
    
    def display_location_info(self):
        """Affiche les informations du lieu actuel"""
        location = self.world.get_current_location()
        
        # Utilise les traductions pour les descriptions
        desc = f"\n📍 {location.name}\n"
        desc += f"{'='*len(location.name)}\n"
        
        # Traduit la description selon la langue
        if get_language() == "fr":
            # Utilise les descriptions françaises
            fr_descriptions = {
                "Peaceful Village": t('VILLAGE_DESC'),
                "Mystic Forest": t('FOREST_DESC'),
                "Deep Forest": t('DEEP_FOREST_DESC'),
                "Ancient Ruins": t('RUINS_DESC'),
                "Abandoned Temple": t('TEMPLE_DESC'),
                "Dungeon Entrance": t('DUNGEON_ENTRANCE_DESC'),
                "Dungeon Halls": t('DUNGEON_HALLS_DESC'),
                "Dungeon Depths": t('DUNGEON_DEPTHS_DESC'),
                "Mountain Pass": t('MOUNTAIN_PASS_DESC')
            }
            desc += fr_descriptions.get(location.name, location.description) + "\n\n"
        else:
            desc += location.description + "\n\n"
        
        if location.connections:
            desc += f"🧭 {t('EXITS')}: "
            exits = []
            for direction, loc_name in location.connections.items():
                direction_text = t(direction.upper()) if direction.upper() in ['NORTH', 'SOUTH', 'EAST', 'WEST', 'UP', 'DOWN'] else direction.upper()
                exits.append(f"{direction_text} {t('TO')} {loc_name}")
            desc += ", ".join(exits) + "\n"
        
        # Affiche les PNJ
        npcs = self.story_manager.get_npc_at_location(self.world.current_location_name)
        if npcs and not location.visited:
            npc_names = [npc.name for npc in npcs]
            desc += f"\n👥 {t('PEOPLE_HERE')}: {', '.join(npc_names)}"
        
        print(desc)
    
    def handle_exploration(self):
        """Gère les rencontres aléatoires lors de l'exploration"""
        if random.random() < 0.15:  # 15% de chance de rencontre
            enemy_type = self.world.get_current_location().check_for_enemy_encounter()
            if enemy_type:
                self.start_combat(enemy_type)
    
    def start_combat(self, enemy_type: str):
        """Commence un combat avec un ennemi"""
        enemy = create_enemy(enemy_type)
        
        print(f"\n⚠️  {t('ENEMY_APPEARS', enemy_name=enemy.name)}")
        input(t('START_COMBAT'))
        
        self.in_combat = True
        victory = CombatManager.start_combat(self.player, enemy)
        self.in_combat = False
        
        if not victory:
            self.game_over()
        else:
            # Met à jour la progression des quêtes pour les tués
            completed_quests = self.story_manager.update_quest_progress(
                self.player, "kill", enemy_type, 1
            )
            
            # Affiche les complétions de quêtes
            for quest, rewards in completed_quests:
                print(f"\n🎉 {t('QUEST_COMPLETED')}: {quest.name}")
                if rewards:
                    print(f"🎁 {t('QUEST_REWARDS')}: {', '.join(rewards)}")
                input(t('PRESS_ENTER'))
            
            # Fait progresser l'histoire
            if enemy_type == "goblin":
                self.story_manager.advance_story("first_blood")
    
    def get_player_action(self) -> str:
        """Obtient le choix d'action du joueur"""
        print(f"\n🎮 {t('WHAT_DO')}")
        print(f"1. {t('MOVE_TRAVEL')}")
        print(f"2. {t('EXPLORE_AREA')}")
        print(f"3. {t('INVENTORY')}")
        print(f"4. {t('QUESTS')}")
        print(f"5. {t('TALK_NPC')}")
        print(f"6. {t('VIEW_MAP')}")
        print(f"7. {t('CHARACTER_STATS')}")
        print(f"8. {t('SAVE_GAME')}")
        print(f"9. {t('HELP')}")
        print(f"0. {t('QUIT')}")
        
        choice = input(f"\n{t('ENTER_CHOICE')}").strip()
        
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
        """Gère le déplacement du joueur"""
        directions = self.world.get_available_directions()
        
        if not directions:
            print(f"❌ {t('NO_EXITS')} !")
            input(t('PRESS_ENTER'))
            return
        
        print(f"\n🧭 {t('AVAILABLE_DIRECTIONS')}:")
        for i, direction in enumerate(directions, 1):
            target_location = self.world.get_current_location().connections[direction]
            direction_text = t(direction.upper()) if direction.upper() in ['NORTH', 'SOUTH', 'EAST', 'WEST', 'UP', 'DOWN'] else direction.upper()
            print(f"{i}. {direction_text} {t('TO')} {target_location}")
        
        try:
            choice = int(input(f"\n{t('CHOOSE_DIRECTION', count=len(directions))}: ")) - 1
            if 0 <= choice < len(directions):
                direction = directions[choice]
                success, message = self.world.move_to_location(direction)
                
                if success:
                    print(f"✅ {message}")
                    self.player.current_location = self.world.current_location_name
                    
                    # Affiche la description du nouveau lieu
                    new_location = self.world.get_current_location()
                    if not new_location.visited:
                        self.display_location_info()
                        input(t('PRESS_ENTER'))
                else:
                    print(f"❌ {message}")
                    input(t('PRESS_ENTER'))
            else:
                print(f"❌ {t('INVALID_DIRECTION')} !")
                input(t('PRESS_ENTER'))
        except ValueError:
            print(f"❌ {t('ENTER_NUMBER')} !")
            input(t('PRESS_ENTER'))
    
    def handle_exploration_action(self):
        """Gère l'exploration active"""
        location = self.world.get_current_location()
        print(f"\n🔍 {t('EXPLORING', location=location.name)}...")
        
        # Vérifie les rencontres d'ennemis
        enemy_type = location.check_for_enemy_encounter()
        if enemy_type:
            self.start_combat(enemy_type)
        else:
            # Chance de trouver des objets
            if random.random() < 0.3:  # 30% de chance
                item = generate_loot("common")
                if item:
                    print(f"💰 {t('FOUND_ITEM', item_name=item.name)}")
                    if self.player.inventory.add_item(item):
                        print(f"📦 {t('ITEM_ADDED')} !")
                    else:
                        print(f"❌ {t('INVENTORY_FULL')} !")
            else:
                print(f"🔍 {t('NOTHING_FOUND')}.")
            
            input(t('PRESS_ENTER'))
    
    def handle_inventory(self):
        """Gère la gestion de l'inventaire"""
        self.clear_screen()
        print(self.player.inventory.get_inventory_display())
        
        if self.player.inventory.items:
            print(f"\nOptions:")
            print(f"1. {t('USE_ITEM_OPTION')}")
            print(f"2. {t('EQUIP_OPTION')}")
            print(f"3. {t('BACK_GAME')}")
            
            choice = input(f"\n{t('CHOOSE_OPTION')} (1-3): ").strip()
            
            if choice == "1":
                self.use_inventory_item()
            elif choice == "2":
                self.equip_item()
        
        input(f"\n{t('PRESS_ENTER')}")
    
    def use_inventory_item(self):
        """Gère l'utilisation d'objets de l'inventaire"""
        consumables = self.player.inventory.get_items_by_type("consumable")
        
        if not consumables:
            print(f"❌ {t('NO_CONSUMABLES')} !")
            return
        
        print(f"\n🧪 {t('CONSUMABLE_ITEMS')}:")
        for i, item in enumerate(consumables, 1):
            quantity = f" x{item.quantity}" if item.stackable and item.quantity > 1 else ""
            print(f"{i}. {item.name}{quantity} - {item.get_info()}")
        
        try:
            choice = int(input(f"\n{t('CHOOSE_ITEM_USE')}")) - 1
            if 0 <= choice < len(consumables):
                item = consumables[choice]
                # Trouve l'objet dans l'inventaire et l'utilise
                for i, inv_item in enumerate(self.player.inventory.items):
                    if inv_item.name == item.name:
                        if self.player.use_item(i):
                            print(f"✅ {t('USED_ITEM', item_name=item.name)} !")
                        break
            elif choice == -1:
                return
            else:
                print(f"❌ {t('INVALID_ITEM')} !")
        except ValueError:
            print(f"❌ {t('ENTER_NUMBER')} !")
    
    def equip_item(self):
        """Gère l'équipement d'objets"""
        equipment = self.player.inventory.get_items_by_type("weapon") + \
                   self.player.inventory.get_items_by_type("armor")
        
        if not equipment:
            print(f"❌ {t('NO_EQUIPMENT')} !")
            return
        
        print(f"\n⚔️  {t('EQUIPMENT')}:")
        for i, item in enumerate(equipment, 1):
            print(f"{i}. {item.name} - {item.get_info()}")
        
        try:
            choice = int(input(f"\n{t('CHOOSE_ITEM_EQUIP')}")) - 1
            if 0 <= choice < len(equipment):
                item = equipment[choice]
                if item.item_type == "weapon":
                    self.player.equip_weapon(item)
                elif item.item_type == "armor":
                    self.player.equip_armor(item)
            elif choice == -1:
                return
            else:
                print(f"❌ {t('INVALID_ITEM')} !")
        except ValueError:
            print(f"❌ {t('ENTER_NUMBER')} !")
    
    def handle_quests(self):
        """Gère l'interface des quêtes"""
        self.clear_screen()
        print(self.story_manager.get_quests_display(self.player))
        input(f"\n{t('PRESS_ENTER')}")
    
    def handle_talk(self):
        """Gère les discussions avec les PNJ"""
        npcs = self.story_manager.get_npc_at_location(self.world.current_location_name)
        
        if not npcs:
            print(f"❌ {t('NO_ONE_TALK')} !")
            input(t('PRESS_ENTER'))
            return
        
        print(f"\n👥 {t('TALK_TO')}")
        for i, npc in enumerate(npcs, 1):
            print(f"{i}. {npc.name}")
        
        try:
            choice = int(input(f"\n{t('CHOOSE_PERSON')}")) - 1
            if 0 <= choice < len(npcs):
                npc = npcs[choice]
                self.conversation_with_npc(npc)
            elif choice == -1:
                return
            else:
                print(f"❌ {t('INVALID_PERSON')} !")
        except ValueError:
            print(f"❌ {t('ENTER_NUMBER')} !")
        
        input(t('PRESS_ENTER'))
    
    def conversation_with_npc(self, npc):
        """Gère la conversation avec un PNJ"""
        print(f"\n💬 {t('CONVERSATION_WITH', npc_name=npc.name)}")
        print(f"   {t('DESCRIPTION', npc_name=npc.name, description=npc.description)}")
        
        # Obtient le dialogue approprié
        if npc.has_available_quests(self.player):
            dialogue = npc.get_dialogue("greeting")
            print(f"\n{npc.name}: {dialogue}")
            
            # Offre une quête
            quest = npc.get_next_quest()
            if quest:
                print(f"\n📜 {t('QUEST_OFFER')}: {quest.name}")
                print(f"   {quest.description}")
                print(f"   {t('QUEST_PROGRESS')}:\n{quest.get_progress_text()}")
                
                accept = input(f"\n{t('ACCEPT_QUEST')}").strip().lower()
                if accept in ['y', 'yes', 'o', 'oui']:
                    print(f"\n{npc.name}: {npc.get_dialogue('quest_accepted')}")
                else:
                    print(f"\n{npc.name}: {t('QUEST_ACCEPTED')}")
        else:
            dialogue = npc.get_dialogue("no_quests")
            print(f"\n{npc.name}: {dialogue}")
    
    def handle_map(self):
        """Gère l'affichage de la carte du monde"""
        self.clear_screen()
        print(self.world.get_world_map())
        input(f"\n{t('PRESS_ENTER')}")
    
    def handle_stats(self):
        """Gère l'affichage des statistiques du personnage"""
        self.clear_screen()
        print(self.player.get_detailed_stats())
        input(f"\n{t('PRESS_ENTER')}")
    
    def handle_save(self):
        """Gère la sauvegarde du jeu"""
        if self.save_manager.save_game(self.player, self.world, self.story_manager):
            print(f"✅ {t('SAVE_SUCCESS')} !")
        else:
            print(f"❌ {t('SAVE_FAILED')} !")
        input(t('PRESS_ENTER'))
    
    def handle_quit(self):
        """Gère le fait de quitter le jeu"""
        print(f"\n{t('SURE_QUIT')}")
        print(f"1. {t('SAVE_AND_QUIT')}")
        print(f"2. {t('QUIT_WITHOUT_SAVING')}")
        print(f"3. {t('CANCEL')}")
        
        choice = input(f"\n{t('CHOOSE_OPTION_QUIT')}").strip()
        
        if choice == "1":
            self.handle_save()
            self.running = False
        elif choice == "2":
            self.running = False
        elif choice == "3":
            return
        else:
            print(f"❌ {t('INVALID_CHOICE')} !")
    
    def handle_help(self):
        """Affiche les informations d'aide"""
        help_text = f"""
🎮 {t('GAME_TITLE')} - {t('HELP_GUIDE')}
========================

{t('MOVEMENT_SECTION')}:
{t('MOVEMENT_TEXT')}

{t('COMBAT_SECTION')}:
{t('COMBAT_TEXT')}

{t('INVENTORY_SECTION')}:
{t('INVENTORY_TEXT')}

{t('QUESTS_SECTION')}:
{t('QUESTS_TEXT')}

{t('EXPLORATION_SECTION')}:
{t('EXPLORATION_TEXT')}

{t('TIPS_SECTION')}:
{t('TIPS_TEXT')}

{t('GOOD_LUCK')} !
        """
        print(help_text)
        input(f"\n{t('PRESS_ENTER')}")
    
    def game_over(self):
        """Gère la fin du jeu"""
        self.clear_screen()
        print("""
    ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗██╗     ██╗
    ██╔══██╗██╔══██╗████╗ ████║██╔════╝    ██╔════╝██║     ██║
    ██████╔╝███████║██╔████╔██║█████╗      ██║     ██║     ██║
    ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝      ██║     ██║     ██║
    ██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╗███████╗██║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝╚═╝
                                                                
                        {game_over_title}
        """.format(game_over_title=t('GAME_OVER_TITLE')))
        
        print(f"\n💀 {t('HAS_FALLEN', name=self.player.name)}")
        print(f"📊 {t('FINAL_STATS')}:")
        print(f"   {t('LEVEL')}: {self.player.level}")
        print(f"   {t('QUESTS_COMPLETED_STAT')}: {len(self.player.quests_completed)}")
        print(f"   {t('LOCATIONS_VISITED')}: {sum(1 for loc in self.world.locations.values() if loc.visited)}")
        
        input(f"\n{t('RETURN_MENU')}")
        self.running = False
    
    def run(self):
        """Exécute le jeu"""
        while True:
            menu_choice = self.main_menu()
            
            if menu_choice == "quit":
                print(f"\n👋 {t('THANKS_PLAYING')}!")
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
                self.running = True  # Réinitialise pour la prochaine partie


def main():
    """Point d'entrée principal"""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print(f"\n\n👋 {t('THANKS_PLAYING')}!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ {t('ERROR_OCCURRED', error=e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
