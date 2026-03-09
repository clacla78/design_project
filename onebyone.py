import os
import processing
from qgis.core import QgsProject

# --- CONFIGURATION ---
csv_path = r"C:\Users\clari\Documents\MA3\Design Project\ch.swisstopo.swissimage-dop10-Z0kQrs2O.csv"
output_dir = r"C:\Users\clari\Documents\MA3\Design Project\Crops_Test"
os.makedirs(output_dir, exist_ok=True)

# On prend la couche principale
layer = QgsProject.instance().mapLayersByName("SCA_PRAIRIES_SURF_EXPL_Q2_19-02-2026 — SAP_SURF_EX___Prairie")[0]

def trouver_url_pour_poly(geom_poly, csv_file):
    bbox = geom_poly.boundingBox()
    # Coordonnées théoriques de la dalle SwissTopo (ex: 2600, 1120)
    x_tile = int(bbox.xMinimum() / 1000)
    y_tile = int(bbox.yMinimum() / 1000)
    cible = f"{x_tile}-{y_tile}"
    
    with open(csv_file, 'r') as f:
        for line in f:
            if cible in line and "http" in line:
                return line.strip().replace('"', '').split(',')[0] # Ajustez si l'URL n'est pas en 1ère colonne
    return None

# --- EXECUTION SUR UNE SEULE ENTITÉ ---
# On récupère juste la première entité de la couche pour tester
feature = next(layer.getFeatures()) 
geom = feature.geometry()
id_pratique = feature.id()

url_distante = trouver_url_pour_poly(geom, csv_path)

if url_distante:
    print(f"URL trouvée pour la parcelle {id_pratique} : {url_distante}")
    
    bbox = geom.boundingBox()
    # On ajoute une petite marge de 10m autour du polygone
    buffer = 10
    ext_str = f"{bbox.xMinimum()-buffer},{bbox.xMaximum()+buffer},{bbox.yMinimum()-buffer},{bbox.yMaximum()+buffer} [EPSG:2056]"
    
    output_path = os.path.join(output_dir, f"crop_parcelle_{id_pratique}.tif")
    
    # COMMANDE GDAL - Utilise vsicurl pour ne lire que les pixels nécessaires
    print("Extraction en cours (patience, lecture réseau)...")
    try:
        processing.run("gdal:cliprasterbyextent", {
            'INPUT': f"/vsicurl/{url_distante}",
            'PROJWIN': ext_str,
            'NODATA': 0,
            'OPTIONS': 'COMPRESS=LZW',
            'OUTPUT': output_path
        })
        print(f"SUCCÈS ! Fichier créé : {output_path}")
    except Exception as e:
        print(f"ERREUR : {e}")
else:
    print("Aucune dalle correspondante trouvée dans le CSV pour ce polygone.")