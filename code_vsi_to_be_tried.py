import processing
import os

# CONFIGURATION
nom_couche_polygones = 'votre_couche_valais' # Remplacez par le nom réel
dossier_sortie = "C:/Projet_EPFL/Cuts_10cm/"
os.makedirs(dossier_sortie, exist_ok=True)

layer = QgsProject.instance().mapLayersByName(nom_couche_polygones)[0]

# Exemple d'URL directe d'une dalle (à automatiser via STAC ou une liste)
# Ici on simule pour la première entité sélectionnée
for feature in layer.selectedFeatures():
    geom = feature.geometry()
    bbox = geom.boundingBox()
    ext = f"{bbox.xMinimum()},{bbox.xMaximum()},{bbox.yMinimum()},{bbox.yMaximum()} [EPSG:2056]"
    
    # URL du Cloud Optimized GeoTIFF de SwissTopo
    # Note: L'URL doit être celle du fichier .tif direct
    url_distante = "/vsicurl/https://data.geo.admin.ch/ch.swisstopo.swissimage-dop10/swissimage-dop10_2023_2600-1120_0.1_2056.tif"

    output_file = os.path.join(dossier_sortie, f"parcelle_{feature.id()}.tif")

    # On découpe SANS télécharger tout le fichier
    processing.run("gdal:cliprasterbyextent", {
        'INPUT': url_distante,
        'PROJWIN': ext,
        'NODATA': 0,
        'OPTIONS': 'COMPRESS=LZW',
        'OUTPUT': output_file
    })
    print(f"Découpe distante terminée pour la parcelle {feature.id()}")