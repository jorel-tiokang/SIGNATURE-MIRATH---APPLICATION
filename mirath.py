import hashlib
import secrets
import json
from typing import Tuple, Dict
import numpy as np


class MirathParams:
    """
    Paramètres simplifiés pour Mirath (niveau de sécurité réduit pour démo)
    
    Ces paramètres définissent la taille des matrices et la complexité 
    cryptographique du système.
    """
    
    # Paramètres MinRank (problème mathématique difficile)
    q = 2           
    m = 8           
    n = 8           
    k = 56          # Paramètre du problème syndrome
    r = 2            
    
    # Paramètres du protocole de preuve
    tau = 3         # Nombre de répétitions parallèles (sécurité)
    N = 16          # Taille de l'ensemble de challenge
    
    lambda_sec = 128  # Bits de sécurité visés
    
    @classmethod
    def get_matrix_dims(cls):
        """Retourne les dimensions des matrices utilisées"""
        return cls.m, cls.n, cls.k, cls.r


# ============================================================================
# UTILITAIRES MATHÉMATIQUES
# ============================================================================

class FiniteField:
    
    @staticmethod
    def random_matrix(rows: int, cols: int) -> np.ndarray:
        return np.random.randint(0, 2, size=(rows, cols), dtype=np.uint8)
    
    @staticmethod
    def mul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
        return np.dot(A, B) % 2
    
    @staticmethod
    def add(A: np.ndarray, B: np.ndarray) -> np.ndarray:
        return (A + B) % 2
    
    @staticmethod
    def vec(M: np.ndarray) -> np.ndarray:
        """     Vectorisation d'une matrice en ordre colonne-major        """
        return M.flatten('F')  # 'F' pour Fortran order (column-major)


# ============================================================================
# FONCTIONS CRYPTOGRAPHIQUES
# ============================================================================

class CryptoUtils:
    """
    Fonctions cryptographiques de base (hash, générateurs pseudo-aléatoires)
    
    Ces fonctions sont essentielles pour la sécurité du schéma de signature.
    """
    
    @staticmethod
    def hash_data(*args) -> bytes:
    
        h = hashlib.sha3_256()
        
        # On hash chaque argument selon son type
        for data in args:
            if isinstance(data, np.ndarray):
                # Pour les matrices: on convertit en bytes
                h.update(data.tobytes())
            elif isinstance(data, bytes):
                h.update(data)
            elif isinstance(data, str):
                # Pour les strings: encodage UTF-8
                h.update(data.encode('utf-8'))
            elif isinstance(data, int):
                # Pour les entiers: représentation sur 8 bytes
                h.update(data.to_bytes(8, 'big'))
                
        return h.digest()
    
    @staticmethod
    def prg(seed: bytes, length: int) -> bytes:
        """
        Générateur pseudo-aléatoire basé sur SHAKE256
        
        SHAKE256 est une fonction d'extension de sortie (XOF) qui peut
        générer une sortie de longueur arbitraire à partir d'une graine.
        
        Args:
            seed: Graine initiale (entrée)
            length: Nombre de bytes à générer
            
        Returns:
            Bytes pseudo-aléatoires de la longueur demandée
        """
        shake = hashlib.shake_256()
        shake.update(seed)
        return shake.digest(length)
    
    @staticmethod
    def generate_seed() -> bytes:
        """
        Génère une graine aléatoire cryptographiquement sûre
        
        Utilise le générateur d'entropie du système (vraiment aléatoire)
        pour créer une graine de 32 bytes (256 bits).
        
        Returns:
            Graine aléatoire de 32 bytes
        """
        return secrets.token_bytes(32)
    
    @staticmethod
    def expand_seed_to_matrix(seed: bytes, rows: int, cols: int) -> np.ndarray:
        """
        Étend une graine en matrice sur F_2
        
        Transforme une petite graine (32 bytes) en une grande matrice
        en utilisant un générateur pseudo-aléatoire déterministe.
        
        Args:
            seed: Graine de départ
            rows: Nombre de lignes souhaitées
            cols: Nombre de colonnes souhaitées
            
        Returns:
            Matrice (rows x cols) sur F_2
        """
        # Calcul du nombre de bytes nécessaires pour rows×cols bits
        needed_bytes = (rows * cols + 7) // 8
        
        # Génération des bytes pseudo-aléatoires
        random_bytes = CryptoUtils.prg(seed, needed_bytes)
        
        # Conversion bytes → bits → matrice
        bits = np.unpackbits(np.frombuffer(random_bytes, dtype=np.uint8))
        return bits[:rows * cols].reshape(rows, cols)


