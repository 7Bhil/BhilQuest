"""
BhilQuest - Jeu RPG d'Aventure Terminal
Boucle de jeu principal et interface utilisateur

Créé par: Bhilal CHITOU (Bhil€)
Email: 7bhilal.chitou7@gmail.com
GitHub: https://github.com/7Bhil
"""

import os
import sys
import time
import random
from typing import Optional

# Import des modules de jeu
from character import Player, create_enemy
from world import World
from combat import CombatManager
from inventory import Inventory, create_health_potion, generate_loot
from story import StoryManager
from save import SaveManager, AutoSave


class Jeu:
    """Classe principale du jeu"""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.world: Optional[World] = None
        self.story_manager: Optional[StoryManager] = None
        self.save_manager = SaveManager()
        self.auto_save = AutoSave(self.save_manager)
        self.running = True
        self.in_combat = False
        
        # Couleurs du jeu (amélioration optionnelle)
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
                                                                                                                 
                           créé par Bhilal. CHITOU (Bhil€)
        
                    Jeu RPG d'Aventure Terminal
        """
        print(self.colors['cyan'] + title + self.colors['reset'])
        print(self.colors['yellow'] + "                    Une Aventure RPG Terminal" + self.colors['reset'])
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
            
            print("📋 MENU PRINCIPAL")
            print("="*30)
            print("1. Nouvelle Partie")
            print("2. Continuer Partie")
            print("3. Quitter")
            print("="*30)
            
            # Vérifie si un fichier de sauvegarde existe
            if not self.save_manager.has_save_file():
                print("⚠️  Aucune sauvegarde trouvée")
            
            choice = input("\nChoisissez votre option (1-3): ").strip()
            
            if choice == "1":
                return "new"
            elif choice == "2":
                if self.save_manager.has_save_file():
                    return "continue"
                else:
                    print("❌ Aucune sauvegarde trouvée !")
                    input("Appuyez sur Entrée pour continuer...")
            elif choice == "3":
                return "quit"
            else:
                print("❌ Choix invalide ! Veuillez entrer 1-3.")
                input("Appuyez sur Entrée pour continuer...")
    
    def create_new_game(self):
        """Initialise une nouvelle partie"""
        self.clear_screen()
        self.print_title()
        
        print("🎮 CRÉATION DE PERSONNAGE")
        print("="*30)
        
        while True:
            name = input("Entrez le nom de votre personnage: ").strip()
            if name and len(name) > 0 and len(name) <= 20:
                break
            else:
                print("❌ Veuillez entrer un nom valide (1-20 caractères)")
        
        print(f"\nBienvenue, {name} ! Votre aventure commence maintenant...")
        input("Appuyez sur Entrée pour continuer...")
        
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
        
        print(f"\n🎉 {name} le héros se réveille dans le village paisible !")
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
            
            print(f"\n🎉 Bon retour, {self.player.name} !")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement de la sauvegarde: {e}")
            input("Appuyez sur Entrée pour continuer...")
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
                input("Appuyez sur Entrée pour continuer...")
    
    def display_game_info(self):
        """Affiche les informations de base du jeu"""
        print(f"📍 Lieu: {self.world.get_current_location().name}")
        print(f"⚔️  {self.player.get_stats()}")
        print(f"📦 Inventaire: {len(self.player.inventory)}/20 emplacements")
        
        # Affiche le statut de l'histoire
        story_status = self.story_manager.get_story_status()
        print(f"📖 {story_status}")
    
    def display_location_info(self):
        """Affiche les informations du lieu actuel"""
        location = self.world.get_current_location()
        print(f"\n{location.get_description()}")
        
        # Affiche les PNJ au lieu
        npcs = self.story_manager.get_npc_at_location(self.world.current_location_name)
        if npcs:
            print(f"\n👥 Personnes ici:")
            for npc in npcs:
                print(f"   • {npc.name}")
    
    def handle_exploration(self):
        """Gère les rencontres aléatoires lors de l'exploration"""
        if random.random() < 0.15:  # 15% de chance de rencontre
            enemy_type = self.world.get_current_location().check_for_enemy_encounter()
            if enemy_type:
                self.start_combat(enemy_type)
    
    def start_combat(self, enemy_type: str):
        """Commence un combat avec un ennemi"""
        enemy = create_enemy(enemy_type)
        
        print(f"\n⚠️  Un {enemy.name} sauvage apparaît !")
        input("Appuyez sur Entrée pour commencer le combat...")
        
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
                print(f"\n🎉 QUÊTE TERMINÉE: {quest.name}")
                if rewards:
                    print(f"🎁 Récompenses: {', '.join(rewards)}")
                input("Appuyez sur Entrée pour continuer...")
            
            # Fait progresser l'histoire
            if enemy_type == "goblin":
                self.story_manager.advance_story("first_blood")
    
    def get_player_action(self) -> str:
        """Obtient le choix d'action du joueur"""
        print(f"\n🎮 Que voulez-vous faire ?")
        print("1. Se déplacer/Voyager")
        print("2. Explorer la zone")
        print("3. Inventaire")
        print("4. Quêtes")
        print("5. Parler à un PNJ")
        print("6. Voir la carte")
        print("7. Statistiques du personnage")
        print("8. Sauvegarder la partie")
        print("9. Aide")
        print("0. Quitter le jeu")
        
        choice = input("\nEntrez votre choix (0-9): ").strip()
        
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
            print("❌ Il n'y a pas de sortie de cet endroit !")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        print(f"\n🧭 Directions disponibles:")
        for i, direction in enumerate(directions, 1):
            target_location = self.world.get_current_location().connections[direction]
            print(f"{i}. {direction.upper()} vers {target_location}")
        
        try:
            choice = int(input(f"\nChoisissez une direction (1-{len(directions)}): ")) - 1
            if 0 <= choice < len(directions):
                direction = directions[choice]
                success, message = self.world.move_to_location(direction)
                
                if success:
                    print(f"✅ {message}")
                    self.player.current_location = self.world.current_location_name
                    
                    # Affiche la description du nouveau lieu
                    new_location = self.world.get_current_location()
                    if not new_location.visited:
                        print(f"\n{new_location.get_description()}")
                        input("Appuyez sur Entrée pour continuer...")
                else:
                    print(f"❌ {message}")
                    input("Appuyez sur Entrée pour continuer...")
            else:
                print("❌ Direction invalide !")
                input("Appuyez sur Entrée pour continuer...")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide !")
            input("Appuyez sur Entrée pour continuer...")
    
    def handle_exploration_action(self):
        """Gère l'exploration active"""
        print(f"\n🔍 Exploration de {self.world.get_current_location().name}...")
        
        # Vérifie les rencontres d'ennemis
        enemy_type = self.world.get_current_location().check_for_enemy_encounter()
        if enemy_type:
            self.start_combat(enemy_type)
        else:
            # Chance de trouver des objets
            if random.random() < 0.3:  # 30% de chance
                item = generate_loot("common")
                if item:
                    print(f"💰 Vous avez trouvé: {item.name}")
                    if self.player.inventory.add_item(item):
                        print("📦 Objet ajouté à l'inventaire !")
                    else:
                        print("❌ Inventaire plein ! Impossible de ramasser l'objet.")
            else:
                print("🔍 Vous explorez la zone mais ne trouvez rien d'intéressant.")
            
            input("Appuyez sur Entrée pour continuer...")
    
    def handle_inventory(self):
        """Gère la gestion de l'inventaire"""
        self.clear_screen()
        print(self.player.inventory.get_inventory_display())
        
        if self.player.inventory.items:
            print(f"\nOptions:")
            print("1. Utiliser un objet")
            print("2. Équiper une arme/armure")
            print("3. Retour au jeu")
            
            choice = input("\nChoisissez une option (1-3): ").strip()
            
            if choice == "1":
                self.use_inventory_item()
            elif choice == "2":
                self.equip_item()
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def use_inventory_item(self):
        """Gère l'utilisation d'objets de l'inventaire"""
        consumables = self.player.inventory.get_items_by_type("consumable")
        
        if not consumables:
            print("❌ Aucun objet consommable disponible !")
            return
        
        print("\n🧪 Objets consommables:")
        for i, item in enumerate(consumables, 1):
            quantity = f" x{item.quantity}" if item.stackable and item.quantity > 1 else ""
            print(f"{i}. {item.name}{quantity} - {item.get_info()}")
        
        try:
            choice = int(input("\nChoisissez un objet à utiliser (0 pour annuler): ")) - 1
            if 0 <= choice < len(consumables):
                item = consumables[choice]
                # Trouve l'objet dans l'inventaire et l'utilise
                for i, inv_item in enumerate(self.player.inventory.items):
                    if inv_item.name == item.name:
                        if self.player.use_item(i):
                            print(f"✅ {item.name} utilisé !")
                        break
            elif choice == -1:
                return
            else:
                print("❌ Objet invalide !")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide !")
    
    def equip_item(self):
        """Gère l'équipement d'objets"""
        equipment = self.player.inventory.get_items_by_type("weapon") + \
                   self.player.inventory.get_items_by_type("armor")
        
        if not equipment:
            print("❌ Aucun équipement disponible !")
            return
        
        print("\n⚔️  Équipement:")
        for i, item in enumerate(equipment, 1):
            print(f"{i}. {item.name} - {item.get_info()}")
        
        try:
            choice = int(input("\nChoisissez un objet à équiper (0 pour annuler): ")) - 1
            if 0 <= choice < len(equipment):
                item = equipment[choice]
                if item.item_type == "weapon":
                    self.player.equip_weapon(item)
                elif item.item_type == "armor":
                    self.player.equip_armor(item)
            elif choice == -1:
                return
            else:
                print("❌ Objet invalide !")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide !")
    
    def handle_quests(self):
        """Gère l'interface des quêtes"""
        self.clear_screen()
        print(self.story_manager.get_quests_display(self.player))
        input("\nAppuyez sur Entrée pour continuer...")
    
    def handle_talk(self):
        """Gère les discussions avec les PNJ"""
        npcs = self.story_manager.get_npc_at_location(self.world.current_location_name)
        
        if not npcs:
            print("❌ Il n'y a personne à qui parler ici !")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        print(f"\n👥 Avec qui voulez-vous parler ?")
        for i, npc in enumerate(npcs, 1):
            print(f"{i}. {npc.name}")
        
        try:
            choice = int(input("\nChoisissez une personne (0 pour annuler): ")) - 1
            if 0 <= choice < len(npcs):
                npc = npcs[choice]
                self.conversation_with_npc(npc)
            elif choice == -1:
                return
            else:
                print("❌ Personne invalide !")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide !")
        
        input("Appuyez sur Entrée pour continuer...")
    
    def conversation_with_npc(self, npc):
        """Gère la conversation avec un PNJ"""
        print(f"\n💬 {npc.name}:")
        print(f"   {npc.description}")
        
        # Obtient le dialogue approprié
        if npc.has_available_quests(self.player):
            dialogue = npc.get_dialogue("greeting")
            print(f"\n{npc.name}: {dialogue}")
            
            # Offre une quête
            quest = npc.get_next_quest()
            if quest:
                print(f"\n📜 Offre de quête: {quest.name}")
                print(f"   {quest.description}")
                print(f"   Progression:\n{quest.get_progress_text()}")
                
                accept = input("\nAccepter cette quête ? (o/n): ").strip().lower()
                if accept in ['o', 'oui']:
                    print(f"\n{npc.name}: {npc.get_dialogue('quest_accepted')}")
                    # Note: Dans un système plus complexe, on suivrait l'acceptation de quête
                else:
                    print(f"\n{npc.name}: Peut-être une autre fois alors...")
        else:
            dialogue = npc.get_dialogue("no_quests")
            print(f"\n{npc.name}: {dialogue}")
    
    def handle_map(self):
        """Gère l'affichage de la carte du monde"""
        self.clear_screen()
        print(self.world.get_world_map())
        input("\nAppuyez sur Entrée pour continuer...")
    
    def handle_stats(self):
        """Gère l'affichage des statistiques du personnage"""
        self.clear_screen()
        print(self.player.get_detailed_stats())
        input("\nAppuyez sur Entrée pour continuer...")
    
    def handle_save(self):
        """Gère la sauvegarde du jeu"""
        if self.save_manager.save_game(self.player, self.world, self.story_manager):
            print("✅ Jeu sauvegardé avec succès !")
        else:
            print("❌ Échec de la sauvegarde du jeu !")
        input("Appuyez sur Entrée pour continuer...")
    
    def handle_quit(self):
        """Gère le fait de quitter le jeu"""
        print("\nÊtes-vous sûr de vouloir quitter ?")
        print("1. Sauvegarder et quitter")
        print("2. Quitter sans sauvegarder")
        print("3. Annuler")
        
        choice = input("\nChoisissez une option (1-3): ").strip()
        
        if choice == "1":
            self.handle_save()
            self.running = False
        elif choice == "2":
            self.running = False
        elif choice == "3":
            return
        else:
            print("❌ Choix invalide !")
    
    def handle_help(self):
        """Affiche les informations d'aide"""
        help_text = """
🎮 BHILQUEST - GUIDE D'AIDE
========================

DÉPLACEMENT:
• Utilisez l'option Se déplacer pour voyager entre les lieux
• Choisissez parmi les directions disponibles (N, S, E, W, etc.)

COMBAT:
• Le combat est au tour par tour et se produit automatiquement lors de l'exploration
• Choisissez des actions: Attaquer, Défendre, Utiliser un objet, ou Fuir
• Différents ennemis ont différents niveaux de difficulté

INVENTAIRE:
• Gérez vos objets via le menu Inventaire
• Utilisez des potions de soin
• Équipez des armes et armures pour améliorer vos statistiques

QUÊTES:
• Parlez aux PNJ pour recevoir des quêtes
• Complétez les quêtes en remplissant les exigences
• Gagnez de l'expérience et des récompenses pour les quêtes terminées

EXPLORATION:
• Explorez les zones pour trouver des objets et rencontrer des ennemis
• Différents lieux ont différents dangers et récompenses
• Visitez tous les lieux pour découvrir le monde

CONSEILS:
• Sauvegardez votre progression régulièrement
• Faites le plein de potions de soin avant les zones dangereuses
• Complétez les quêtes pour gagner de l'expérience et des récompenses
• Explorez minutieusement pour trouver des objets de valeur

Bonne chance, héros !
        """
        print(help_text)
        input("\nAppuyez sur Entrée pour continuer...")
    
    def game_over(self):
        """Gère la fin du jeu"""
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
        
        print(f"\n💀 {self.player.name} a été vaincu au combat...")
        print(f"📊 Statistiques finales:")
        print(f"   Niveau: {self.player.level}")
        print(f"   Quêtes terminées: {len(self.player.quests_completed)}")
        print(f"   Lieux visités: {sum(1 for loc in self.world.locations.values() if loc.visited)}")
        
        input("\nAppuyez sur Entrée pour retourner au menu principal...")
        self.running = False
    
    def run(self):
        """Exécute le jeu"""
        while True:
            menu_choice = self.main_menu()
            
            if menu_choice == "quit":
                print("\n👋 Merci d'avoir joué à BhilQuest !")
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
        jeu = Jeu()
        jeu.run()
    except KeyboardInterrupt:
        print("\n\n👋 Merci d'avoir joué à BhilQuest !")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Une erreur est survenue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
