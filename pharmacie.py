"""
pharmacie.py - Module pour les Pharmacies
==========================================

Ce fichier contient les fonctions permettant aux pharmaciens de:
- Charger les clés publiques des médecins
- Vérifier l'authenticité des ordonnances signées
- Valider que les ordonnances n'ont pas été modifiées

Une pharmacie a accès aux clés publiques des médecins (mais pas aux clés privées)
pour pouvoir vérifier les signatures sans pouvoir en créer de fausses.
"""

import os
from mirath import MirathSignature
from ordonnance import Ordonnance


# ============================================================================
# CLASSE PHARMACIE
# ============================================================================

class Pharmacie:
    """
    Représente une pharmacie avec sa capacité de vérifier des ordonnances
    
    Cette classe encapsule toutes les opérations de vérification
    qu'une pharmacie peut effectuer dans le système.
    """
    
    def __init__(self, nom_pharmacie: str):
        """
        Initialise une pharmacie
        
        Args:
            nom_pharmacie: Nom de la pharmacie
        """
        self.nom_pharmacie = nom_pharmacie
        
        # Système de vérification Mirath
        self.mirath = MirathSignature()
        
        # Registre des clés publiques des médecins
        # Dictionnaire: {id_medecin: public_key}
        self.cles_publiques_medecins = {}
    
    def charger_cle_publique_medecin(self, id_medecin: str, dossier: str = "cles_medecins"):
        """
        Charge la clé publique d'un médecin
        
        Les pharmacies ont besoin des clés publiques des médecins
        pour vérifier leurs signatures. Ces clés peuvent être partagées
        sans risque de sécurité.
        
        Args:
            id_medecin: Identifiant du médecin
            dossier: Dossier contenant les clés publiques
            
        Returns:
            True si le chargement réussit, False sinon
        """
        # Construction du chemin du fichier
        fichier_public = os.path.join(dossier, f"{id_medecin}_public.json")
        
        # Vérification de l'existence du fichier
        if not os.path.exists(fichier_public):
            print(f"❌ Erreur: Clé publique introuvable pour {id_medecin}")
            print(f"   Fichier cherché: {fichier_public}")
            return False
        
        try:
            # Chargement de la clé publique
            public_key, _ = MirathSignature.load_keys(fichier_public, None)
            
            # Ajout au registre
            self.cles_publiques_medecins[id_medecin] = public_key
            
            print(f"✓ Clé publique chargée pour médecin {id_medecin}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def charger_toutes_cles_publiques(self, dossier: str = "cles_medecins"):
        """
        Charge toutes les clés publiques disponibles dans un dossier
        
        Pratique pour initialiser la pharmacie avec toutes les clés
        publiques des médecins du système.
        
        Args:
            dossier: Dossier contenant les clés publiques
            
        Returns:
            Nombre de clés chargées
        """
        print(f"\n📂 Chargement des clés publiques depuis {dossier}...")
        
        # Vérification de l'existence du dossier
        if not os.path.exists(dossier):
            print(f"❌ Dossier introuvable: {dossier}")
            return 0
        
        # Parcours de tous les fichiers du dossier
        compteur = 0
        for fichier in os.listdir(dossier):
            # On ne charge que les fichiers de clés publiques
            if fichier.endswith("_public.json"):
                # Extraction de l'ID médecin depuis le nom du fichier
                id_medecin = fichier.replace("_public.json", "")
                
                # Tentative de chargement
                if self.charger_cle_publique_medecin(id_medecin, dossier):
                    compteur += 1
        
        print(f"\n✓ {compteur} clé(s) publique(s) chargée(s)")
        return compteur
    
    def verifier_ordonnance(self, ordonnance: Ordonnance) -> dict:
        """
        Vérifie l'authenticité et l'intégrité d'une ordonnance signée
        
        Cette fonction effectue plusieurs vérifications:
        1. L'ordonnance possède-t-elle une signature?
        2. La clé publique du médecin est-elle disponible?
        3. La signature est-elle valide?
        4. L'ordonnance a-t-elle été modifiée?
        
        Args:
            ordonnance: Ordonnance à vérifier
            
        Returns:
            Dictionnaire contenant:
            - 'valide': bool - True si l'ordonnance est valide
            - 'raison': str - Raison du résultat
            - 'details': dict - Détails supplémentaires
        """
        print(f"\n🔍 Vérification de l'ordonnance...")
        
        resultat = {
            'valide': False,
            'raison': '',
            'details': {}
        }
        
        # Vérification 1: L'ordonnance est-elle signée?
        if ordonnance.signature is None:
            resultat['raison'] = "L'ordonnance n'est pas signée"
            print(f"   ❌ {resultat['raison']}")
            return resultat
        
        print("   ✓ L'ordonnance possède une signature")
        
        # Vérification 2: Clé publique du médecin disponible?
        id_medecin = ordonnance.medecin_id
        
        if id_medecin not in self.cles_publiques_medecins:
            resultat['raison'] = f"Clé publique du médecin {id_medecin} non disponible"
            print(f"   ❌ {resultat['raison']}")
            print(f"   💡 Conseil: Chargez la clé publique du médecin")
            return resultat
        
        print(f"   ✓ Clé publique du médecin {id_medecin} disponible")
        
        # Vérification 3: Validation de la signature Mirath
        try:
            # Récupération de la clé publique
            public_key = self.cles_publiques_medecins[id_medecin]
            
            # Conversion de l'ordonnance en message
            message = ordonnance.to_signable_message()
            
            # Vérification de la signature
            print("   ⏳ Vérification cryptographique en cours...")
            est_valide = self.mirath.verify(message, ordonnance.signature, public_key)
            
            if est_valide:
                resultat['valide'] = True
                resultat['raison'] = "Signature valide - Ordonnance authentique"
                resultat['details'] = {
                    'medecin': f"Dr. {ordonnance.medecin_prenom} {ordonnance.medecin_nom}",
                    'patient': f"{ordonnance.patient_prenom} {ordonnance.patient_nom}",
                    'date': ordonnance.date_prescription,
                    'nb_medicaments': len(ordonnance.medicaments)
                }
                print(f"   ✅ {resultat['raison']}")
            else:
                resultat['raison'] = "Signature invalide - Ordonnance altérée ou contrefaite"
                print(f"   ❌ {resultat['raison']}")
                print(f"   ⚠️  L'ordonnance a peut-être été modifiée après signature")
            
        except Exception as e:
            resultat['raison'] = f"Erreur lors de la vérification: {str(e)}"
            print(f"   ❌ {resultat['raison']}")
        
        return resultat
    
    def afficher_rapport_verification(self, ordonnance: Ordonnance, resultat: dict):
        """
        Affiche un rapport détaillé de la vérification
        
        Cette fonction présente les résultats de vérification de manière
        claire et professionnelle pour le pharmacien.
        
        Args:
            ordonnance: Ordonnance vérifiée
            resultat: Résultat de la vérification
        """
        print("\n" + "=" * 70)
        print("RAPPORT DE VÉRIFICATION D'ORDONNANCE")
        print("=" * 70)
        
        # En-tête avec statut
        if resultat['valide']:
            print("\n✅ ORDONNANCE VALIDE ET AUTHENTIQUE")
        else:
            print("\n❌ ORDONNANCE INVALIDE OU SUSPECTE")
        
        print("\n📋 INFORMATIONS:")
        print(f"   Pharmacie vérificatrice: {self.nom_pharmacie}")
        print(f"   Raison du résultat: {resultat['raison']}")
        
        # Affichage des détails si disponibles
        if 'details' in resultat and resultat['details']:
            print("\n📄 DÉTAILS DE L'ORDONNANCE:")
            for cle, valeur in resultat['details'].items():
                print(f"   {cle}: {valeur}")
        
        # Affichage de l'ordonnance complète
        ordonnance.afficher()
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        if resultat['valide']:
            print("   • Vous pouvez délivrer les médicaments prescrits")
            print("   • Vérifiez l'identité du patient")
            print("   • Archivez cette ordonnance conformément à la réglementation")
        else:
            print("   • NE PAS DÉLIVRER les médicaments")
            print("   • Contactez le médecin prescripteur pour vérification")
            print("   • Signalez toute tentative de fraude aux autorités")
        
        print("\n" + "=" * 70)


# ============================================================================
# FONCTIONS UTILITAIRES POUR LE MODULE PHARMACIE
# ============================================================================

def workflow_verification_ordonnance():
    """
    Workflow complet pour qu'une pharmacie vérifie une ordonnance
    
    Cette fonction guide l'utilisateur (pharmacien) à travers toutes les étapes:
    1. Identification de la pharmacie
    2. Chargement des clés publiques
    3. Chargement de l'ordonnance à vérifier
    4. Vérification de l'authenticité
    5. Affichage du rapport de vérification
    """
    print("\n" + "=" * 70)
    print("WORKFLOW: VÉRIFICATION D'ORDONNANCE MÉDICALE")
    print("=" * 70)
    
    # Étape 1: Identification de la pharmacie
    print("\n[Étape 1/4] Identification de la pharmacie")
    nom_pharmacie = input("  Nom de la pharmacie: ").strip()
    
    # Création de l'instance pharmacie
    pharmacie = Pharmacie(nom_pharmacie)
    
    # Étape 2: Chargement des clés publiques
    print("\n[Étape 2/4] Chargement des clés publiques des médecins")
    print("  1. Charger toutes les clés disponibles")
    print("  2. Charger la clé d'un médecin spécifique")
    
    choix = input("  Votre choix (1 ou 2): ").strip()
    
    if choix == '1':
        # Chargement de toutes les clés
        nb_cles = pharmacie.charger_toutes_cles_publiques()
        if nb_cles == 0:
            print("⚠️  Aucune clé publique chargée. Vérification impossible.")
            return
    elif choix == '2':
        # Chargement d'une clé spécifique
        id_medecin = input("  ID du médecin: ").strip()
        if not pharmacie.charger_cle_publique_medecin(id_medecin):
            print("⚠️  Impossible de charger la clé. Vérification impossible.")
            return
    else:
        print("❌ Choix invalide")
        return
    
    # Étape 3: Chargement de l'ordonnance
    print("\n[Étape 3/4] Chargement de l'ordonnance à vérifier")
    fichier_ordonnance = input("  Chemin du fichier d'ordonnance: ").strip()
    
    try:
        ordonnance = Ordonnance.charger(fichier_ordonnance)
        print("✓ Ordonnance chargée")
    except FileNotFoundError:
        print(f"❌ Fichier introuvable: {fichier_ordonnance}")
        return
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return
    
    # Étape 4: Vérification
    print("\n[Étape 4/4] Vérification de l'authenticité")
    
    # Si le médecin n'est pas dans le registre, on propose de charger sa clé
    if ordonnance.medecin_id not in pharmacie.cles_publiques_medecins:
        print(f"\n⚠️  La clé publique du médecin {ordonnance.medecin_id} n'est pas chargée")
        charger = input("  Voulez-vous la charger maintenant? (o/N): ").strip().lower()
        
        if charger == 'o':
            if not pharmacie.charger_cle_publique_medecin(ordonnance.medecin_id):
                print("❌ Impossible de vérifier l'ordonnance")
                return
        else:
            print("❌ Vérification annulée")
            return
    
    # Vérification de l'ordonnance
    resultat = pharmacie.verifier_ordonnance(ordonnance)
    
    # Affichage du rapport
    pharmacie.afficher_rapport_verification(ordonnance, resultat)
    
    # Proposition de sauvegarder le rapport
    print("\n💾 Sauvegarde du rapport")
    sauvegarder = input("  Voulez-vous sauvegarder un rapport de vérification? (o/N): ").strip().lower()
    
    if sauvegarder == 'o':
        nom_rapport = input("  Nom du fichier de rapport: ").strip()
        if not nom_rapport.endswith('.txt'):
            nom_rapport += '.txt'
        
        # Création d'un rapport textuel
        with open(nom_rapport, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RAPPORT DE VÉRIFICATION D'ORDONNANCE\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Pharmacie: {nom_pharmacie}\n")
            f.write(f"Date de vérification: {ordonnance.date_prescription}\n")
            f.write(f"Statut: {'VALIDE' if resultat['valide'] else 'INVALIDE'}\n")
            f.write(f"Raison: {resultat['raison']}\n\n")
            f.write("Ordonnance:\n")
            f.write(ordonnance.to_signable_message())
        
        print(f"✓ Rapport sauvegardé: {nom_rapport}")
    
    print("\n" + "=" * 70)
    print("✅ VÉRIFICATION TERMINÉE")
    print("=" * 70)


def verifier_ordonnance_simple(fichier_ordonnance: str, 
                               id_medecin: str = None,
                               nom_pharmacie: str = "Pharmacie Test"):
    """
    Fonction simplifiée pour vérifier rapidement une ordonnance
    
    Cette fonction est utile pour des tests rapides ou des scripts
    automatisés.
    
    Args:
        fichier_ordonnance: Chemin du fichier d'ordonnance
        id_medecin: ID du médecin (optionnel, sera extrait de l'ordonnance)
        nom_pharmacie: Nom de la pharmacie
        
    Returns:
        True si l'ordonnance est valide, False sinon
    """
    # Création de la pharmacie
    pharmacie = Pharmacie(nom_pharmacie)
    
    # Chargement de l'ordonnance
    try:
        ordonnance = Ordonnance.charger(fichier_ordonnance)
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return False
    
    # Détermination de l'ID médecin si non fourni
    if id_medecin is None:
        id_medecin = ordonnance.medecin_id
    
    # Chargement de la clé publique
    if not pharmacie.charger_cle_publique_medecin(id_medecin):
        return False
    
    # Vérification
    resultat = pharmacie.verifier_ordonnance(ordonnance)
    
    # Affichage du rapport
    pharmacie.afficher_rapport_verification(ordonnance, resultat)
    
    return resultat['valide']


# ============================================================================
# TEST DU MODULE
# ============================================================================

if __name__ == "__main__":
    """
    Code de test pour vérifier le fonctionnement du module pharmacie
    """
    print("=" * 70)
    print("TEST DU MODULE PHARMACIE")
    print("=" * 70)
    
    # Pour tester ce module, on a besoin d'une ordonnance signée
    # Vérifiez d'abord que le fichier test_ordonnance_signee.json existe
    # (créé par les tests du module medecin.py)
    
    print("\n[TEST] Vérification d'une ordonnance de test...")
    
    fichier_test = "test_ordonnance_signee.json"
    
    if os.path.exists(fichier_test):
        verifier_ordonnance_simple(fichier_test, "MED_TEST_001", "Pharmacie de Test")
    else:
        print(f"⚠️  Fichier de test non trouvé: {fichier_test}")
        print("   Exécutez d'abord medecin.py pour créer une ordonnance signée")
    
    print("\n" + "=" * 70)
    print("TESTS COMPLÉTÉS")
    print("=" * 70)