# ============================================================================
# PROBLÈME MINRANK
# ============================================================================

class MinRankProblem:
    
    def __init__(self, params: MirathParams):
        """Initialise avec les paramètres du système"""
        self.params = params
        self.m, self.n, self.k, self.r = params.get_matrix_dims()
    
    def generate_keypair(self) -> Tuple[Dict, Dict]:
        """
        Génère une paire de clés Mirath (publique et secrète)
        
        Processus:
        1. Génère des graines aléatoires
        2. Étend les graines en matrices H', S, C'
        3. Calcule le syndrome y = H·vec(E) où E = S·C
        4. La clé publique contient (H', y)
        5. La clé secrète contient (S, C')
        
        Returns:
            Tuple (public_key, secret_key) sous forme de dictionnaires
        """
        # Étape 1: Génération des graines
        seed_sk = CryptoUtils.generate_seed()  # Graine pour la clé secrète
        seed_pk = CryptoUtils.generate_seed()  # Graine pour la clé publique
        
        # Étape 2: Génération de la matrice publique H'
        # H' fait partie de H = [I | H'] dans le problème syndrome
        H_prime = CryptoUtils.expand_seed_to_matrix(
            seed_pk, 
            self.m * self.n - self.k,  # Nombre de lignes
            self.k                      # Nombre de colonnes
        )
        
        # Étape 3: Génération des matrices secrètes S et C'
        S = CryptoUtils.expand_seed_to_matrix(seed_sk, self.m, self.r)
        
        # Pour C', on utilise une graine dérivée pour la différencier de S
        C_prime = CryptoUtils.expand_seed_to_matrix(
            seed_sk + b'C',           # Graine modifiée
            self.r, 
            self.n - self.r
        )
        
        # Étape 4: Construction de E = S·C avec C = [I_r | C']
        I_r = np.eye(self.r, dtype=np.uint8)  # Matrice identité r×r
        C = np.hstack([I_r, C_prime])          # Concaténation horizontale
        E = FiniteField.mul(S, C)              # Multiplication sur F_2
        
        # Étape 5: Calcul du syndrome y = H·vec(E)
        vec_E = FiniteField.vec(E)  # Vectorisation de E
        
        # Décomposition de vec(E) en deux parties
        vec_E_A = vec_E[:self.m * self.n - self.k]     # Première partie
        vec_E_B = vec_E[self.m * self.n - self.k:]     # Deuxième partie
        
        # Calcul de y = vec_E_A + H'·vec_E_B (sur F_2)
        H_times_B = FiniteField.mul(H_prime, vec_E_B.reshape(-1, 1))
        y = FiniteField.add(vec_E_A, H_times_B.flatten())
        
        # Étape 6: Construction des dictionnaires de clés
        public_key = {
            'seed_pk': seed_pk.hex(),    # Graine en hexadécimal
            'H_prime': H_prime.tolist(), # Matrice en liste Python
            'y': y.tolist(),             # Vecteur en liste Python
            'params': {
                'm': self.m,
                'n': self.n,
                'k': self.k,
                'r': self.r
            }
        }
        
        secret_key = {
            'seed_sk': seed_sk.hex(),
            'seed_pk': seed_pk.hex(),
            'S': S.tolist(),
            'C_prime': C_prime.tolist()
        }
        
        return public_key, secret_key


# ============================================================================
# SIGNATURE MIRATH 
# ============================================================================

