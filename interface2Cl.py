"""
gui.py - Interface Graphique pour le Système d'Authentification d'Ordonnances
==============================================================================

Interface graphique Tkinter pour le système de signature post-quantique Mirath.
Style médical professionnel avec fenêtres séparées pour chaque rôle.

Lancement: python gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import sys
from datetime import datetime

# Import des modules du système
try:
    from mirath import MirathSignature
    from ordonnance import Ordonnance, creer_medicament
    from medecin import Medecin, initialiser_medecin
    from pharmacie import Pharmacie
except ImportError as e:
    print(f"❌ ERREUR: {e}")
    print("Assurez-vous que tous les modules sont dans le même dossier!")
    sys.exit(1)


# ============================================================================
# CONFIGURATION DES COULEURS ET STYLES
# ============================================================================

class StyleConfig:
    """Configuration des couleurs et styles de l'interface"""
    
    # Palette médicale professionnelle
    BLEU_PRINCIPAL = "#2C5F8D"      # Bleu médical
    BLEU_CLAIR = "#4A90C6"          # Bleu plus clair
    BLANC = "#FFFFFF"
    GRIS_CLAIR = "#F5F5F5"
    GRIS_MOYEN = "#CCCCCC"
    GRIS_FONCE = "#666666"
    
    # Couleurs de statut
    VERT_VALIDE = "#28A745"         # Vert pour validations
    ROUGE_ERREUR = "#DC3545"        # Rouge pour erreurs
    ORANGE_ATTENTION = "#FFA500"    # Orange pour avertissements
    
    # Polices
    POLICE_TITRE = ("Arial", 16, "bold")
    POLICE_SOUS_TITRE = ("Arial", 12, "bold")
    POLICE_NORMALE = ("Arial", 10)
    POLICE_PETIT = ("Arial", 9)


# ============================================================================
# FENÊTRE PRINCIPALE - MENU DE SÉLECTION
# ============================================================================

