"""
Pack de Langue Française pour BhilQuest
Toutes les chaînes de texte en français
"""

# Titre du jeu et branding
GAME_TITLE = "BHILQUEST"
GAME_SUBTITLE = "Jeu RPG d'Aventure Terminal"
CREATED_BY = "créé par Bhilal. CHITOU (Bhil€)"
EMAIL_CONTACT = "Email: 7bhilal.chitou7@gmail.com"
GITHUB_LINK = "GitHub: https://github.com/7Bhil"

# Menu Principal
MAIN_MENU_TITLE = "MENU PRINCIPAL"
NEW_GAME = "Nouvelle Partie"
CONTINUE_GAME = "Continuer Partie"
QUIT_GAME = "Quitter"
NO_SAVE_FOUND = "Aucune sauvegarde trouvée"
CHOOSE_OPTION = "Choisissez votre option (1-3):"
INVALID_CHOICE = "Choix invalide ! Veuillez entrer 1-3."

# Création de Personnage
CHARACTER_CREATION = "CRÉATION DE PERSONNAGE"
ENTER_NAME = "Entrez le nom de votre personnage:"
VALID_NAME = "Veuillez entrer un nom valide (1-20 caractères)"
WELCOME_MESSAGE = "Bienvenue, {name} ! Votre aventure commence maintenant..."
PRESS_ENTER = "Appuyez sur Entrée pour continuer..."
HERO_AWAKENS = "{name} le héros se réveille dans le village paisible !"

# Actions du jeu
WHAT_DO = "Que voulez-vous faire ?"
MOVE_TRAVEL = "Se déplacer/Voyager"
EXPLORE_AREA = "Explorer la zone"
INVENTORY = "Inventaire"
QUESTS = "Quêtes"
TALK_NPC = "Parler à un PNJ"
VIEW_MAP = "Voir la carte"
CHARACTER_STATS = "Statistiques du personnage"
SAVE_GAME = "Sauvegarder la partie"
HELP = "Aide"
QUIT = "Quitter le jeu"
ENTER_CHOICE = "Entrez votre choix (0-9):"

# Déplacement
AVAILABLE_DIRECTIONS = "Directions disponibles:"
CHOOSE_DIRECTION = "Choisissez une direction (1-{count}):"
TRAVEL_SUCCESS = "Vous voyagez {direction} vers {location}"
CANNOT_GO = "Vous ne pouvez pas aller {direction} d'ici"
NO_EXITS = "Il n'y a pas de sortie de cet endroit !"
INVALID_DIRECTION = "Direction invalide !"
ENTER_NUMBER = "Veuillez entrer un nombre valide !"

# Exploration
EXPLORING = "Exploration de {location}..."
FOUND_ITEM = "Vous avez trouvé: {item_name}"
ITEM_ADDED = "Objet ajouté à l'inventaire !"
INVENTORY_FULL = "Inventaire plein ! Impossible de ramasser l'objet."
NOTHING_FOUND = "Vous explorez la zone mais ne trouvez rien d'intéressant."

# Combat
ENEMY_APPEARS = "Un {enemy_name} sauvage apparaît !"
START_COMBAT = "Appuyez sur Entrée pour commencer le combat..."
COMBAT_BEGINS = "COMBAT COMMENCE !"
PLAYER_TURN = "Tour de {player_name}:"
ATTACK = "Attaquer"
DEFEND = "Défendre"
USE_ITEM = "Utiliser un objet"
FLEE = "Fuir"
CHOOSE_ACTION = "Choisissez votre action (1-4):"
INVALID_ACTION = "Choix invalide ! Veuillez entrer 1-4."
ATTACKS_FOR = "attaque {target} pour {damage} dégâts !"
TAKES_DAMAGE = "{target} subit {damage} dégâts !"
IS_DEFENDING = "{target} se défend ! Dégâts réduits !"
DEFENSIVE_STANCE = "prend une posture défensive !"
FAILED_TO_FLEE = "échoue à fuir !"
SUCCESSFULLY_FLED = "fuit avec succès du combat !"
TOO_MANY_ATTEMPTS = "Vous avez tenté de fuir trop de fois ! Vous devez combattre !"
USE_CONSUMABLE = "Utiliser des objets consommables"
NO_CONSUMABLES = "Aucun objet consommable disponible !"
CHOOSE_ITEM_USE = "Choisissez un objet à utiliser (0 pour annuler):"
CANNOT_USE_ITEM = "Impossible d'utiliser cet objet !"
INVALID_ITEM = "Objet invalide !"
VICTORY = "VICTOIRE !"
DEFEATED_ENEMY = "{player_name} a vaincu {enemy_name} !"
GAINED_EXP = "Gagné {exp} EXP !"
DROPPED = "{enemy_name} a laissé tomber:"
CANNOT_PICKUP = "Inventaire plein ! Impossible de ramasser {item_name}."
DEFEAT = "DÉFAITE !"
DEFEATED_BY = "{player_name} a été vaincu par {enemy_name} !"
LOST_BATTLE = "Vous avez perdu la bataille..."