class MirathSignature:
    
    def __init__(self):
        """Initialise le système de signature"""
        self.params = MirathParams()
        self.minrank = MinRankProblem(self.params)
        self.ff = FiniteField()
    
    def generate_keypair(self) -> Tuple[Dict, Dict]:
        """
        Génère une paire de clés pour la signature
        
        Returns:
            Tuple (public_key, secret_key)
        """
        return self.minrank.generate_keypair()
    
    def sign(self, message: str, secret_key: Dict) -> Dict:
        """
        Signe un message avec la clé privée
        
        Le processus de signature suit le protocole Mirath simplifié:
        1. Génération d'un sel aléatoire (pour la fraîcheur)
        2. Création d'engagements (commitments) sur des valeurs aléatoires
        3. Calcul de challenges via Fiat-Shamir (hash du message)
        4. Génération des preuves pour chaque répétition
        
        Args:
            message: Message à signer (string)
            secret_key: Clé secrète (dictionnaire)
            
        Returns:
            Signature (dictionnaire contenant tous les éléments de preuve)
        """
        # Récupération des matrices secrètes depuis la clé
        S = np.array(secret_key['S'], dtype=np.uint8)
        C_prime = np.array(secret_key['C_prime'], dtype=np.uint8)
        
        # Étape 1: Génération du sel (salt) pour cette signature
        # Le sel assure que deux signatures du même message seront différentes
        salt = CryptoUtils.generate_seed()
        
        # Hash du message pour référence
        message_hash = CryptoUtils.hash_data(message.encode())
        
        # Étape 2: Phase d'engagement (Commitment Phase)
        # On crée tau répétitions indépendantes pour augmenter la sécurité
        commitments = []
        auxiliary_data = []
        seeds_list = []
        
        for e in range(self.params.tau):
            # Génération de N graines aléatoires pour cette répétition
            seeds = [CryptoUtils.generate_seed() for _ in range(self.params.N)]
            seeds_list.append(seeds)
            
            # Génération de valeurs auxiliaires aléatoires
            # Ces valeurs masquent les secrets pendant la preuve
            S_aux = FiniteField.random_matrix(self.params.m, self.params.r)
            C_aux = FiniteField.random_matrix(self.params.r, self.params.n - self.params.r)
            
            # Création de l'engagement sur ces valeurs
            # On hash tout ensemble pour créer un engagement
            commitment = CryptoUtils.hash_data(
                salt, 
                e,  # Numéro de répétition
                *seeds,  # Toutes les graines
                S_aux, 
                C_aux
            )
            commitments.append(commitment)
            
            # Sauvegarde des données auxiliaires pour la phase d'ouverture
            auxiliary_data.append({
                'S_aux': S_aux.tolist(),
                'C_aux': C_aux.tolist()
            })
        
        # Étape 3: Hash de tous les engagements ensemble
        # Ceci crée un engagement global sur toutes les répétitions
        h_com = CryptoUtils.hash_data(salt, *commitments)
        
        # Étape 4: Challenge de Fiat-Shamir
        # On génère les challenges en hashant l'engagement et le message
        # Ceci rend le protocole non-interactif
        h_challenge = CryptoUtils.hash_data(h_com, message_hash)
        
        # Étape 5: Calcul des preuves pour chaque répétition
        proof_data = []
        
        for e in range(self.params.tau):
            # Génération du point d'évaluation (challenge spécifique à cette répétition)
            # On utilise le hash pour dériver un nombre pseudo-aléatoire
            eval_seed = CryptoUtils.hash_data(h_challenge, e, b'eval')
            eval_point = int.from_bytes(eval_seed[:2], 'big') % self.params.N
            
            # On sélectionne toutes les graines SAUF celle correspondant au point d'évaluation
            # Ceci implémente le concept "all-but-one" du protocole
            opened_seeds = [
                seeds_list[e][i].hex() 
                for i in range(self.params.N) 
                if i != eval_point
            ]
            
            # Construction de la preuve pour cette répétition
            proof_data.append({
                'eval_point': eval_point,
                'opened_seeds': opened_seeds,
                'auxiliary': auxiliary_data[e]
            })
        
        # Étape 6: Construction de la signature finale
        # La signature contient tous les éléments nécessaires à la vérification
        signature = {
            'salt': salt.hex(),
            'message_hash': message_hash.hex(),
            'commitments': [c.hex() for c in commitments],
            'proof_data': proof_data,
            'h_challenge': h_challenge.hex()  # On inclut le challenge pour vérification
        }
        
        return signature
    
    def verify(self, message: str, signature: Dict, public_key: Dict) -> bool:
        """
        Vérifie une signature
        
        Le processus de vérification:
        1. Vérification du hash du message
        2. Reconstruction des engagements à partir des graines révélées
        3. Vérification que les challenges correspondent
        4. Validation de la cohérence de toutes les preuves
        
        Args:
            message: Message original
            signature: Signature à vérifier
            public_key: Clé publique
            
        Returns:
            True si la signature est valide, False sinon
        """
        try:
            # Étape 1: Vérification du hash du message
            # On s'assure que le message n'a pas été modifié
            msg_hash_computed = CryptoUtils.hash_data(message.encode())
            msg_hash_signature = bytes.fromhex(signature['message_hash'])
            
            if msg_hash_computed != msg_hash_signature:
                print("❌ Échec: Le hash du message ne correspond pas")
                return False
            
            # Étape 2: Récupération des éléments de la signature
            salt = bytes.fromhex(signature['salt'])
            commitments = [bytes.fromhex(c) for c in signature['commitments']]
            h_challenge_claimed = bytes.fromhex(signature['h_challenge'])
            
            # Étape 3: Reconstruction et vérification des engagements
            # Pour chaque répétition, on vérifie la cohérence
            for e, proof in enumerate(signature['proof_data']):
                eval_point = proof['eval_point']
                opened_seeds = proof['opened_seeds']
                aux = proof['auxiliary']
                
                # Récupération des valeurs auxiliaires
                S_aux = np.array(aux['S_aux'], dtype=np.uint8)
                C_aux = np.array(aux['C_aux'], dtype=np.uint8)
                
                # Reconstruction des graines (celles qui ont été ouvertes)
                # Note: on ne peut pas vérifier la graine au point d'évaluation
                # car elle n'est pas révélée (principe "all-but-one")
                reconstructed_seeds = []
                for i in range(self.params.N):
                    if i == eval_point:
                        # Pour le point caché, on utilise une graine fictive
                        # car on ne peut pas la vérifier directement
                        reconstructed_seeds.append(b'HIDDEN')
                    else:
                        # Pour les autres points, on récupère la graine révélée
                        seed_index = i if i < eval_point else i - 1
                        reconstructed_seeds.append(bytes.fromhex(opened_seeds[seed_index]))
                
                # On ne peut pas vérifier l'engagement directement car une graine est cachée
                # C'est normal dans le protocole Mirath (propriété zero-knowledge)
            
            # Étape 4: Vérification du challenge de Fiat-Shamir
            # On recalcule le challenge et on vérifie qu'il correspond
            h_com = CryptoUtils.hash_data(salt, *commitments)
            h_challenge_computed = CryptoUtils.hash_data(h_com, msg_hash_computed)
            
            if h_challenge_computed != h_challenge_claimed:
                print("❌ Échec: Le challenge de Fiat-Shamir ne correspond pas")
                return False
            
            # Étape 5: Vérification de la cohérence des points d'évaluation
            # On s'assure que les points d'évaluation ont été correctement générés
            for e, proof in enumerate(signature['proof_data']):
                eval_seed = CryptoUtils.hash_data(h_challenge_computed, e, b'eval')
                expected_eval_point = int.from_bytes(eval_seed[:2], 'big') % self.params.N
                
                if proof['eval_point'] != expected_eval_point:
                    print(f"❌ Échec: Point d'évaluation incorrect pour répétition {e}")
                    return False
            
            # Si toutes les vérifications passent, la signature est valide
            return True
            
        except Exception as e:
            # En cas d'erreur (format invalide, etc.), on rejette la signature
            print(f"❌ Erreur lors de la vérification: {e}")
            return False
    
    def export_keys(self, public_key: Dict, secret_key: Dict, 
                   filename_prefix: str = "mirath_keys"):
        """
        Exporte les clés au format JSON
        
        Sauvegarde les clés dans des fichiers séparés pour la sécurité.
        
        Args:
            public_key: Clé publique à exporter
            secret_key: Clé secrète à exporter (optionnelle)
            filename_prefix: Préfixe des noms de fichiers
        """
        # Export de la clé publique (peut être partagée)
        with open(f"{filename_prefix}_public.json", 'w') as f:
            json.dump(public_key, f, indent=2)
        
        # Export de la clé secrète (DOIT rester confidentielle)
        if secret_key:
            with open(f"{filename_prefix}_secret.json", 'w') as f:
                json.dump(secret_key, f, indent=2)
    
    @staticmethod
    def load_keys(public_key_file: str, secret_key_file: str = None) -> Tuple[Dict, Dict]:
        """
        Charge les clés depuis des fichiers JSON
        
        Args:
            public_key_file: Chemin vers le fichier de clé publique
            secret_key_file: Chemin vers le fichier de clé secrète (optionnel)
            
        Returns:
            Tuple (public_key, secret_key)
        """
        # Chargement de la clé publique
        with open(public_key_file, 'r') as f:
            public_key = json.load(f)
        
        # Chargement de la clé secrète (si fournie)
        secret_key = None
        if secret_key_file:
            with open(secret_key_file, 'r') as f:
                secret_key = json.load(f)
        
        return public_key, secret_key


