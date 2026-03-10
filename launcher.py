"""
BhilQuest - Lanceur
Démarre le jeu BhilQuest

Créé par: Bhilal CHITOU (Bhil€)
Email: 7bhilal.chitou7@gmail.com
GitHub: https://github.com/7Bhil
"""

import os
import sys
import time

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
    print(colors['yellow'] + "                    Une Aventure RPG en Console" + colors['reset'])
    print("\n" + "="*60 + "\n")

def main():
    """Point d'entrée principal"""
    try:
        clear_screen()
        print_title()
        print("🇫🇷 Lancement de BhilQuest...")
        print("🎮 Démarrage du jeu...")
        time.sleep(1)
        
        # Importe et lance le jeu (main.py est maintenant en français)
        import main
        main.main()
                
    except KeyboardInterrupt:
        print("\n\n👋 Merci d'avoir joué à BhilQuest !")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