# Inventaire
INVENTORY_DISPLAY = "INVENTAIRE"
INVENTORY_EMPTY = "Votre inventaire est vide"
SLOTS = "emplacements"
AVAILABLE_QUESTS = "QUÊTES DISPONIBLES"
ACTIVE_QUESTS = "QUÊTES ACTIVES"
USE_ITEM_OPTION = "Utiliser un objet"
EQUIP_OPTION = "Équiper une arme/armure"
BACK_GAME = "Retour au jeu"
CONSUMABLE_ITEMS = "Objets consommables"
CHOOSE_ITEM_EQUIP = "Choisissez un objet à équiper (0 pour annuler):"
EQUIPMENT = "Équipement"
NO_EQUIPMENT = "Aucun équipement disponible !"
USED_ITEM = "{item_name} utilisé !"

# Quêtes
QUEST_COMPLETED = "QUÊTE TERMINÉE"
QUEST_REWARDS = "Récompenses"
QUEST_OFFER = "Offre de quête"
QUEST_PROGRESS = "Progression"
ACCEPT_QUEST = "Accepter cette quête ? (o/n):"
QUEST_ACCEPTED = "Peut-être une autre fois alors..."
NO_AVAILABLE_QUESTS = "Aucune quête disponible !"

# PNJ
TALK_TO = "Avec qui voulez-vous parler ?"
CHOOSE_PERSON = "Choisissez une personne (0 pour annuler):"
INVALID_PERSON = "Personne invalide !"
NO_ONE_TALK = "Il n'y a personne à qui parler ici !"
CONVERSATION_WITH = "Conversation avec {npc_name}"
DESCRIPTION = "{npc_name}: {description}"
GREETING = "{npc_name}: {dialogue}"
PERHAPS_ANOTHER_TIME = "Peut-être une autre fois alors..."

# Carte et Statistiques
WORLD_MAP = "CARTE DU MONDE"
CURRENT_LOCATION = "Lieu Actuel"
PRESS_ENTER_CONTINUE = "Appuyez sur Entrée pour continuer..."

# Système de Sauvegarde
SAVE_SUCCESS = "Jeu sauvegardé avec succès !"
SAVE_FAILED = "Échec de la sauvegarde du jeu !"
LOAD_SUCCESS = "Jeu chargé avec succès ! (Sauvegardé: {timestamp})"
LOAD_FAILED = "Échec du chargement du jeu: {error}"
SAVE_FILE_INFO = "INFO FICHIER DE SAUVEGARDE"
PLAYER_NAME = "Joueur"
LEVEL = "Niveau"
LOCATION = "Lieu"
QUESTS_COMPLETED = "Quêtes Terminées"
SAVED = "Sauvegardé"
NO_SAVE_FILE = "Aucune sauvegarde trouvée !"

# Game Over
GAME_OVER_TITLE = "GAME OVER"
HAS_FALLEN = "{name} a été vaincu au combat..."
FINAL_STATS = "Statistiques finales"
QUESTS_COMPLETED_STAT = "Quêtes terminées"
LOCATIONS_VISITED = "Lieux visités"
RETURN_MENU = "Appuyez sur Entrée pour retourner au menu principal..."

