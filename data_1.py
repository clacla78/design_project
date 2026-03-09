import subprocess
import sys
import os

# Commande pour forcer la mise à jour de Pydantic dans l'environnement QGIS
print("Tentative de réparation des bibliothèques Python...")

try:
    # On utilise l'exécutable Python interne de QGIS pour installer les bonnes versions
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pydantic", "pydantic-core"])
    
    print("-" * 50)
    print("RÉPARATION RÉUSSIE !")
    print("Veuillez REDÉMARRER QGIS maintenant pour appliquer les changements.")
    print("-" * 50)
except Exception as e:
    print(f"ÉCHEC de la réparation. Erreur : {e}")
    print("Essayez de lancer QGIS en mode Administrateur pour autoriser la modification.")