================================================================================
  GUIDE D'UTILISATION - SYSTÈME D'AUTHENTIFICATION D'ORDONNANCES MÉDICALES
  Signature Post-Quantique Mirath
================================================================================

📋 TABLE DES MATIÈRES
================================================================================

1. INTRODUCTION - Qu'est-ce que ce système?
2. ARCHITECTURE - Comment les fichiers sont organisés
3. PRÉREQUIS - Ce dont vous avez besoin avant de commencer
4. INSTALLATION - Comment préparer le système
5. UTILISATION - Comment lancer et utiliser le programme
6. DÉBOGAGE - Comment résoudre les problèmes
7. FONCTIONNEMENT DÉTAILLÉ - Comment ça marche en interne

================================================================================
1. INTRODUCTION
================================================================================

Objectif du système:
-----------------------
Ce système permet de signer numériquement des ordonnances médicales avec une
technologie résistante aux ordinateurs quantiques (cryptographie post-quantique).

👥 Acteurs principaux:
----------------------
- MÉDECINS: Créent et signent des ordonnances avec leur clé privée
- PHARMACIENS: Vérifient l'authenticité des ordonnances avec la clé publique

🔐 Sécurité:
-----------
Le système utilise le schéma de signature Mirath, basé sur le problème
mathématique MinRank qui reste difficile même pour les ordinateurs quantiques.

================================================================================
2. ARCHITECTURE - ORGANISATION DES FICHIERS
================================================================================

Ce projet doit être organisé comme ceci:

projet_ordonnances/              ← Dossier principal 
│
├── mirath.py                    ← Module cryptographique (signature Mirath)
├── ordonnance.py                ← Gestion des ordonnances médicales
├── medecin.py                   ← Actions des médecins (signer)
├── pharmacie.py                 ← Actions des pharmaciens (vérifier)
├── main.py                      ← Programme principal (à exécuter)
│
├── cles_medecins/               ← Dossier créé automatiquement
│   ├── MED001_public.json       ← Clés publiques des médecins
│   └── MED001_secret.json       ← Clés secrètes (CONFIDENTIELLES!)
│
└── ordonnances/                 ← Dossier pour vos ordonnances (optionnel)
    ├── ord_patient1.json
    └── ord_patient2.json

📝 Détail de chaque fichier:
-----------------------------

┌─────────────────────────────────────────────────────────────────────────┐
│ mirath.py - LE CŒUR CRYPTOGRAPHIQUE                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ Rôle: Implémente le schéma de signature Mirath                          │
│                                                                         │
│ Contient:                                                               │
│   • MirathParams: Paramètres du système                                 │
│   • FiniteField: Opérations mathématiques sur F₂                        │
│   • CryptoUtils: Fonctions de hash et générateurs                       │
│   • MinRankProblem: Le problème mathématique de base                    │
│   • MirathSignature: Classe principale pour signer/vérifier             │
│                                                                         │
│ Vous n'avez PAS besoin de modifier ce fichier sauf pour déboguer        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ ordonnance.py - STRUCTURE DES DONNÉES                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ Rôle: Définit ce qu'est une ordonnance et comment la manipuler          │
│                                                                         │
│ Contient:                                                               │
│   • Classe Ordonnance: Représente une ordonnance complète               │
│   • creer_medicament(): Crée un médicament                              │
│   • creer_ordonnance_interactive(): Guide pour créer une ordonnance     │
│                                                                         │
│ Vous pouvez modifier ce fichier si vous voulez ajouter des champs       │
│ à l'ordonnance (ex: durée du traitement, contre-indications, etc.)      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ medecin.py - ACTIONS DES MÉDECINS                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ Rôle: Permet aux médecins de signer des ordonnances                     │
│                                                                         │
│ Contient:                                                               │
│   • Classe Medecin: Représente un médecin avec ses clés                 │
│   • initialiser_medecin(): Crée un nouveau médecin                      │
│   • workflow_signature_ordonnance(): Guide complet de signature         │
│                                                                         │
│ C'est ici que vous ajouteriez des fonctionnalités pour les médecins     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ pharmacie.py - ACTIONS DES PHARMACIENS                                  │
├─────────────────────────────────────────────────────────────────────────┤
│ Rôle: Permet aux pharmaciens de vérifier les ordonnances                │
│                                                                         │
│ Contient:                                                               │
│   • Classe Pharmacie: Représente une pharmacie                          │
│   • workflow_verification_ordonnance(): Guide de vérification           │
│   • verifier_ordonnance_simple(): Vérification rapide                   │
│                                                                         │
│ C'est ici que vous ajouteriez des fonctionnalités pour les pharmacies   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ main.py - PROGRAMME PRINCIPAL                                           │
├─────────────────────────────────────────────────────────────────────────┤
│ Rôle: Point d'entrée du système, gère les menus interactifs             │
│                                                                         │
│ Contient:                                                               │
│   • menu_principal(): Menu de choix du rôle                             │
│   • menu_medecin(): Menu pour les médecins                              │
│   • menu_pharmacien(): Menu pour les pharmaciens                        │
│   • demonstration_complete(): Démo de bout en bout                      │
│                                                                         │
│ C'est LE FICHIER À EXÉCUTER pour utiliser le système!                   │
└─────────────────────────────────────────────────────────────────────────┘