# Système d'Aide
HELP_GUIDE = "GUIDE D'AIDE"
MOVEMENT_SECTION = "DÉPLACEMENT"
MOVEMENT_TEXT = "• Utilisez l'option Se déplacer pour voyager entre les lieux\n• Choisissez parmi les directions disponibles (N, S, E, W, etc.)"
COMBAT_SECTION = "COMBAT"
COMBAT_TEXT = "• Le combat est au tour par tour et se produit automatiquement lors de l'exploration\n• Choisissez des actions: Attaquer, Défendre, Utiliser un objet, ou Fuir\n• Différents ennemis ont différents niveaux de difficulté"
INVENTORY_SECTION = "INVENTAIRE"
INVENTORY_TEXT = "• Gérez vos objets via le menu Inventaire\n• Utilisez des potions de soin\n• Équipez des armes et armures pour améliorer vos statistiques"
QUESTS_SECTION = "QUÊTES"
QUESTS_TEXT = "• Parlez aux PNJ pour recevoir des quêtes\n• Complétez les quêtes en remplissant les exigences\n• Gagnez de l'expérience et des récompenses pour les quêtes terminées"
EXPLORATION_SECTION = "EXPLORATION"
EXPLORATION_TEXT = "• Explorez les zones pour trouver des objets et rencontrer des ennemis\n• Différents lieux ont différents dangers et récompenses\n• Visitez tous les lieux pour découvrir le monde"
TIPS_SECTION = "CONSEILS"
TIPS_TEXT = "• Sauvegardez votre progression régulièrement\n• Faites le plein de potions de soin avant les zones dangereuses\n• Complétez les quêtes pour gagner de l'expérience et des récompenses\n• Explorez minutieusement pour trouver des objets de valeur"
GOOD_LUCK = "Bonne chance, héros !"

# Quitter le jeu
SURE_QUIT = "Êtes-vous sûr de vouloir quitter ?"
SAVE_AND_QUIT = "Sauvegarder et quitter"
QUIT_WITHOUT_SAVING = "Quitter sans sauvegarder"
CANCEL = "Annuler"
CHOOSE_OPTION_QUIT = "Choisissez une option (1-3):"

# Messages
THANKS_PLAYING = "Merci d'avoir joué à BhilQuest !"
ERROR_OCCURRED = "Une erreur est survenue: {error}"

# Noms des lieux
VILLAGE = "Village Paisible"
MYSTIC_FOREST = "Forêt Mystique"
DEEP_FOREST = "Forêt Profonde"
ANCIENT_RUINS = "Ruines Anciennes"
ABANDONED_TEMPLE = "Temple Abandonné"
DUNGEON_ENTRANCE = "Entrée du Donjon"
DUNGEON_HALLS = "Salles du Donjon"
DUNGEON_DEPTHS = "Profondeurs du Donjon"
MOUNTAIN_PASS = "Passage Montagneux"

# Descriptions des lieux
VILLAGE_DESC = "Un petit village paisible entouré de palissades en bois. Vous pouvez voir quelques maisons, une forge et un puits au centre. Les villageois vaquent à leurs occupations quotidiennes, et l'atmosphère est calme et accueillante."
FOREST_DESC = "Une forêt dense et ancienne avec de grands arbres qui bloquent la plupart de la lumière du soleil. L'air est épais de l'odeur de mousse et de terre humide. Vous pouvez entendre des oiseaux chanter et occasionnellement du bruit dans les buissons. Les chemins serpentent entre les arbres, mais il est facile de se perdre si on ne fait pas attention."
DEEP_FOREST_DESC = "La partie plus profonde de la forêt où les arbres sont plus anciens et les ombres plus longues. Des champignons lumineux poussent sur les troncs tombés, et vous ressentez une présence surnaturelle. Cette zone est connue pour être dangereuse, avec beaucoup de créatures qui se cachent dans l'obscurité."
RUINS_DESC = "Les restes effondrés d'une civilisation antique. Des colonnes brisées et des structures en pierre usée parsèment le paysage. Des symboles étranges sont gravés dans les pierres, et vous pouvez sentir le poids de l'histoire en ce lieu. Les chasseurs de trésors explorent souvent ici, mais de nombreux dangers se cachent dans les ombres."
TEMPLE_DESC = "Un temple sacré maintenant tombé en désuétude. Les murs en pierre sont couverts de vignes, et l'autel est fissuré et taché. Des échos étranges semblent rebondir sur les murs, et vous ressentez une présence inquiétante. Des artéfacts anciens pourraient encore être cachés à l'intérieur."
DUNGEON_ENTRANCE_DESC = "Une entrée sombre et menaçante vers ce qui semble être un donjon souterrain. L'arche en pierre est couverte de symboles d'avertissement, et un air frais s'échappe d'en dessous. Vous pouvez entendre de l'eau qui goutte et des sons lointains et non identifiés. Seuls les braves oseraient entrer."
DUNGEON_HALLS_DESC = "Salles souterraines avec des murs en pierre et des corridors éclairés par des torches. L'air est humide et froid, et vos pas résonnent dans le silence. Des cellules de prison tapissent certains murs, et vous pouvez voir des preuves de batailles passées. Cet endroit est clairement dangereux."
DUNGEON_DEPTHS_DESC = "La partie la plus profonde du donjon où les créatures les plus dangereuses habitent. Les murs sont couverts de taches sombres, et vous pouvez entendre des grognements en avant. Une chambre massive s'ouvre, et au centre, vous pouvez voir le silhouette de quelque chose de grand et puissant."
MOUNTAIN_PASS_DESC = "Un chemin de montagne étroit avec des falaises abruptes des deux côtés. Le vent hurle à travers le passage, et vous pouvez voir de la neige sur les pics au-dessus. Ce chemin mène à d'autres régions, mais il est périlleux et seuls les voyageurs expérimentés devraient tenter."

