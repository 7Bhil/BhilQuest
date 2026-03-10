"""
BhilQuest - Lanceur Multilingue
Permet de choisir la langue du jeu

Créé par: Bhilal CHITOU (Bhil€)
Email: 7bhilal.chitou7@gmail.com
GitHub: https://github.com/7Bhil
"""

import os
import sys
import time
from typing import Optional

# Import des jeux selon la langue
def clear_screen():
    """Efface l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    """Affiche l'écran-titre du lanceur"""
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
    
    colors = {
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'reset': '\033[0m'
    }
    
    print(colors['cyan'] + title + colors['reset'])
    print(colors['yellow'] + "                    A Terminal RPG Adventure" + colors['reset'])
    print("\n" + "="*60 + "\n")

def language_menu() -> str:
    """Affiche le menu de sélection de langue"""
    while True:
        clear_screen()
        print_title()
        
        print("🌍 LANGUAGE / LANGUE SELECTION")
        print("="*40)
        print("1. 🇬🇧 English")
        print("2. 🇫🇷 Français")
        print("3. ❌ Quitter / Exit")
        print("="*40)
        
        choice = input("\nChoose your language / Choisissez votre langue (1-3): ").strip()
        
        if choice == "1":
            return "english"
        elif choice == "2":
            return "french"
        elif choice == "3":
            return "quit"
        else:
            print("❌ Invalid choice! / Choix invalide !")
            input("Press Enter to continue / Appuyez sur Entrée pour continuer...")

def launch_game(language: str):
    """Lance le jeu dans la langue choisie"""
    clear_screen()
    
    if language == "english":
        print("🇬🇧 Launching BhilQuest in English...")
        print("🎮 Starting game...")
        time.sleep(1)
        
        try:
            # Importe et lance la version anglaise
            import main
            main.main()
        except ImportError as e:
            print(f"❌ Error loading English version: {e}")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")
    
    elif language == "french":
        print("🇫🇷 Lancement de BhilQuest en Français...")
        print("🎮 Démarrage du jeu...")
        time.sleep(1)
        
        try:
            # Importe et lance la version française
            import main_fr
            main_fr.main()
        except ImportError as e:
            print(f"❌ Erreur lors du chargement de la version française: {e}")
            input("Appuyez sur Entrée pour continuer...")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            input("Appuyez sur Entrée pour continuer...")

def main():
    """Point d'entrée principal du lanceur"""
    try:
        while True:
            language = language_menu()
            
            if language == "quit":
                print("\n👋 Thanks for playing BhilQuest! / Merci d'avoir joué à BhilQuest !")
                break
            else:
                launch_game(language)
                
                # Après avoir quitté le jeu, demande si l'utilisateur veut continuer
                clear_screen()
                print_title()
                print("🔄 Back to language selection...")
                print("🔄 Retour à la sélection de langue...")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing BhilQuest! / Merci d'avoir joué à BhilQuest !")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred / Une erreur est survenue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