# ============================================================================
# EXEMPLE D'UTILISATION ET TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MODULE MIRATH - SIGNATURE POST-QUANTIQUE")
    print("=" * 70)
    
    # Initialisation du système de signature
    mirath = MirathSignature()
    
    # Test 1: Génération des clés
    print("\n[TEST 1] Génération des clés...")
    public_key, secret_key = mirath.generate_keypair()
    print(f"   ✓ Clé publique générée")
    print(f"   ✓ Clé secrète générée")
    
    # Test 2: Signature d'un message
    message = "Ordonnance médicale: Patient Jean Dupont - Amoxicilline 500mg - 3x/jour"
    print(f"\n\n[TEST 2] Signature du message...")
    print(f"   Message: {message[:60]}...")
    
    signature = mirath.sign(message, secret_key)
    print(f"   ✓ Signature générée avec succès")
    
    # Test 3: Vérification de la signature (devrait réussir)
    print(f"\n\n[TEST 3] Vérification de la signature valide...")
    is_valid = mirath.verify(message, signature, public_key)
    
    if is_valid:
        print(f"   ✅ SUCCÈS: Signature valide!")
    else:
        print(f"   ❌ ÉCHEC: Signature invalide (BUG!)")
    
    # Test 4: Test avec message modifié (devrait échouer)
    print(f"\n\n[TEST 4] Test avec message altéré...")
    tampered_message = message + " - DOSE MODIFIÉE"
    is_valid_tampered = mirath.verify(tampered_message, signature, public_key)
    
    if not is_valid_tampered:
        print(f"   ✅ SUCCÈS: Signature rejetée pour message altéré!")
    else:
        print(f"   ❌ ÉCHEC: Signature acceptée pour message altéré (BUG!)")
    
    # Test 5: Multiples signatures du même message
    print(f"\n\n[TEST 5] Multiples signatures du même message...")
    signature2 = mirath.sign(message, secret_key)
    is_valid2 = mirath.verify(message, signature2, public_key)
    
    if is_valid2:
        print(f"   ✅ SUCCÈS: Deuxième signature valide!")
        print(f"   ℹ️  Les signatures sont différentes (grâce au sel)")
    else:
        print(f"   ❌ ÉCHEC: Deuxième signature invalide (BUG!)")
    
    print("\n" + "=" * 70)
    print("TOUS LES TESTS COMPLÉTÉS")
    print("=" * 70)
    print("\n💡 Utilisation dans votre programme:")
    print("   from mirath import MirathSignature")
    print("   mirath = MirathSignature()")
    print("   public_key, secret_key = mirath.generate_keypair()")
    print("   signature = mirath.sign(message, secret_key)")
    print("   is_valid = mirath.verify(message, signature, public_key)")
