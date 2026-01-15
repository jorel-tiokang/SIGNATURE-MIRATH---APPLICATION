"""
ordonnance.py - Gestion des Ordonnances Médicales
==================================================

Ce fichier définit la structure d'une ordonnance médicale et fournit
les fonctions pour créer, sauvegarder et charger des ordonnances.

Une ordonnance contient:
- Informations du patient
- Informations du médecin
- Liste des médicaments prescrits
- Date de prescription
- Signature numérique Mirath
"""

import json
from datetime import datetime
from typing import Dict, List


# ============================================================================
# CLASSE ORDONNANCE
# ============================================================================

class Ordonnance:
    """
    Représente une ordonnance médicale complète
    
    Cette classe encapsule toutes les informations d'une ordonnance
    et permet de la convertir en format signable (string).
    """
    
    def __init__(self, 
                 patient_nom: str,
                 patient_prenom: str,
                 patient_id: str,
                 medecin_nom: str,
                 medecin_prenom: str,
                 medecin_id: str,
                 medicaments: List[Dict[str, str]],
                 date_prescription: str = None):
       
        # Informations du patient
        self.patient_nom = patient_nom
        self.patient_prenom = patient_prenom
        self.patient_id = patient_id
        
        # Informations du médecin
        self.medecin_nom = medecin_nom
        self.medecin_prenom = medecin_prenom
        self.medecin_id = medecin_id
        
        # Médicaments prescrits
        self.medicaments = medicaments
        
        # Date de prescription (si non fournie, on prend la date actuelle)
        if date_prescription is None:
            self.date_prescription = datetime.now().isoformat()
        else:
            self.date_prescription = date_prescription
        
        # La signature sera ajoutée plus tard par le médecin
        self.signature = None
    
    def to_signable_message(self) -> str:
        """
        Convertit l'ordonnance en message signable
        
        Cette fonction crée une représentation textuelle canonique
        de l'ordonnance qui sera signée par le médecin.
        
        Le format est standardisé pour que:
        - La même ordonnance produise toujours le même message
        - Toute modification soit détectable
        
        Returns:
            String représentant l'ordonnance de manière unique
        """
        # Construction du message ligne par ligne
        lignes = [
            "=== ORDONNANCE MÉDICALE ===",
            f"Date: {self.date_prescription}",
            "",
            "PATIENT:",
            f"  Nom: {self.patient_nom}",
            f"  Prénom: {self.patient_prenom}",
            f"  ID: {self.patient_id}",
            "",
            "MÉDECIN PRESCRIPTEUR:",
            f"  Dr. {self.medecin_prenom} {self.medecin_nom}",
            f"  ID: {self.medecin_id}",
            "",
            "MÉDICAMENTS PRESCRITS:"
        ]
        
        # Ajout de chaque médicament
        for i, med in enumerate(self.medicaments, 1):
            lignes.append(f"  {i}. {med['nom']}")
            lignes.append(f"     Dosage: {med['dosage']}")
            lignes.append(f"     Posologie: {med['posologie']}")
        
        # Jointure avec des retours à la ligne
        return "\n".join(lignes)
    
    def to_dict(self) -> Dict:
      
        return {
            'patient': {
                'nom': self.patient_nom,
                'prenom': self.patient_prenom,
                'id': self.patient_id
            },
            'medecin': {
                'nom': self.medecin_nom,
                'prenom': self.medecin_prenom,
                'id': self.medecin_id
            },
            'medicaments': self.medicaments,
            'date_prescription': self.date_prescription,
            'signature': self.signature
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Ordonnance':
        """
        Crée une ordonnance à partir d'un dictionnaire
        
        Fonction inverse de to_dict(), utilisée pour charger
        des ordonnances depuis des fichiers JSON.
        """
        # Création de l'ordonnance
        ordonnance = cls(
            patient_nom=data['patient']['nom'],
            patient_prenom=data['patient']['prenom'],
            patient_id=data['patient']['id'],
            medecin_nom=data['medecin']['nom'],
            medecin_prenom=data['medecin']['prenom'],
            medecin_id=data['medecin']['id'],
            medicaments=data['medicaments'],
            date_prescription=data['date_prescription']
        )
        
        # Ajout de la signature si elle existe
        ordonnance.signature = data.get('signature')
        
        return ordonnance
    
    def sauvegarder(self, nom_fichier: str):
    
        # Conversion en dictionnaire
        data = self.to_dict()
        
        # Écriture dans le fichier avec indentation pour lisibilité
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Ordonnance sauvegardée dans: {nom_fichier}")
    
    @staticmethod
    def charger(nom_fichier: str) -> 'Ordonnance':
        
        # Lecture du fichier
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Création de l'ordonnance depuis les données
        return Ordonnance.from_dict(data)
    
    def afficher(self):
        
        print("\n" + "=" * 70)
        print("ORDONNANCE MÉDICALE")
        print("=" * 70)
        
        print(f"\n📅 Date: {self.date_prescription}")
        
        print("\n👤 PATIENT:")
        print(f"   {self.patient_prenom} {self.patient_nom}")
        print(f"   ID: {self.patient_id}")
        
        print("\n⚕️  MÉDECIN PRESCRIPTEUR:")
        print(f"   Dr. {self.medecin_prenom} {self.medecin_nom}")
        print(f"   ID: {self.medecin_id}")
        
        print("\n💊 MÉDICAMENTS PRESCRITS:")
        for i, med in enumerate(self.medicaments, 1):
            print(f"\n   {i}. {med['nom']}")
            print(f"      • Dosage: {med['dosage']}")
            print(f"      • Posologie: {med['posologie']}")
        
        # Affichage du statut de signature
        print("\n🔐 SIGNATURE NUMÉRIQUE:")
        if self.signature:
            print("   ✓ Ordonnance signée numériquement")
            print("   ✓ Signature Mirath présente")
        else:
            print("   ✗ Ordonnance non signée")
        
        print("\n" + "=" * 70)


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def creer_medicament(nom: str, dosage: str, posologie: str) -> Dict[str, str]:

    return {
        'nom': nom,
        'dosage': dosage,
        'posologie': posologie
    }


def creer_ordonnance_interactive() -> Ordonnance:
    
    print("\n" + "=" * 70)
    print("CRÉATION D'UNE NOUVELLE ORDONNANCE")
    print("=" * 70)
    
    # Informations du patient
    print("\n📋 INFORMATIONS DU PATIENT:")
    patient_nom = input("  Nom du patient: ").strip()
    patient_prenom = input("  Prénom du patient: ").strip()
    patient_id = input("  ID du patient: ").strip()
    
    # Informations du médecin
    print("\n⚕️  INFORMATIONS DU MÉDECIN:")
    medecin_nom = input("  Nom du médecin: ").strip()
    medecin_prenom = input("  Prénom du médecin: ").strip()
    medecin_id = input("  ID du médecin: ").strip()
    
    # Médicaments
    print("\n💊 MÉDICAMENTS À PRESCRIRE:")
    medicaments = []
    
    while True:
        print(f"\n  Médicament #{len(medicaments) + 1}:")
        nom = input("    Nom du médicament: ").strip()
        
        # Si l'utilisateur ne saisit rien, on arrête
        if not nom:
            if len(medicaments) == 0:
                print("    ⚠️  Au moins un médicament doit être prescrit!")
                continue
            else:
                break
        
        dosage = input("    Dosage (ex: 500mg): ").strip()
        posologie = input("    Posologie (ex: 3 fois/jour pendant 7 jours): ").strip()
        
        # Ajout du médicament à la liste
        medicaments.append(creer_medicament(nom, dosage, posologie))
        
        # Demande si on continue
        continuer = input("\n  Ajouter un autre médicament? (o/N): ").strip().lower()
        if continuer != 'o':
            break
    
    # Création de l'ordonnance
    ordonnance = Ordonnance(
        patient_nom=patient_nom,
        patient_prenom=patient_prenom,
        patient_id=patient_id,
        medecin_nom=medecin_nom,
        medecin_prenom=medecin_prenom,
        medecin_id=medecin_id,
        medicaments=medicaments
    )
    
    print("\n✓ Ordonnance créée avec succès!")
    return ordonnance


# ============================================================================
# TEST DU MODULE
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("TEST DU MODULE ORDONNANCE")
    print("=" * 70)
    
    # Test 1: Création d'une ordonnance
    print("\n[TEST 1] Création d'une ordonnance...")
    ordonnance_test = Ordonnance(
        patient_nom="Dupont",
        patient_prenom="Jean",
        patient_id="PAT001",
        medecin_nom="Martin",
        medecin_prenom="Sophie",
        medecin_id="MED001",
        medicaments=[
            creer_medicament("Amoxicilline", "500mg", "3 fois par jour pendant 7 jours"),
            creer_medicament("Paracétamol", "1g", "En cas de douleur, max 3g/jour")
        ]
    )
    print("✓ Ordonnance créée")
    
    print("\n[TEST 2] Affichage de l'ordonnance...")
    ordonnance_test.afficher()
    
    print("\n[TEST 3] Conversion en message signable...")
    message = ordonnance_test.to_signable_message()
    print("Message généré:")
    print(message)
    
    print("\n[TEST 4] Sauvegarde et chargement...")
    nom_fichier = "test_ordonnance.json"
    ordonnance_test.sauvegarder(nom_fichier)
    
    ordonnance_chargee = Ordonnance.charger(nom_fichier)
    print("✓ Ordonnance chargée depuis le fichier")
    
    # Vérification que les données sont identiques
    if ordonnance_chargee.to_signable_message() == message:
        print("✓ Les données sont identiques après chargement")
    else:
        print("✗ Erreur: les données diffèrent après chargement")
    
    print("\n" + "=" * 70)
    print("TESTS COMPLÉTÉS")
    print("=" * 70)
