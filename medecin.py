"""
medecin.py - Module pour les Médecins Prescripteurs
====================================================

Ce fichier contient les fonctions permettant aux médecins de:
- Générer leurs paires de clés Mirath
- Signer des ordonnances médicales
- Gérer leurs clés de signature

Un médecin possède une clé privée (gardée secrète) et une clé publique
(partagée avec les pharmacies pour vérifier ses prescriptions).
"""

import os
from mirath import MirathSignature
from ordonnance import Ordonnance


# ============================================================================
# CLASSE MÉDECIN
# ============================================================================

class Medecin:
    """
    Représente un médecin avec sa capacité de signer des ordonnances
    
    Cette classe encapsule toutes les opérations qu'un médecin peut
    effectuer dans le système d'authentification.
    """
    
    def __init__(self, nom: str, prenom: str, id_medecin: str):
       
        self.nom = nom
        self.prenom = prenom
        self.id_medecin = id_medecin
        
        # Système de signature Mirath
        self.mirath = MirathSignature()
        
        # Clés de signature
        self.public_key = None
        self.secret_key = None
    
    def generer_cles(self):
       
        print(f"\n🔑 Génération des clés Mirath pour Dr. {self.prenom} {self.nom}...")
        
        # Génération de la paire de clés via le module Mirath
        self.public_key, self.secret_key = self.mirath.generate_keypair()
        
        print("   ✓ Clés générées avec succès!")
        print(f"   ✓ Clé publique: prête à être partagée")
        print(f"   ✓ Clé secrète: CONFIDENTIELLE - ne jamais partager!")
    
    def sauvegarder_cles(self, dossier: str = "cles_medecins"):
        """
        Sauvegarde les clés du médecin dans des fichiers
        
        Crée deux fichiers:
        - {id_medecin}_public.json : clé publique (peut être partagée)
        - {id_medecin}_secret.json : clé secrète (CONFIDENTIELLE)
        
        Args:
            dossier: Dossier où sauvegarder les clés
        """
        # Vérification que les clés existent
        if self.public_key is None or self.secret_key is None:
            print("❌ Erreur: Aucune clé à sauvegarder. Générez d'abord les clés.")
            return
        
        # Création du dossier s'il n'existe pas
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            print(f"✓ Dossier créé: {dossier}")
        
        # Construction des noms de fichiers
        prefix = os.path.join(dossier, self.id_medecin)
        
        # Sauvegarde via le module Mirath
        self.mirath.export_keys(self.public_key, self.secret_key, prefix)
        
        print(f"\n💾 Clés sauvegardées:")
        print(f"   • Clé publique : {prefix}_public.json")
        print(f"   • Clé secrète  : {prefix}_secret.json")
        print(f"\n⚠️  ATTENTION: Gardez le fichier secret en lieu sûr!")
    
    def charger_cles(self, dossier: str = "cles_medecins"):
        
        # Construction des chemins de fichiers
        prefix = os.path.join(dossier, self.id_medecin)
        fichier_public = f"{prefix}_public.json"
        fichier_secret = f"{prefix}_secret.json"
        
        # Vérification de l'existence des fichiers
        if not os.path.exists(fichier_public) or not os.path.exists(fichier_secret):
            print(f"❌ Erreur: Fichiers de clés introuvables pour {self.id_medecin}")
            print(f"   Cherché dans: {dossier}")
            return False
        
        try:
            # Chargement des clés
            self.public_key, self.secret_key = MirathSignature.load_keys(
                fichier_public, 
                fichier_secret
            )
            
            print(f"✓ Clés chargées pour Dr. {self.prenom} {self.nom}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des clés: {e}")
            return False
    
    def signer_ordonnance(self, ordonnance: Ordonnance):
        """
        1. Convertit l'ordonnance en message signable
        2. Crée une signature Mirath
        3. Attache la signature à l'ordonnance
        """
        # Vérification que les clés sont disponibles
        if self.secret_key is None:
            print("❌ Erreur: Clé secrète non disponible. Chargez ou générez vos clés.")
            return False
        
        # Vérification que le médecin correspond à l'ordonnance
        if ordonnance.medecin_id != self.id_medecin:
            print(f"❌ Erreur: L'ordonnance n'est pas prescrite par ce médecin")
            print(f"   Ordonnance pour: {ordonnance.medecin_id}")
            print(f"   Médecin actuel: {self.id_medecin}")
            return False
        
        print(f"\n✍️  Signature de l'ordonnance en cours...")
        
        try:
            # Conversion de l'ordonnance en message
            message = ordonnance.to_signable_message()
            
            # Création de la signature Mirath
            signature = self.mirath.sign(message, self.secret_key)
            
            # Attachement de la signature à l'ordonnance
            ordonnance.signature = signature
            
            print("   ✓ Ordonnance signée avec succès!")
            print("   ✓ Signature Mirath appliquée")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la signature: {e}")
            return False


# ============================================================================
# FONCTIONS UTILITAIRES POUR LE MODULE MÉDECIN
# ============================================================================

def initialiser_medecin(nom: str, prenom: str, id_medecin: str) -> Medecin:
   
    print("\n" + "=" * 70)
    print("INITIALISATION D'UN NOUVEAU MÉDECIN")
    print("=" * 70)
    
    # Création de l'instance
    medecin = Medecin(nom, prenom, id_medecin)
    
    # Génération des clés
    medecin.generer_cles()
    
    # Sauvegarde
    medecin.sauvegarder_cles()
    
    print("\n✅ Médecin initialisé avec succès!")
    print(f"   Dr. {prenom} {nom} (ID: {id_medecin})")
    print(f"   Les clés ont été sauvegardées dans: cles_medecins/")
    
    return medecin


