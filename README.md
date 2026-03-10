# BhilQuest - Aventure RPG en Terminal 🎮✨

Un jeu de rôle (RPG) complet en mode texte développé en Python. Explorez un monde mystérieux, combattez des monstres et accomplissez des quêtes épiques directement dans votre terminal !

## 🚀 Comment Lancer le Jeu (Tous OS)

### 📋 Prérequis
- **Python 3.8** ou supérieur installé sur votre système.

### 🐧 Sur Linux & macOS
1. Ouvrez un terminal dans le dossier du projet.
2. Donnez les permissions d'exécution au script :
   ```bash
   chmod +x bhilquest
   ```
3. Lancez le jeu :
   ```bash
   ./bhilquest
   ```
   *Alternativement, vous pouvez lancer directement : `python3 launcher.py`*

### 🪟 Sur Windows
- Double-cliquez simplement sur le fichier **`bhilquest.bat`**.
- Ou ouvrez un terminal (PowerShell ou CMD) et tapez :
  ```powershell
  python launcher.py
  ```

---

## 🎮 Fonctionnalités

- **⚔️ Combat au Tour par Tour** : Système stratégique avec attaques et défense.
- **📈 Progression** : Gagnez de l'expérience, montez en niveau et boostez vos statistiques.
- **🎒 Inventaire Royal** : Équipez des armes/armures et utilisez des potions de soin.
- **🗺️ Exploration Libre** : Voyagez entre le Village, la Forêt, les Ruines et le Donjon.
- **📜 Quêtes et PNJ** : Interagissez avec les habitants pour obtenir des missions.
- **💾 Sauvegarde Automatique** : Votre progression est conservée dans `saves/`.

## 📁 Structure du Projet

- `launcher.py` : Le point d'entrée recommandé pour tous les utilisateurs.
- `main.py` : La boucle principale de jeu et l'interface.
- `character.py` : Logique des joueurs et des ennemis.
- `inventory.py` : Gestion des objets et de l'équipement.
- `world.py` : Gestion de la carte et des lieux.
- `save.py` : Système de sauvegarde JSON.
- `combat.py` / `story.py` : Moteurs de combat et d'histoire.

## 🎯 Commandes en Jeu
Une fois le jeu lancé, utilisez les touches **0 à 9** pour naviguer dans les menus :
- `1` pour se déplacer, `2` pour explorer.
- `3` pour voir votre sac à dos.
- `8` pour sauvegarder manuellement.
- `0` pour quitter proprement.

---
**Créé par Bhilal CHITOU (Bhil€)**
*Bonne chance dans votre quête, héros !*