# Directions
NORTH = "NORD"
SOUTH = "SUD"
EAST = "EST"
WEST = "OUEST"
UP = "HAUT"
DOWN = "BAS"

# Navigation
EXITS = "Sorties"
TO = "vers"
PEOPLE_HERE = "Personnes ici"
ITEMS_VISIBLE = "Objets visibles"

# Niveaux de danger
DANGER_LEVEL = "Niveau de Danger"
SAFE = "Sûr"
MODERATE = "Modéré"
DANGEROUS = "Dangereux"

# Messages de l'histoire
NEW_ADVENTURER = "Vous êtes un nouvel aventurier, prêt à prouver votre valeur."
TASTED_COMBAT = "Vous avez goûté au combat et survécu. Le chemin d'un héros s'ouvre devant vous."
CAPABLE_WARRIOR = "Vous vous êtes prouvé en tant que guerrier capable. De plus grands défis vous attendent."
TRUE_HERO = "Vous êtes un vrai héros du royaume ! Le dragon est vaincu et la paix restaurée."
LEGEND_GROWS = "Votre légende continue de grandir..."

# Noms des PNJ
ELDER_MARCUS = "Ancien Marcus"
BLACKSMITH_THORIN = "Forgeron Thorin"
MYSTERIOUS_STRANGER = "Étranger Mystérieux"

# Descriptions des PNJ
ELDER_DESC = "Un vieil homme sage avec une longue barbe blanche et des yeux gentils. Il a vécu dans le village toute sa vie et connaît de nombreux secrets."
BLACKSMITH_DESC = "Un nain musclé avec une barbe épaisse et des mains couvertes de suie. Il travaille toujours à sa forge."
STRANGER_DESC = "Une silhouette encapuchonnée avec une aura de mystère. Son visage est caché dans l'ombre."

# Noms des quêtes
GOBLIN_TROUBLE = "Problèmes de Gobelins"
RUINS_EXPLORATION = "Exploration des Ruines"
DUNGEON_MATERIALS = "Matériaux du Donjon"
DRAGON_SLAYER = "Tueur de Dragon"

# Descriptions des quêtes
GOBLIN_TROUBLE_DESC = "Le village est attaqué par des gobelins. Aidez-nous en vainquant 5 gobelins pour rendre notre village sûr à nouveau."
RUINS_EXPLORATION_DESC = "Explorez les ruines anciennes et trouvez l'artefact mystérieux que l'étranger cherche."
DUNGEON_MATERIALS_DESC = "Aventurez-vous dans les profondeurs du donjon et collectez des matériaux rares pour le forgeron."
DRAGON_SLAYER_DESC = "Le dragon ancien dans les profondeurs du donjon menace tout le royaume. Vous devez le vaincre !"

# Progression des quêtes
DEFEAT_GOBLINS = "Vaincre les gobelins: {current}/{required}"
OBTAIN_ARTIFACT = "Obtenir ancient_artifact: {status}"
COLLECT_MATERIALS = "Vaincre les squelettes: {current}/{required}"
DEFEAT_DRAGON = "Vaincre le dragon: {current}/{required}"

# Indicateurs de statut
STATUS_INDICATORS = "Indicateurs de statut"
CHECK = "✓"
CROSS = "✗"