def charger_medecin_existant(id_medecin: str) -> Medecin:
    """
    Charge un médecin existant avec ses clés
    
    Permet à un médecin déjà enregistré de se reconnecter
    au système pour signer de nouvelles ordonnances.
    """
    print(f"\n🔍 Chargement du médecin {id_medecin}...")
    
    # Création d'une instance temporaire pour charger les clés
    # On n'a pas encore le nom/prénom, mais ce n'est pas grave
    # pour charger les clés
    medecin = Medecin("", "", id_medecin)
    
    # Tentative de chargement des clés
    if medecin.charger_cles():
        print("✅ Médecin chargé avec succès!")
        return medecin
    else:
        print("❌ Impossible de charger le médecin")
        return None


def workflow_signature_ordonnance():
    """
    1. Identification du médecin
    2. Chargement de ses clés
    3. Création ou chargement d'une ordonnance
    4. Signature de l'ordonnance
    5. Sauvegarde de l'ordonnance signée
    """
    print("\n" + "=" * 70)
    print("WORKFLOW: SIGNATURE D'ORDONNANCE MÉDICALE")
    print("=" * 70)
    
    # Étape 1: Identification du médecin
    print("\n[Étape 1/5] Identification du médecin")
    id_medecin = input("  Entrez votre ID médecin: ").strip()
    
    # Tentative de chargement
    medecin = charger_medecin_existant(id_medecin)
    
    if medecin is None:
        print("\n⚠️  Ce médecin n'existe pas encore dans le système.")
        initialiser = input("  Voulez-vous l'initialiser? (o/N): ").strip().lower()
        
        if initialiser == 'o':
            nom = input("  Nom: ").strip()
            prenom = input("  Prénom: ").strip()
            medecin = initialiser_medecin(nom, prenom, id_medecin)
        else:
            print("❌ Abandon de l'opération")
            return
    
    # Étape 2: Choix de l'ordonnance
    print("\n[Étape 2/5] Sélection de l'ordonnance")
    print("  1. Créer une nouvelle ordonnance")
    print("  2. Charger une ordonnance existante")
    
    choix = input("  Votre choix (1 ou 2): ").strip()
    
    if choix == '1':
        # Création d'une nouvelle ordonnance
        from ordonnance import creer_ordonnance_interactive
        ordonnance = creer_ordonnance_interactive()
    elif choix == '2':
        # Chargement d'une ordonnance existante
        fichier = input("  Nom du fichier d'ordonnance: ").strip()
        try:
            ordonnance = Ordonnance.charger(fichier)
            print("✓ Ordonnance chargée")
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return
    else:
        print("❌ Choix invalide")
        return
    
    # Étape 3: Affichage de l'ordonnance
    print("\n[Étape 3/5] Vérification de l'ordonnance")
    ordonnance.afficher()
    
    # Étape 4: Confirmation et signature
    print("\n[Étape 4/5] Signature numérique")
    confirmer = input("  Voulez-vous signer cette ordonnance? (o/N): ").strip().lower()
    
    if confirmer != 'o':
        print("❌ Signature annulée")
        return
    
    # Signature de l'ordonnance
    if not medecin.signer_ordonnance(ordonnance):
        print("❌ Échec de la signature")
        return
    
    # Étape 5: Sauvegarde
    print("\n[Étape 5/5] Sauvegarde de l'ordonnance signée")
    nom_fichier = input("  Nom du fichier de sauvegarde (ex: ordonnance_patient.json): ").strip()
    
    if not nom_fichier.endswith('.json'):
        nom_fichier += '.json'
    
    ordonnance.sauvegarder(nom_fichier)
    
    print("\n" + "=" * 70)
    print("✅ ORDONNANCE SIGNÉE ET SAUVEGARDÉE AVEC SUCCÈS!")
    print("=" * 70)
    print(f"\nL'ordonnance peut maintenant être vérifiée par une pharmacie.")
    print(f"Fichier: {nom_fichier}")


# ============================================================================
# TEST DU MODULE
# ============================================================================

if __name__ == "__main__":
    """
    Code de test pour vérifier le fonctionnement du module médecin
    """
    print("=" * 70)
    print("TEST DU MODULE MÉDECIN")
    print("=" * 70)
    
    # Test 1: Création et initialisation d'un médecin
    print("\n[TEST 1] Création d'un médecin...")
    medecin_test = initialiser_medecin("Martin", "Sophie", "MED_TEST_001")
    
    # Test 2: Chargement d'un médecin existant
    print("\n[TEST 2] Chargement du médecin...")
    medecin_charge = charger_medecin_existant("MED_TEST_001")
    
    if medecin_charge:
        print("✓ Médecin rechargé avec succès")
    
    # Test 3: Création et signature d'une ordonnance
    print("\n[TEST 3] Création et signature d'une ordonnance...")
    from ordonnance import Ordonnance, creer_medicament
    
    ordonnance_test = Ordonnance(
        patient_nom="Dupont",
        patient_prenom="Jean",
        patient_id="PAT001",
        medecin_nom="Martin",
        medecin_prenom="Sophie",
        medecin_id="MED_TEST_001",
        medicaments=[
            creer_medicament("Amoxicilline", "500mg", "3 fois par jour pendant 7 jours")
        ]
    )
    
    # Signature
    if medecin_charge.signer_ordonnance(ordonnance_test):
        print("✓ Ordonnance signée")
        
        # Sauvegarde
        ordonnance_test.sauvegarder("test_ordonnance_signee.json")
    
    print("\n" + "=" * 70)
    print("TESTS COMPLÉTÉS")
    print("=" * 70)