================================================================================
3. PRÉREQUIS - CE DONT VOUS AVEZ BESOIN
================================================================================

✅ Python:
----------
Vous devez avoir Python 3.7 ou plus récent installé sur votre ordinateur.

Pour vérifier votre version de Python, ouvrez un terminal et tapez:
   python --version
   
ou (sur certains systèmes):
   python3 --version

Si vous n'avez pas Python, téléchargez-le depuis: https://www.python.org

✅ Bibliothèque NumPy:
----------------------
Le système utilise NumPy pour les opérations matricielles.

Pour installer NumPy, tapez dans le terminal:
   pip install numpy

ou (sur certains systèmes):
   pip3 install numpy

⚠️ Note importante:
Si vous avez des erreurs du type "pip n'est pas reconnu", c'est que pip n'est
pas dans votre PATH. Essayez plutôt:
   python -m pip install numpy

✅ Éditeur de texte ou IDE:
---------------------------
Pour lire et modifier le code, vous aurez besoin d'un éditeur. Suggestions:
- Visual Studio Code (gratuit, recommandé)
- PyCharm (gratuit en version Community)
- Sublime Text
- Notepad++ (Windows)
- Ou simplement le bloc-notes

✅ Terminal / Invite de commandes:
----------------------------------
Vous devez savoir ouvrir un terminal:
- Windows: Cherchez "cmd" ou "PowerShell" dans le menu Démarrer
- Mac: Ouvrez "Terminal" depuis Applications/Utilitaires
- Linux: Ctrl+Alt+T (généralement)

================================================================================
4. INSTALLATION - PRÉPARATION DU SYSTÈME
================================================================================

Étape 1: Créer le dossier du projet
------------------------------------
Créez un nouveau dossier où vous voulez, par exemple:
   C:\Users\VotreNom\projet_ordonnances    (Windows)
   /home/votrenom/projet_ordonnances       (Linux/Mac)

Étape 2: Placer les fichiers Python
------------------------------------
Copiez TOUS les fichiers .py dans ce dossier:
   ✓ mirath.py
   ✓ ordonnance.py
   ✓ medecin.py
   ✓ pharmacie.py
   ✓ main.py

⚠️ IMPORTANT: Tous les fichiers doivent être dans le MÊME dossier!

Étape 3: Vérifier l'installation de NumPy
------------------------------------------
Ouvrez un terminal et tapez:
   python -c "import numpy; print('NumPy OK')"

Si vous voyez "NumPy OK", c'est bon!
Sinon, installez NumPy comme expliqué dans la section 3.

Étape 4: Tester que Python trouve les fichiers
-----------------------------------------------
Dans le terminal, naviguez vers votre dossier projet:
   cd chemin/vers/projet_ordonnances

Puis testez:
   python -c "import mirath; print('Import OK')"

Si vous voyez "Import OK", tout est prêt!

================================================================================
5. UTILISATION - COMMENT LANCER LE PROGRAMME
================================================================================

🚀 Lancement du programme principal:
-------------------------------------

1. Ouvrez un terminal / invite de commandes

2. Naviguez vers le dossier du projet:
   cd chemin/vers/projet_ordonnances

3. Lancez le programme:
   python main.py

   ou sur certains systèmes:
   python3 main.py

4. Le menu principal s'affiche! Suivez les instructions à l'écran.

📋 Structure du menu:
---------------------

MENU PRINCIPAL
  ├── [1] Agir en tant que MÉDECIN
  │     ├── Workflow complet (création + signature)
  │     ├── Initialiser un nouveau médecin
  │     └── Signer une ordonnance existante
  │
  ├── [2] Agir en tant que PHARMACIEN
  │     ├── Workflow complet (vérification)
  │     └── Vérification rapide
  │
  ├── [3] GESTION DU SYSTÈME
  │     ├── Initialiser un nouveau médecin
  │     ├── Lister les médecins
  │     └── Afficher une ordonnance
  │
  └── [4] DÉMONSTRATION COMPLÈTE
        └── Exemple de bout en bout (RECOMMANDÉ POUR DÉBUTER!)

