import sys
import os

try:
    from mirath import MirathSignature
    from ordonnance import Ordonnance, creer_ordonnance_interactive, creer_medicament
    from medecin import Medecin, initialiser_medecin, workflow_signature_ordonnance
    from pharmacie import Pharmacie, workflow_verification_ordonnance
except ImportError as e:
    print("❌ ERREUR D'IMPORTATION")
    print(f"   {e}")
    print("\n⚠️  Assurez-vous que tous les fichiers suivants sont dans le même dossier:")
    print("   - mirath.py")
    print("   - ordonnance.py")
    print("   - medecin.py")
    print("   - pharmacie.py")
    print("   - main.py (ce fichier)")
    sys.exit(1)


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def afficher_banniere():
    print("\n" + "=" * 70)
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║     SYSTÈME D'AUTHENTIFICATION D'ORDONNANCES MÉDICALES       ║")
    print("║              Signature Numérique Post-Quantique              ║")
    print("║                     Schéma Mirath                            ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("=" * 70)


def pause():

    input("\nAppuyez sur Entrée pour continuer...")


def effacer_ecran():
  
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_principal():
    
    print("\n📋 MENU PRINCIPAL")
    print("=" * 70)
    print("\nQue souhaitez-vous faire?")
    print()
    print("  [1] Agir en tant que MÉDECIN")
    print("      → Créer et signer des ordonnances")
    print()
    print("  [2] Agir en tant que PHARMACIEN")
    print("      → Vérifier l'authenticité d'ordonnances")
    print()
    print("  [3] GESTION DU SYSTÈME")
    print("      → Initialiser des médecins, voir les clés, etc.")
    print()
    print("  [4] DÉMONSTRATION COMPLÈTE")
    print("      → Exemple de bout en bout du système")
    print()
    print("  [0] QUITTER")
    print()
    print("=" * 70)
    
    choix = input("\nVotre choix: ").strip()
    return choix


def menu_medecin():
    
    print("\n⚕️  MENU MÉDECIN")
    print("=" * 70)
    print("\n  [1] Workflow complet: Créer et signer une ordonnance")
    print("  [2] Initialiser un nouveau médecin dans le système")
    print("  [3] Signer une ordonnance existante")
    print()
    print("  [0] Retour au menu principal")
    print()
    print("=" * 70)
    
    choix = input("\nVotre choix: ").strip()
    return choix


def menu_pharmacien():
    
    print("\n💊 MENU PHARMACIEN")
    print("=" * 70)
    print("\n  [1] Workflow complet: Vérifier une ordonnance")
    print("  [2] Vérification rapide d'une ordonnance")
    print()
    print("  [0] Retour au menu principal")
    print()
    print("=" * 70)
    
    choix = input("\nVotre choix: ").strip()
    return choix


def menu_gestion():
  
    print("\n⚙️  MENU GESTION")
    print("=" * 70)
    print("\n  [1] Initialiser un nouveau médecin")
    print("  [2] Lister les médecins du système")
    print("  [3] Afficher une ordonnance existante")
    print()
    print("  [0] Retour au menu principal")
    print()
    print("=" * 70)
    
    choix = input("\nVotre choix: ").strip()
    return choix


# ============================================================================
# FONCTIONS DE GESTION
# ============================================================================

def gestion_initialiser_medecin():
   
    print("\n" + "=" * 70)
    print("INITIALISATION D'UN NOUVEAU MÉDECIN")
    print("=" * 70)
    i = 0;
    while i==0:
        i = 1
        # Collecte des informations
        print("\nEntrez les informations du médecin:")
        nom = input("  Nom: ").strip()
        prenom = input("  Prénom: ").strip()
        id_medecin = input("  ID médecin (ex: MED001): ").strip()
        
        # Vérification que les champs ne sont pas vides
        if not nom or not prenom or not id_medecin:
            print("\n❌ Tous les champs doivent être remplis")
            i = 0
            #return
    
    # Initialisation
    try:
        medecin = initialiser_medecin(nom, prenom, id_medecin)
        print(f"\n✅ Médecin {id_medecin} initialisé avec succès!")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {e}")


def gestion_lister_medecins():
    """
    Liste tous les médecins enregistrés dans le système
    
    Parcourt le dossier des clés et affiche les médecins trouvés.
    """
    print("\n" + "=" * 70)
    print("LISTE DES MÉDECINS ENREGISTRÉS")
    print("=" * 70)
    
    dossier_cles = "cles_medecins"
    
    # Vérification de l'existence du dossier
    if not os.path.exists(dossier_cles):
        print("\n⚠️  Aucun médecin enregistré dans le système")
        print(f"   Le dossier {dossier_cles} n'existe pas")
        return
    
    # Parcours des fichiers
    medecins = set()  # Ensemble pour éviter les doublons
    
    for fichier in os.listdir(dossier_cles):
        if fichier.endswith("_public.json"):
            # Extraction de l'ID médecin
            id_medecin = fichier.replace("_public.json", "")
            medecins.add(id_medecin)
    
    # Affichage
    if len(medecins) == 0:
        print("\n⚠️  Aucun médecin enregistré")
    else:
        print(f"\n✓ {len(medecins)} médecin(s) trouvé(s):\n")
        for i, id_med in enumerate(sorted(medecins), 1):
            print(f"  {i}. {id_med}")


def gestion_afficher_ordonnance():
    """
    Utile pour visualiser une ordonnance sans la vérifier.
    """
    print("\n" + "=" * 70)
    print("AFFICHAGE D'UNE ORDONNANCE")
    print("=" * 70)
    
    while True:
        fichier = input("\nChemin du fichier d'ordonnance: ").strip()
        
        try:
            ordonnance = Ordonnance.charger(fichier)
            ordonnance.afficher()
            break
            
        except FileNotFoundError:
            print(f"\n❌ Fichier introuvable: {fichier}")
        except Exception as e:
            print(f"\n❌ Erreur lors du chargement: {e}")


# ============================================================================
# FONCTION DE DÉMONSTRATION
# ============================================================================

def demonstration_complete():

    print("\n" + "=" * 70)
    print("DÉMONSTRATION COMPLÈTE DU SYSTÈME")
    print("=" * 70)
    
    print("\nCette démonstration va:")
    print("  1. Créer un médecin de test")
    print("  2. Créer et signer une ordonnance")
    print("  3. Vérifier l'ordonnance comme une pharmacie")
    print()
    
    continuer = input("Voulez-vous continuer? (o/N): ").strip().lower()
    if continuer != 'o':
        return
    
    # Étape 1: Création d'un médecin de test
    print("\n" + "-" * 70)
    print("[ÉTAPE 1/3] Création d'un médecin de test")
    print("-" * 70)
    
    medecin_demo = initialiser_medecin("Démonstration", "Dr", "DEMO_001")
    pause()
    
    # Étape 2: Création et signature d'une ordonnance
    print("\n" + "-" * 70)
    print("[ÉTAPE 2/3] Création et signature d'une ordonnance")
    print("-" * 70)
    
    # Création d'une ordonnance de démonstration
    ordonnance_demo = Ordonnance(
        patient_nom="Patient",
        patient_prenom="Test",
        patient_id="PAT_DEMO_001",
        medecin_nom="Démonstration",
        medecin_prenom="Dr",
        medecin_id="DEMO_001",
        medicaments=[
            creer_medicament("Amoxicilline", "500mg", "3 fois par jour pendant 7 jours"),
            creer_medicament("Paracétamol", "1g", "En cas de fièvre, max 3g/jour")
        ]
    )
    
    print("\nOrdonnance créée:")
    ordonnance_demo.afficher()
    
    print("\n🔏 Signature de l'ordonnance...")
    if medecin_demo.signer_ordonnance(ordonnance_demo):
        # Sauvegarde
        fichier_demo = "demo_ordonnance_signee.json"
        ordonnance_demo.sauvegarder(fichier_demo)
        print(f"\n✅ Ordonnance signée et sauvegardée: {fichier_demo}")
    else:
        print("\n❌ Échec de la signature")
        return
    
    pause()
    
    # Étape 3: Vérification par une pharmacie
    print("\n" + "-" * 70)
    print("[ÉTAPE 3/3] Vérification par une pharmacie")
    print("-" * 70)
    
    # Création d'une pharmacie de test
    pharmacie_demo = Pharmacie("Pharmacie de Démonstration")
    
    # Chargement de la clé publique du médecin
    print("\nChargement de la clé publique du médecin...")
    if not pharmacie_demo.charger_cle_publique_medecin("DEMO_001"):
        print("❌ Impossible de charger la clé")
        return
    
    # Vérification de l'ordonnance
    print("\nVérification de l'ordonnance...")
    resultat = pharmacie_demo.verifier_ordonnance(ordonnance_demo)
    
    # Affichage du rapport
    pharmacie_demo.afficher_rapport_verification(ordonnance_demo, resultat)
    
    # Test de modification (démonstration de la détection de fraude)
    print("\n" + "-" * 70)
    print("[BONUS] Test de détection de modification")
    print("-" * 70)
    
    print("\nQue se passe-t-il si on modifie l'ordonnance?")
    pause()
    
    # Modification de l'ordonnance (simulation de fraude)
    ordonnance_demo.medicaments[0]['dosage'] = "1000mg"  # Doublement de la dose!
    
    print("\n⚠️  Ordonnance modifiée: dose doublée pour l'Amoxicilline")
    print("🔍 Nouvelle vérification...")
    
    resultat_modifie = pharmacie_demo.verifier_ordonnance(ordonnance_demo)
    
    if not resultat_modifie['valide']:
        print("\n✅ EXCELLENT! Le système a détecté la modification!")
        print("   La signature ne correspond plus → Ordonnance rejetée")
    else:
        print("\n❌ ERREUR: La modification n'a pas été détectée (BUG!)")
    
    print("\n" + "=" * 70)
    print("FIN DE LA DÉMONSTRATION")
    print("=" * 70)
    print("\n💡 Le système a bien détecté:")
    print("   ✓ Ordonnance valide et authentique")
    print("   ✓ Ordonnance modifiée et frauduleuse")
    print("\n🎯 Le système d'authentification fonctionne correctement!")


# ============================================================================
# BOUCLE PRINCIPALE
# ============================================================================

def main():
    """
    Fonction principale du programme
    
    Cette fonction gère la boucle principale du menu interactif.
    Elle continue de tourner jusqu'à ce que l'utilisateur choisisse de quitter.
    """
    # Affichage de la bannière au démarrage
    afficher_banniere()
    
    print("\n🚀 Bienvenue dans le système d'authentification d'ordonnances!")
    print("   Ce système utilise la cryptographie post-quantique Mirath")
    print("   pour garantir l'authenticité et l'intégrité des prescriptions médicales.")
    
    pause()
    
    # Boucle principale
    while True:
        effacer_ecran()
        afficher_banniere()
        
        # Affichage du menu principal et récupération du choix
        choix = menu_principal()
        
        # Traitement du choix
        if choix == '1':
            # Menu médecin
            while True:
                effacer_ecran()
                afficher_banniere()
                choix_medecin = menu_medecin()
                
                if choix_medecin == '1':
                    workflow_signature_ordonnance()
                    pause()
                elif choix_medecin == '2':
                    gestion_initialiser_medecin()
                    pause()
                elif choix_medecin == '3':
                    print("\n⚠️  Fonction non encore implémentée")
                    pause()
                elif choix_medecin == '0':
                    break
                else:
                    print("\n❌ Choix invalide")
                    pause()
        
        elif choix == '2':
            # Menu pharmacien
            while True:
                effacer_ecran()
                afficher_banniere()
                choix_pharmacien = menu_pharmacien()
                
                if choix_pharmacien == '1':
                    workflow_verification_ordonnance()
                    pause()
                elif choix_pharmacien == '2':
                    print("\n📋 VÉRIFICATION RAPIDE")
                    fichier = input("Fichier d'ordonnance: ").strip()
                    from pharmacie import verifier_ordonnance_simple
                    verifier_ordonnance_simple(fichier)
                    pause()
                elif choix_pharmacien == '0':
                    break
                else:
                    print("\n❌ Choix invalide")
                    pause()
        
        elif choix == '3':
            # Menu gestion
            while True:
                effacer_ecran()
                afficher_banniere()
                choix_gestion = menu_gestion()
                
                if choix_gestion == '1':
                    gestion_initialiser_medecin()
                    pause()
                elif choix_gestion == '2':
                    gestion_lister_medecins()
                    pause()
                elif choix_gestion == '3':
                    gestion_afficher_ordonnance()
                    pause()
                elif choix_gestion == '0':
                    break
                else:
                    print("\n❌ Choix invalide")
                    pause()
        
        elif choix == '4':
            # Démonstration
            demonstration_complete()
            pause()
        
        elif choix == '0':
            # Quitter
            print("\n" + "=" * 70)
            print("👋 Merci d'avoir utilisé le système!")
            print("   À bientôt!")
            print("=" * 70)
            break
        
        else:
            print("\n❌ Choix invalide. Veuillez choisir un numéro du menu.")
            pause()


# ============================================================================
# POINT D'ENTRÉE DU PROGRAMME
# ============================================================================

if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        # Gestion de Ctrl+C (interruption par l'utilisateur)
        print("\n\n⚠️  Programme interrompu par l'utilisateur")
        print("   Au revoir!")
    except Exception as e:
        # Gestion des erreurs inattendues
        print("\n\n❌ ERREUR CRITIQUE")
        print(f"   {type(e).__name__}: {e}")
        print("\n💡 Si l'erreur persiste:")
        print("   1. Vérifiez que tous les fichiers sont présents")
        print("   2. Vérifiez que numpy est installé: pip install numpy")
        print("   3. Contactez le support")
