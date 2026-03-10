#!/usr/bin/env python3
"""
BhilQuest - Script de Nettoyage des Sauvegardes
Supprime toutes les sauvegardes existantes pour réinitialiser le jeu

Créé par: Bhilal CHITOU (Bhil€)
Email: 7bhilal.chitou7@gmail.com
GitHub: https://github.com/7Bhil
"""

import os
import shutil
import glob
from datetime import datetime

class SaveCleaner:
    """Gère le nettoyage des sauvegardes BhilQuest"""
    
    def __init__(self):
        self.save_directory = "saves"
        self.backup_directory = "saves_backup"
        self.cleaned_files = []
        self.backup_files = []
        
    def list_save_files(self) -> list:
        """Liste tous les fichiers de sauvegarde"""
        save_files = []
        
        # Fichiers de sauvegarde principaux
        patterns = [
            f"{self.save_directory}/*.json",
            f"{self.save_directory}/*.save",
            f"{self.save_directory}/*.sav",
            "*.json",  # Dans le répertoire racine
            "*.save",  # Dans le répertoire racine
            "*.sav"    # Dans le répertoire racine
        ]
        
        for pattern in patterns:
            files = glob.glob(pattern)
            save_files.extend(files)
        
        return list(set(save_files))  # Évite les doublons
    
    def create_backup(self, files_to_backup: list) -> bool:
        """Crée une sauvegarde des fichiers avant suppression"""
        try:
            # Crée le répertoire de backup
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_folder = f"{self.backup_directory}/backup_{timestamp}"
            os.makedirs(backup_folder)
            
            for file_path in files_to_backup:
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    backup_path = os.path.join(backup_folder, filename)
                    shutil.copy2(file_path, backup_path)
                    self.backup_files.append((file_path, backup_path))
                    print(f"✅ Backup créé: {file_path} → {backup_path}")
            
            print(f"\n📦 Backup complet dans: {backup_folder}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du backup: {e}")
            return False
    
    def delete_save_files(self, files_to_delete: list) -> bool:
        """Supprime les fichiers de sauvegarde"""
        try:
            for file_path in files_to_delete:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.cleaned_files.append(file_path)
                    print(f"🗑️  Supprimé: {file_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            return False
    
    def clean_save_directory(self) -> bool:
        """Nettoie le répertoire de sauvegardes"""
        try:
            if os.path.exists(self.save_directory):
                # Supprime tous les fichiers dans le répertoire
                for filename in os.listdir(self.save_directory):
                    file_path = os.path.join(self.save_directory, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        self.cleaned_files.append(file_path)
                        print(f"🗑️  Supprimé: {file_path}")
                
                print(f"✅ Répertoire {self.save_directory} nettoyé")
                return True
            else:
                print(f"ℹ️  Le répertoire {self.save_directory} n'existe pas")
                return True
                
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage du répertoire: {e}")
            return False
    
    def show_summary(self):
        """Affiche un résumé des opérations"""
        print("\n" + "="*60)
        print("🧹 RÉSUMÉ DU NETTOYAGE")
        print("="*60)
        
        if self.backup_files:
            print(f"\n📦 FICHIERS BACKUPÉS ({len(self.backup_files)}):")
            for original, backup in self.backup_files:
                print(f"   {original} → {backup}")
        
        if self.cleaned_files:
            print(f"\n🗑️  FICHIERS SUPPRIMÉS ({len(self.cleaned_files)}):")
            for file_path in self.cleaned_files:
                print(f"   {file_path}")
        
        if not self.backup_files and not self.cleaned_files:
            print("\n✅ Aucun fichier de sauvegarde trouvé - Le jeu est déjà propre!")
        
        print(f"\n💡 CONSEIL: Lance maintenant './bhilquest' pour une nouvelle partie!")
    
    def interactive_cleanup(self):
        """Nettoyage interactif avec confirmation"""
        print("🔍 RECHERCHE DES FICHIERS DE SAUVEGARDE...")
        save_files = self.list_save_files()
        
        if not save_files:
            print("✅ Aucun fichier de sauvegarde trouvé!")
            return
        
        print(f"\n📋 FICHIERS TROUVÉS ({len(save_files)}):")
        for file_path in save_files:
            size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M") if os.path.exists(file_path) else "N/A"
            print(f"   📄 {file_path} ({size} bytes, {modified})")
        
        print(f"\n⚠️  CE NETTOYAGE SUPPRIMERA TOUTES LES SAUVEGARDES!")
        print("🎯 Cela réinitialisera complètement le jeu")
        
        # Options
        print(f"\n📋 OPTIONS:")
        print("1. Supprimer les sauvegardes (avec backup)")
        print("2. Supprimer les sauvegardes (sans backup)")
        print("3. Annuler")
        
        choice = input(f"\nChoisissez une option (1-3): ").strip()
        
        if choice == "1":
            print("\n📦 Création du backup...")
            if self.create_backup(save_files):
                print("\n🗑️  Suppression des fichiers...")
                if self.delete_save_files(save_files):
                    self.clean_save_directory()
                    self.show_summary()
                else:
                    print("❌ Erreur lors de la suppression")
            else:
                print("❌ Erreur lors du backup")
        
        elif choice == "2":
            print("\n🗑️  Suppression des fichiers (sans backup)...")
            if self.delete_save_files(save_files):
                self.clean_save_directory()
                self.show_summary()
            else:
                print("❌ Erreur lors de la suppression")
        
        elif choice == "3":
            print("\n❌ Opération annulée")
        
        else:
            print("\n❌ Choix invalide!")

def main():
    """Fonction principale"""
    print("🧹 BHILQUEST - NETTOYAGE DES SAUVEGARDES")
    print("="*50)
    
    cleaner = SaveCleaner()
    cleaner.interactive_cleanup()

if __name__ == "__main__":
    main()