class MenuPrincipal:
    """Fenêtre de sélection du rôle (Médecin, Pharmacien, Gestion)"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Système d'Authentification d'Ordonnances - Mirath")
        self.root.geometry("600x500")
        self.root.configure(bg=StyleConfig.BLANC)
        
        # Centrer la fenêtre
        self.centrer_fenetre(600, 500)
        
        self.creer_interface()
    
    def centrer_fenetre(self, largeur, hauteur):
        """Centre la fenêtre sur l'écran"""
        x = (self.root.winfo_screenwidth() // 2) - (largeur // 2)
        y = (self.root.winfo_screenheight() // 2) - (hauteur // 2)
        self.root.geometry(f"{largeur}x{hauteur}+{x}+{y}")
    
    def creer_interface(self):
        """Crée l'interface du menu principal"""
        
        # En-tête avec titre
        frame_header = tk.Frame(self.root, bg=StyleConfig.BLEU_PRINCIPAL, height=120)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        tk.Label(
            frame_header,
            text="🏥 SYSTÈME D'AUTHENTIFICATION",
            font=StyleConfig.POLICE_TITRE,
            bg=StyleConfig.BLEU_PRINCIPAL,
            fg=StyleConfig.BLANC
        ).pack(pady=15)
        
        tk.Label(
            frame_header,
            text="Signature Numérique Post-Quantique - Schéma Mirath",
            font=StyleConfig.POLICE_NORMALE,
            bg=StyleConfig.BLEU_PRINCIPAL,
            fg=StyleConfig.BLANC
        ).pack()
        
        # Corps avec les boutons
        frame_corps = tk.Frame(self.root, bg=StyleConfig.BLANC)
        frame_corps.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        tk.Label(
            frame_corps,
            text="Sélectionnez votre rôle :",
            font=StyleConfig.POLICE_SOUS_TITRE,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.BLEU_PRINCIPAL
        ).pack(pady=(0, 30))
        
        # Bouton Médecin
        self.creer_bouton_role(
            frame_corps,
            "⚕️  MÉDECIN",
            "Créer et signer des ordonnances",
            self.ouvrir_interface_medecin
        )
        
        # Bouton Pharmacien
        self.creer_bouton_role(
            frame_corps,
            "💊 PHARMACIEN",
            "Vérifier l'authenticité d'ordonnances",
            self.ouvrir_interface_pharmacien
        )
        
        # Bouton Gestion
        self.creer_bouton_role(
            frame_corps,
            "⚙️  GESTION",
            "Gérer les médecins du système",
            self.ouvrir_interface_gestion
        )
        
        # Bouton Quitter
        tk.Button(
            frame_corps,
            text="Quitter",
            command=self.root.quit,
            bg=StyleConfig.GRIS_MOYEN,
            fg=StyleConfig.BLANC,
            font=StyleConfig.POLICE_NORMALE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=5
        ).pack(pady=(20, 0))
    
    def creer_bouton_role(self, parent, titre, description, commande):
        """Crée un bouton de sélection de rôle"""
        frame = tk.Frame(parent, bg=StyleConfig.GRIS_CLAIR, relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.X, pady=10)
        
        btn = tk.Button(
            frame,
            text=titre,
            command=commande,
            bg=StyleConfig.BLEU_PRINCIPAL,
            fg=StyleConfig.BLANC,
            font=StyleConfig.POLICE_SOUS_TITRE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=15
        )
        btn.pack(fill=tk.X)
        
        tk.Label(
            frame,
            text=description,
            font=StyleConfig.POLICE_PETIT,
            bg=StyleConfig.GRIS_CLAIR,
            fg=StyleConfig.GRIS_FONCE
        ).pack(pady=(5, 10))
    
    def ouvrir_interface_medecin(self):
        """Ouvre l'interface médecin"""
        InterfaceMedecin(self.root)
    
    def ouvrir_interface_pharmacien(self):
        """Ouvre l'interface pharmacien"""
        InterfacePharmacien(self.root)
    
    def ouvrir_interface_gestion(self):
        """Ouvre l'interface de gestion"""
        InterfaceGestion(self.root)


# ============================================================================
# INTERFACE MÉDECIN
# ============================================================================

class InterfaceMedecin:
    """Interface pour les médecins"""
    
    def __init__(self, parent):
        self.fenetre = tk.Toplevel(parent)
        self.fenetre.title("Interface Médecin")
        self.fenetre.geometry("800x700")
        self.fenetre.configure(bg=StyleConfig.BLANC)
        
        self.medicaments_liste = []  # Liste des médicaments à prescrire
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface médecin"""
        
        # En-tête
        frame_header = tk.Frame(self.fenetre, bg=StyleConfig.BLEU_PRINCIPAL, height=80)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        tk.Label(
            frame_header,
            text="⚕️  INTERFACE MÉDECIN",
            font=StyleConfig.POLICE_TITRE,
            bg=StyleConfig.BLEU_PRINCIPAL,
            fg=StyleConfig.BLANC
        ).pack(pady=25)
        
        # Zone avec scrollbar pour le contenu
        canvas = tk.Canvas(self.fenetre, bg=StyleConfig.BLANC)
        scrollbar = ttk.Scrollbar(self.fenetre, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=StyleConfig.BLANC)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Contenu dans frame_scroll
        frame_contenu = tk.Frame(frame_scroll, bg=StyleConfig.BLANC)
        frame_contenu.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)
        
        # Section 1: Identification du médecin
        self.creer_section_medecin(frame_contenu)
        
        # Section 2: Informations du patient
        self.creer_section_patient(frame_contenu)
        
        # Section 3: Médicaments
        self.creer_section_medicaments(frame_contenu)
        
        # Section 4: Actions
        self.creer_section_actions(frame_contenu)
    
    def creer_section_medecin(self, parent):
        """Section d'identification du médecin"""
        frame = tk.LabelFrame(
            parent,
            text="📋 Identification du Médecin",
            font=StyleConfig.POLICE_SOUS_TITRE,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.BLEU_PRINCIPAL
        )
        frame.pack(fill=tk.X, pady=(0, 20))
        
        # Sélection du médecin
        tk.Label(
            frame,
            text="ID Médecin :",
            font=StyleConfig.POLICE_NORMALE,
            bg=StyleConfig.BLANC
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        
        self.combo_medecin = ttk.Combobox(
            frame,
            values=self.obtenir_liste_medecins(),
            state="readonly",
            width=30
        )
        self.combo_medecin.grid(row=0, column=1, padx=10, pady=10)
        
        if self.combo_medecin['values']:
            self.combo_medecin.current(0)
        
        # Clé secrète (seed_sk en hexadécimal)
        tk.Label(
            frame,
            text="Clé Secrète :",
            font=StyleConfig.POLICE_NORMALE,
            bg=StyleConfig.BLANC
        ).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        
        self.entry_cle_secrete = tk.Entry(frame, width=50, show="*")
        self.entry_cle_secrete.grid(row=1, column=1, padx=10, pady=10)
        
        # Bouton pour afficher/masquer la clé
        self.btn_afficher_cle = tk.Button(
            frame,
            text="👁️",
            command=self.toggle_affichage_cle,
            bg=StyleConfig.GRIS_CLAIR,
            relief=tk.FLAT,
            cursor="hand2",
            width=3
        )
        self.btn_afficher_cle.grid(row=1, column=2, padx=5)
        
        # Note explicative
        tk.Label(
            frame,
            text="⚠️ Copiez le 'seed_sk' depuis votre fichier *_secret.json",
            font=StyleConfig.POLICE_PETIT,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.ORANGE_ATTENTION
        ).grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=(0, 10))
    
    def toggle_affichage_cle(self):
        """Bascule entre affichage et masquage de la clé"""
        if self.entry_cle_secrete.cget('show') == '*':
            self.entry_cle_secrete.config(show='')
            self.btn_afficher_cle.config(text='🔒')
        else:
            self.entry_cle_secrete.config(show='*')
            self.btn_afficher_cle.config(text='👁️')
    
    def creer_section_patient(self, parent):
        """Section des informations du patient"""
        frame = tk.LabelFrame(
            parent,
            text="👤 Informations du Patient",
            font=StyleConfig.POLICE_SOUS_TITRE,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.BLEU_PRINCIPAL
        )
        frame.pack(fill=tk.X, pady=(0, 20))
        
        # Nom
        tk.Label(frame, text="Nom :", bg=StyleConfig.BLANC).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=5
        )
        self.entry_patient_nom = tk.Entry(frame, width=30)
        self.entry_patient_nom.grid(row=0, column=1, padx=10, pady=5)
        
        # Prénom
        tk.Label(frame, text="Prénom :", bg=StyleConfig.BLANC).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=5
        )
        self.entry_patient_prenom = tk.Entry(frame, width=30)
        self.entry_patient_prenom.grid(row=1, column=1, padx=10, pady=5)
        
        # ID
        tk.Label(frame, text="ID Patient :", bg=StyleConfig.BLANC).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=5
        )
        self.entry_patient_id = tk.Entry(frame, width=30)
        self.entry_patient_id.grid(row=2, column=1, padx=10, pady=5)
    
    def creer_section_medicaments(self, parent):
        """Section de prescription des médicaments"""
        frame = tk.LabelFrame(
            parent,
            text="💊 Médicaments à Prescrire",
            font=StyleConfig.POLICE_SOUS_TITRE,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.BLEU_PRINCIPAL
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Formulaire d'ajout
        frame_ajout = tk.Frame(frame, bg=StyleConfig.BLANC)
        frame_ajout.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_ajout, text="Nom :", bg=StyleConfig.BLANC).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.entry_med_nom = tk.Entry(frame_ajout, width=25)
        self.entry_med_nom.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_ajout, text="Dosage :", bg=StyleConfig.BLANC).grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5
        )
        self.entry_med_dosage = tk.Entry(frame_ajout, width=15)
        self.entry_med_dosage.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_ajout, text="Posologie :", bg=StyleConfig.BLANC).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.entry_med_posologie = tk.Entry(frame_ajout, width=50)
        self.entry_med_posologie.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        
        tk.Button(
            frame_ajout,
            text="➕ Ajouter",
            command=self.ajouter_medicament,
            bg=StyleConfig.VERT_VALIDE,
            fg=StyleConfig.BLANC,
            relief=tk.FLAT,
            cursor="hand2"
        ).grid(row=2, column=3, pady=10)
        
        # Liste des médicaments ajoutés
        self.text_medicaments = scrolledtext.ScrolledText(
            frame,
            height=8,
            width=70,
            font=StyleConfig.POLICE_NORMALE
        )
        self.text_medicaments.pack(padx=10, pady=(0, 10))
    
    def creer_section_actions(self, parent):
        """Section des boutons d'action"""
        frame = tk.Frame(parent, bg=StyleConfig.BLANC)
        frame.pack(fill=tk.X, pady=20)
        
        tk.Button(
            frame,
            text="✍️  Créer et Signer l'Ordonnance",
            command=self.creer_et_signer_ordonnance,
            bg=StyleConfig.BLEU_PRINCIPAL,
            fg=StyleConfig.BLANC,
            font=StyleConfig.POLICE_SOUS_TITRE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=15
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        tk.Button(
            frame,
            text="Fermer",
            command=self.fenetre.destroy,
            bg=StyleConfig.GRIS_MOYEN,
            fg=StyleConfig.BLANC,
            font=StyleConfig.POLICE_NORMALE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
    
    def obtenir_liste_medecins(self):
        """Obtient la liste des médecins enregistrés"""
        dossier = "cles_medecins"
        if not os.path.exists(dossier):
            return []
        
        medecins = []
        for fichier in os.listdir(dossier):
            if fichier.endswith("_public.json"):
                medecins.append(fichier.replace("_public.json", ""))
        
        return sorted(medecins)
    
    def ajouter_medicament(self):
        """Ajoute un médicament à la liste"""
        nom = self.entry_med_nom.get().strip()
        dosage = self.entry_med_dosage.get().strip()
        posologie = self.entry_med_posologie.get().strip()
        
        if not nom or not dosage or not posologie:
            messagebox.showwarning("Attention", "Tous les champs doivent être remplis!")
            return
        
        medicament = creer_medicament(nom, dosage, posologie)
        self.medicaments_liste.append(medicament)
        
        # Affichage dans la zone de texte
        self.text_medicaments.insert(
            tk.END,
            f"{len(self.medicaments_liste)}. {nom} - {dosage}\n   Posologie: {posologie}\n\n"
        )
        
        # Réinitialisation des champs
        self.entry_med_nom.delete(0, tk.END)
        self.entry_med_dosage.delete(0, tk.END)
        self.entry_med_posologie.delete(0, tk.END)
    
    def creer_et_signer_ordonnance(self):
        """Crée et signe une ordonnance"""
        try:
            # Validation
            id_medecin = self.combo_medecin.get()
            if not id_medecin:
                messagebox.showerror("Erreur", "Veuillez sélectionner un médecin!")
                return
            
            patient_nom = self.entry_patient_nom.get().strip()
            patient_prenom = self.entry_patient_prenom.get().strip()
            patient_id = self.entry_patient_id.get().strip()
            
            if not patient_nom or not patient_prenom or not patient_id:
                messagebox.showerror("Erreur", "Tous les champs du patient doivent être remplis!")
                return
            
            if len(self.medicaments_liste) == 0:
                messagebox.showerror("Erreur", "Au moins un médicament doit être prescrit!")
                return
            
            # Chargement du médecin
            medecin = Medecin("", "", id_medecin)
            if not medecin.charger_cles():
                messagebox.showerror("Erreur", f"Impossible de charger les clés du médecin {id_medecin}")
                return
            
            # Création de l'ordonnance
            ordonnance = Ordonnance(
                patient_nom=patient_nom,
                patient_prenom=patient_prenom,
                patient_id=patient_id,
                medecin_nom="",  # Sera récupéré du système
                medecin_prenom="Dr.",
                medecin_id=id_medecin,
                medicaments=self.medicaments_liste
            )
            
            # Signature
            if medecin.signer_ordonnance(ordonnance):
                # Sauvegarde
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nom_fichier = f"ordonnance_{patient_id}_{timestamp}.json"
                ordonnance.sauvegarder(nom_fichier)
                
                messagebox.showinfo(
                    "✅ Succès",
                    f"Ordonnance créée et signée avec succès!\n\nFichier: {nom_fichier}",
                    icon='info'
                )
                
                # Réinitialisation
                self.medicaments_liste = []
                self.text_medicaments.delete(1.0, tk.END)
                self.entry_patient_nom.delete(0, tk.END)
                self.entry_patient_prenom.delete(0, tk.END)
                self.entry_patient_id.delete(0, tk.END)
            else:
                messagebox.showerror("Erreur", "Échec de la signature de l'ordonnance")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création: {str(e)}")


# ============================================================================
# INTERFACE PHARMACIEN
# ============================================================================

class InterfacePharmacien:
    """Interface pour les pharmaciens"""
    
    def __init__(self, parent):
        self.fenetre = tk.Toplevel(parent)
        self.fenetre.title("Interface Pharmacien")
        self.fenetre.geometry("800x600")
        self.fenetre.configure(bg=StyleConfig.BLANC)
        
        self.pharmacie = Pharmacie("Pharmacie Centrale")
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface pharmacien"""
        
        # En-tête
        frame_header = tk.Frame(self.fenetre, bg=StyleConfig.BLEU_CLAIR, height=80)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        tk.Label(
            frame_header,
            text="💊 INTERFACE PHARMACIEN",
            font=StyleConfig.POLICE_TITRE,
            bg=StyleConfig.BLEU_CLAIR,
            fg=StyleConfig.BLANC
        ).pack(pady=25)
        
        # Corps
        frame_corps = tk.Frame(self.fenetre, bg=StyleConfig.BLANC)
        frame_corps.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        # Section 1: Nom de la pharmacie
        frame_nom = tk.Frame(frame_corps, bg=StyleConfig.BLANC)
        frame_nom.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            frame_nom,
            text="Nom de la pharmacie :",
            font=StyleConfig.POLICE_NORMALE,
            bg=StyleConfig.BLANC
        ).pack(side=tk.LEFT)
        
        self.entry_nom_pharmacie = tk.Entry(frame_nom, width=40)
        self.entry_nom_pharmacie.insert(0, "Pharmacie Centrale")
        self.entry_nom_pharmacie.pack(side=tk.LEFT, padx=10)
        
        # Section 2: Sélection de l'ordonnance
        frame_selection = tk.LabelFrame(
            frame_corps,
            text="📄 Sélection de l'Ordonnance",
            font=StyleConfig.POLICE_SOUS_TITRE,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.BLEU_PRINCIPAL
        )
        frame_selection.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            frame_selection,
            text="Ordonnance à vérifier :",
            bg=StyleConfig.BLANC
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        
        self.combo_ordonnance = ttk.Combobox(
            frame_selection,
            values=self.obtenir_liste_ordonnances(),
            state="readonly",
            width=50
        )
        self.combo_ordonnance.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(
            frame_selection,
            text="🔄 Actualiser",
            command=self.actualiser_liste_ordonnances,
            bg=StyleConfig.GRIS_MOYEN,
            fg=StyleConfig.BLANC,
            relief=tk.FLAT,
            cursor="hand2"
        ).grid(row=0, column=2, padx=10)
        
        # Section 3: Résultat de la vérification
        frame_resultat = tk.LabelFrame(
            frame_corps,
            text="📊 Résultat de la Vérification",
            font=StyleConfig.POLICE_SOUS_TITRE,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.BLEU_PRINCIPAL
        )
        frame_resultat.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.text_resultat = scrolledtext.ScrolledText(
            frame_resultat,
            height=15,
            width=80,
            font=StyleConfig.POLICE_NORMALE,
            wrap=tk.WORD
        )
        self.text_resultat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Section 4: Actions
        frame_actions = tk.Frame(frame_corps, bg=StyleConfig.BLANC)
        frame_actions.pack(fill=tk.X)
        
        tk.Button(
            frame_actions,
            text="🔍 Vérifier l'Ordonnance",
            command=self.verifier_ordonnance,
            bg=StyleConfig.BLEU_PRINCIPAL,
            fg=StyleConfig.BLANC,
            font=StyleConfig.POLICE_SOUS_TITRE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=15
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        tk.Button(
            frame_actions,
            text="Fermer",
            command=self.fenetre.destroy,
            bg=StyleConfig.GRIS_MOYEN,
            fg=StyleConfig.BLANC,
            font=StyleConfig.POLICE_NORMALE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
    
    def obtenir_liste_ordonnances(self):
        """Obtient la liste des ordonnances disponibles"""
        ordonnances = []
        for fichier in os.listdir("."):
            if fichier.startswith("ordonnance_") and fichier.endswith(".json"):
                ordonnances.append(fichier)
        
        return sorted(ordonnances, reverse=True)
    
    def actualiser_liste_ordonnances(self):
        """Actualise la liste des ordonnances"""
        self.combo_ordonnance['values'] = self.obtenir_liste_ordonnances()
    
    def verifier_ordonnance(self):
        """Vérifie une ordonnance sélectionnée"""
        try:
            # Récupération du nom de la pharmacie
            nom_pharmacie = self.entry_nom_pharmacie.get().strip()
            if nom_pharmacie:
                self.pharmacie = Pharmacie(nom_pharmacie)
            
            # Récupération du fichier
            fichier = self.combo_ordonnance.get()
            if not fichier:
                messagebox.showwarning("Attention", "Veuillez sélectionner une ordonnance!")
                return
            
            # Chargement de l'ordonnance
            ordonnance = Ordonnance.charger(fichier)
            
            # Chargement de la clé publique du médecin
            if not self.pharmacie.charger_cle_publique_medecin(ordonnance.medecin_id):
                self.afficher_erreur(f"Clé publique du médecin {ordonnance.medecin_id} introuvable!")
                return
            
            # Vérification
            resultat = self.pharmacie.verifier_ordonnance(ordonnance)
            
            # Affichage du résultat
            self.afficher_resultat(ordonnance, resultat)
            
        except FileNotFoundError:
            self.afficher_erreur(f"Fichier introuvable: {fichier}")
        except Exception as e:
            self.afficher_erreur(f"Erreur: {str(e)}")
    
    def afficher_resultat(self, ordonnance, resultat):
        """Affiche le résultat de la vérification"""
        self.text_resultat.delete(1.0, tk.END)
        
        # En-tête avec statut
        if resultat['valide']:
            self.text_resultat.insert(tk.END, "="*70 + "\n")
            self.text_resultat.insert(tk.END, "✅ ORDONNANCE VALIDE ET AUTHENTIQUE\n", "valide")
            self.text_resultat.insert(tk.END, "="*70 + "\n\n")
        else:
            self.text_resultat.insert(tk.END, "="*70 + "\n")
            self.text_resultat.insert(tk.END, "❌ ORDONNANCE INVALIDE OU SUSPECTE\n", "invalide")
            self.text_resultat.insert(tk.END, "="*70 + "\n\n")
        
        # Raison
        self.text_resultat.insert(tk.END, f"Raison: {resultat['raison']}\n\n")
        
        # Détails de l'ordonnance
        self.text_resultat.insert(tk.END, "📋 DÉTAILS DE L'ORDONNANCE:\n\n")
        self.text_resultat.insert(tk.END, f"Date: {ordonnance.date_prescription}\n\n")
        
        self.text_resultat.insert(tk.END, f"Patient: {ordonnance.patient_prenom} {ordonnance.patient_nom}\n")
        self.text_resultat.insert(tk.END, f"ID Patient: {ordonnance.patient_id}\n\n")
        
        self.text_resultat.insert(tk.END, f"Médecin: Dr. {ordonnance.medecin_prenom} {ordonnance.medecin_nom}\n")
        self.text_resultat.insert(tk.END, f"ID Médecin: {ordonnance.medecin_id}\n\n")
        
        self.text_resultat.insert(tk.END, "💊 MÉDICAMENTS PRESCRITS:\n\n")
        for i, med in enumerate(ordonnance.medicaments, 1):
            self.text_resultat.insert(tk.END, f"  {i}. {med['nom']} - {med['dosage']}\n")
            self.text_resultat.insert(tk.END, f"     Posologie: {med['posologie']}\n\n")
        
        # Recommandations
        self.text_resultat.insert(tk.END, "\n" + "="*70 + "\n")
        self.text_resultat.insert(tk.END, "💡 RECOMMANDATIONS:\n\n")
        
        if resultat['valide']:
            self.text_resultat.insert(
                tk.END,
                "• Vous pouvez délivrer les médicaments prescrits\n"
                "• Vérifiez l'identité du patient\n"
                "• Archivez cette ordonnance\n",
                "valide"
            )
        else:
            self.text_resultat.insert(
                tk.END,
                "• NE PAS DÉLIVRER les médicaments\n"
                "• Contactez le médecin prescripteur\n"
                "• Signalez toute tentative de fraude\n",
                "invalide"
            )
        
        # Configuration des tags pour les couleurs
        self.text_resultat.tag_config("valide", foreground=StyleConfig.VERT_VALIDE, font=("Arial", 10, "bold"))
        self.text_resultat.tag_config("invalide", foreground=StyleConfig.ROUGE_ERREUR, font=("Arial", 10, "bold"))
    
    def afficher_erreur(self, message):
        """Affiche un message d'erreur"""
        self.text_resultat.delete(1.0, tk.END)
        self.text_resultat.insert(tk.END, "❌ ERREUR\n\n", "invalide")
        self.text_resultat.insert(tk.END, message)
        self.text_resultat.tag_config("invalide", foreground=StyleConfig.ROUGE_ERREUR, font=("Arial", 12, "bold"))


# ============================================================================
# INTERFACE GESTION
# ============================================================================

class InterfaceGestion:
    """Interface de gestion du système"""
    
    def __init__(self, parent):
        self.fenetre = tk.Toplevel(parent)
        self.fenetre.title("Interface Gestion")
        self.fenetre.geometry("700x500")
        self.fenetre.configure(bg=StyleConfig.BLANC)
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface de gestion"""
        
        # En-tête
        frame_header = tk.Frame(self.fenetre, bg=StyleConfig.GRIS_FONCE, height=80)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        tk.Label(
            frame_header,
            text="⚙️  GESTION DU SYSTÈME",
            font=StyleConfig.POLICE_TITRE,
            bg=StyleConfig.GRIS_FONCE,
            fg=StyleConfig.BLANC
        ).pack(pady=25)
        
        # Corps
        frame_corps = tk.Frame(self.fenetre, bg=StyleConfig.BLANC)
        frame_corps.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        # Section 1: Initialiser un nouveau médecin
        frame_init = tk.LabelFrame(
            frame_corps,
            text="➕ Initialiser un Nouveau Médecin",
            font=StyleConfig.POLICE_SOUS_TITRE,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.BLEU_PRINCIPAL
        )
        frame_init.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(frame_init, text="Nom :", bg=StyleConfig.BLANC).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=5
        )
        self.entry_med_nom = tk.Entry(frame_init, width=30)
        self.entry_med_nom.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(frame_init, text="Prénom :", bg=StyleConfig.BLANC).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=5
        )
        self.entry_med_prenom = tk.Entry(frame_init, width=30)
        self.entry_med_prenom.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(frame_init, text="ID Médecin :", bg=StyleConfig.BLANC).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=5
        )
        self.entry_med_id = tk.Entry(frame_init, width=30)
        self.entry_med_id.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Button(
            frame_init,
            text="✅ Initialiser",
            command=self.initialiser_medecin,
            bg=StyleConfig.VERT_VALIDE,
            fg=StyleConfig.BLANC,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).grid(row=3, column=1, pady=10, sticky=tk.E)
        
        # Section 2: Liste des médecins
        frame_liste = tk.LabelFrame(
            frame_corps,
            text="📋 Médecins Enregistrés",
            font=StyleConfig.POLICE_SOUS_TITRE,
            bg=StyleConfig.BLANC,
            fg=StyleConfig.BLEU_PRINCIPAL
        )
        frame_liste.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.text_medecins = scrolledtext.ScrolledText(
            frame_liste,
            height=10,
            width=60,
            font=StyleConfig.POLICE_NORMALE
        )
        self.text_medecins.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Button(
            frame_liste,
            text="🔄 Actualiser la Liste",
            command=self.afficher_liste_medecins,
            bg=StyleConfig.BLEU_PRINCIPAL,
            fg=StyleConfig.BLANC,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(pady=(0, 10))
        
        # Section 3: Bouton Fermer
        tk.Button(
            frame_corps,
            text="Fermer",
            command=self.fenetre.destroy,
            bg=StyleConfig.GRIS_MOYEN,
            fg=StyleConfig.BLANC,
            font=StyleConfig.POLICE_NORMALE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack()
        
        # Affichage initial de la liste
        self.afficher_liste_medecins()
    
    def initialiser_medecin(self):
        """Initialise un nouveau médecin"""
        try:
            nom = self.entry_med_nom.get().strip()
            prenom = self.entry_med_prenom.get().strip()
            id_medecin = self.entry_med_id.get().strip()
            
            if not nom or not prenom or not id_medecin:
                messagebox.showwarning("Attention", "Tous les champs doivent être remplis!")
                return
            
            # Initialisation
            medecin = initialiser_medecin(nom, prenom, id_medecin)
            
            messagebox.showinfo(
                "✅ Succès",
                f"Médecin {id_medecin} initialisé avec succès!\n\n"
                f"Dr. {prenom} {nom}\n"
                f"Les clés ont été générées et sauvegardées."
            )
            
            # Réinitialisation des champs
            self.entry_med_nom.delete(0, tk.END)
            self.entry_med_prenom.delete(0, tk.END)
            self.entry_med_id.delete(0, tk.END)
            
            # Actualisation de la liste
            self.afficher_liste_medecins()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'initialisation:\n{str(e)}")
    
    def afficher_liste_medecins(self):
        """Affiche la liste des médecins enregistrés"""
        self.text_medecins.delete(1.0, tk.END)
        
        dossier = "cles_medecins"
        
        if not os.path.exists(dossier):
            self.text_medecins.insert(tk.END, "⚠️  Aucun médecin enregistré\n\n")
            self.text_medecins.insert(tk.END, f"Le dossier {dossier} n'existe pas encore.")
            return
        
        medecins = set()
        for fichier in os.listdir(dossier):
            if fichier.endswith("_public.json"):
                medecins.add(fichier.replace("_public.json", ""))
        
        if len(medecins) == 0:
            self.text_medecins.insert(tk.END, "⚠️  Aucun médecin enregistré dans le système")
        else:
            self.text_medecins.insert(tk.END, f"✓ {len(medecins)} médecin(s) enregistré(s):\n\n")
            for i, id_med in enumerate(sorted(medecins), 1):
                self.text_medecins.insert(tk.END, f"  {i}. {id_med}\n")


# ============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================================

def main():
    """Lance l'application graphique"""
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()


if __name__ == "__main__":
    main()
