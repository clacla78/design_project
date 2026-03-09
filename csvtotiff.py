import os
import requests
from qgis.core import QgsProject, QgsRectangle

# --- CONFIGURATION ---
csv_path = r"C:\Users\clari\Documents\MA3\Design Project\ch.swisstopo.swissimage-dop10-Z0kQrs2O.csv"
output_dir = r"C:\Users\clari\Documents\MA3\Design Project"
nom_couche = "SCA_PRAIRIES_SURF_EXPL_Q2_19-02-2026 — SAP_SURF_EX___Prairie"

os.makedirs(output_dir, exist_ok=True)

layer = QgsProject.instance().mapLayersByName(nom_couche)[0]
emprise_totale = layer.extent()

def extraire_bbox_du_lien(url):
    try:
        # Nettoyage pour ne garder que le nom du fichier
        filename = url.split('/')[-1]
        parts = filename.split('_')
        # On cherche le bloc "XXXX-YYYY"
        coord_part = [p for p in parts if "-" in p and p.split("-")[0].isdigit()][0]
        coords = coord_part.split('-')
        x_min = int(coords[0]) * 1000
        y_min = int(coords[1]) * 1000
        return QgsRectangle(x_min, y_min, x_min + 1000, y_min + 1000)
    except:
        return None

# --- EXECUTION ---
print(f"Début de l'analyse...")
compteur_trouve = 0
compteur_telecharge = 0

with open(csv_path, 'r', encoding='utf-8') as f:
    for i, ligne in enumerate(f):
        # On saute l'en-tête si c'est la première ligne et qu'elle contient du texte
        if i == 0 and "http" not in ligne:
            continue
            
        # On cherche l'URL dans la ligne (gestion des CSV avec virgules)
        colonnes = ligne.replace('"', '').split(',')
        url = ""
        for c in colonnes:
            if "http" in c and ".tif" in c:
                url = c.strip()
                break
        
        if not url:
            continue

        bbox_dalle = extraire_bbox_du_lien(url)
        
        if bbox_dalle and bbox_dalle.intersects(emprise_totale):
            compteur_trouve += 1
            nom_fichier = os.path.basename(url)
            chemin_final = os.path.join(output_dir, nom_fichier)
            
            if not os.path.exists(chemin_final):
                print(f" Trouvé ({compteur_trouve}) : {nom_fichier}")
                try:
                    r = requests.get(url, stream=True, timeout=15)
                    r.raise_for_status()
                    with open(chemin_final, 'wb') as out_f:
                        for chunk in r.iter_content(chunk_size=8192):
                            out_f.write(chunk)
                    compteur_telecharge += 1
                except Exception as e:
                    print(f"Erreur sur {nom_fichier}: {e}")
            else:
                # Si déjà là, on compte quand même comme "trouvé"
                pass

print(f"\n--- BILAN ---")
print(f"Dalles correspondant à vos polygones : {compteur_trouve}")
print(f"Nouvelles dalles téléchargées : {compteur_telecharge}")