🎯 Scénario d'utilisation typique:
-----------------------------------

PREMIÈRE UTILISATION (pour comprendre le système):
---------------------------------------------------
1. Lancez: python main.py
2. Choisissez [4] - DÉMONSTRATION COMPLÈTE
3. Suivez le déroulement automatique
4. Observez comment le système fonctionne

UTILISATION NORMALE:
--------------------
1. Lancez: python main.py

2. Pour créer un médecin:
   → [1] Médecin → [2] Initialiser un nouveau médecin
   → Entrez: nom, prénom, ID (ex: MED001)
   → Le système génère et sauvegarde ses clés

3. Pour signer une ordonnance:
   → [1] Médecin → [1] Workflow complet
   → Entrez votre ID médecin
   → Créez ou chargez une ordonnance
   → Signez-la
   → Elle est sauvegardée avec la signature

4. Pour vérifier une ordonnance:
   → [2] Pharmacien → [1] Workflow complet
   → Entrez le nom de votre pharmacie
   → Chargez les clés publiques des médecins
   → Chargez l'ordonnance à vérifier
   → Le système vérifie automatiquement

================================================================================
6. DÉBOGAGE - RÉSOLUTION DES PROBLÈMES
================================================================================

❌ Erreur: "ModuleNotFoundError: No module named 'mirath'"
-----------------------------------------------------------
CAUSE: Python ne trouve pas les fichiers du projet
SOLUTION:
  1. Vérifiez que vous êtes dans le bon dossier:
     pwd (Linux/Mac) ou cd (Windows) pour voir où vous êtes
  2. Vérifiez que main.py et mirath.py sont dans le même dossier:
     ls (Linux/Mac) ou dir (Windows) pour lister les fichiers
  3. Naviguez vers le bon dossier:
     cd chemin/vers/projet_ordonnances

❌ Erreur: "ModuleNotFoundError: No module named 'numpy'"
---------------------------------------------------------
CAUSE: NumPy n'est pas installé
SOLUTION:
  pip install numpy
  ou
  python -m pip install numpy

❌ Erreur: "Signature valide: False" (alors qu'elle devrait être valide)
------------------------------------------------------------------------
CAUSE: Possible bug dans la logique de vérification
SOLUTION:
  1. Assurez-vous d'utiliser la VERSION CORRIGÉE de mirath.py
  2. Vérifiez que l'ordonnance n'a pas été modifiée après signature
  3. Testez avec la démonstration complète pour voir si ça fonctionne

❌ Erreur: "FileNotFoundError: [Errno 2] No such file or directory"
--------------------------------------------------------------------
CAUSE: Le fichier demandé n'existe pas ou le chemin est incorrect
SOLUTION:
  1. Vérifiez le nom du fichier (pas de fautes de frappe)
  2. Vérifiez que le fichier existe réellement
  3. Utilisez le chemin complet si nécessaire:
     C:\Users\...\ordonnance.json au lieu de juste ordonnance.json

❌ Le programme se ferme immédiatement
---------------------------------------
CAUSE: Erreur Python critique au lancement
SOLUTION:
  1. Lancez depuis un terminal (pas en double-cliquant sur le fichier)
  2. Lisez l'erreur affichée dans le terminal
  3. Copiez l'erreur et cherchez-la en ligne si besoin

❌ "TypeError" ou "AttributeError"
----------------------------------
CAUSE: Problème de type de données ou d'attribut manquant
SOLUTION:
  1. Vérifiez que vous utilisez bien Python 3.7+
  2. Vérifiez que tous les fichiers sont les bonnes versions
  3. Regardez le numéro de ligne dans l'erreur
  4. Ajoutez des print() pour déboguer:
     print("Valeur de la variable:", ma_variable)

🔍 Technique de débogage générale:
-----------------------------------
1. Lisez COMPLÈTEMENT le message d'erreur (il contient souvent la solution)
2. Notez le numéro de ligne où l'erreur se produit
3. Ouvrez le fichier concerné
4. Ajoutez des print() avant et après la ligne problématique
5. Relancez et observez ce qui s'affiche

Exemple:
   # Avant la ligne problématique
   print("DEBUG: Valeur de x =", x)
   print("DEBUG: Type de x =", type(x))
   
   # Ligne qui pose problème
   resultat = fonction(x)
   
   # Après
   print("DEBUG: Résultat =", resultat)

================================================================================
7. FONCTIONNEMENT DÉTAILLÉ - COMMENT ÇA MARCHE
================================================================================

🔐 Le système de signature Mirath:
-----------------------------------

1. GÉNÉRATION DE CLÉS (initialisation d'un médecin):
   
   Le médecin reçoit:
   - Clé SECRÈTE (privée): Utilisée pour SIGNER les ordonnances
   - Clé PUBLIQUE: Partagée avec les pharmacies pour VÉRIFIER
   
   Analogie: La clé secrète est comme votre signature manuscrite (personne
   ne doit pouvoir la reproduire), et la clé publique est comme un exemple
   de votre signature que tout le monde peut voir pour vérifier.

2. SIGNATURE D'UNE ORDONNANCE (par le médecin):
   
   Processus:
   a) L'ordonnance est convertie en un texte canonique
   b) Ce texte passe par des fonctions cryptographiques (hash)
   c) La clé secrète du médecin est utilisée pour créer la signature
   d) La signature est attachée à l'ordonnance
   
   Résultat: Une ordonnance avec une "empreinte digitale" unique que seul
   ce médecin peut créer.

3. VÉRIFICATION D'UNE ORDONNANCE (par la pharmacie):
   
   Processus:
   a) L'ordonnance est reconvertie en texte canonique
   b) La signature est analysée avec la clé PUBLIQUE du médecin
   c) Le système vérifie que la signature correspond
   
   Résultat: 
   - Si OUI → L'ordonnance est authentique et n'a pas été modifiée
   - Si NON → L'ordonnance est suspecte (fausse ou altérée)

📊 Flux de données complet:
----------------------------

MÉDECIN                          SYSTÈME                    PHARMACIE
  │                                 │                           │
  │ 1. Initialisation               │                           │
  │───────────────────────────────→ │                           │
  │  (génère clés publique/privée)  │                           │
  │←─────────────────────────────── │                           │
  │                                 │                           │
  │ 2. Crée une ordonnance          │                           │
  │───────────────────────────────→ │                           │
  │                                 │                           │
  │ 3. Signe avec clé privée        │                           │
  │───────────────────────────────→ │                           │
  │                                 │                           │
  │ 4. Ordonnance signée            │                           │
  │←─────────────────────────────── │                           │
  │                                 │                           │
  │ 5. Envoie au patient            │                           │
  │ (fichier JSON)                  │                           │
  │                                 │                           │
  │                                 │ 6. Patient apporte        │
  │                                 │    l'ordonnance           │
  │                                 │←──────────────────────────│
  │                                 │                           │
  │ 7. Partage clé publique         │                           │
  │    (une seule fois)             │                           │
  │─────────────────────────────────────────────────────────────→│
  │                                 │                           │
  │                                 │ 8. Vérifie avec clé       │
  │                                 │    publique               │
  │                                 │←──────────────────────────│
  │                                 │                           │
  │                                 │ 9. Résultat: VALIDE       │
  │                                 │    ou INVALIDE            │
  │                                 │───────────────────────────→│

🔒 Sécurité du système:
------------------------

PROTECTIONS INTÉGRÉES:
✓ Résistance quantique: Basé sur le problème MinRank (difficile même pour
  les ordinateurs quantiques futurs)

✓ Non-répudiation: Un médecin ne peut pas nier avoir signé une ordonnance
  (sa signature est unique)

✓ Intégrité: Toute modification de l'ordonnance invalide la signature

✓ Authenticité: Seul le médecin possédant la clé privée peut créer une
  signature valide

POINTS À SURVEILLER:
⚠️ La clé secrète doit rester CONFIDENTIELLE (comme un mot de passe)
⚠️ Les fichiers *_secret.json ne doivent JAMAIS être partagés
⚠️ En production réelle, les clés devraient être dans un HSM (module
   de sécurité matériel) ou au moins chiffrées

================================================================================
📞 SUPPORT ET AIDE
================================================================================

Si vous avez des problèmes:

1. Relisez la section 6 (DÉBOGAGE)
2. Vérifiez que vous avez suivi toutes les étapes d'installation
3. Testez la démonstration complète (option [4] du menu)
4. Utilisez des print() pour déboguer (voir section 6)
5. Regardez les commentaires dans le code (ils expliquent chaque ligne)

================================================================================
✅ CHECKLIST FINALE
================================================================================

Avant de commencer votre projet, vérifiez:

□ Python 3.7+ installé et fonctionnel
□ NumPy installé (pip install numpy)
□ Tous les fichiers .py dans le même dossier
□ Terminal/invite de commandes maîtrisé(e)
□ Capable de naviguer avec 'cd' vers le dossier du projet
□ Ce guide lu et compris
□ Démonstration complète testée (option [4])

Quand tout est coché, vous êtes prêt(e) à utiliser le système!

================================================================================
FIN DU GUIDE
================================================================================
