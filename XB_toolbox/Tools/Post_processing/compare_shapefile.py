import geopandas as gpd
import os

os.chdir('/home/tfrn/Documents/Stage_TDV/XBeach/Calibration/Calibration morpho/GIS/')

# Charger le fichier de référence
reference_file = 'Morpho_overwash.shp'
reference_data = gpd.read_file(reference_file)

# Calculer l'aire du polygone de référence
area_reference = reference_data.unary_union.area

# Fonction pour calculer l'aire du polygone comparé
def calculate_area(file_path):
    file_data = gpd.read_file(file_path)
    return file_data.unary_union.area

# Fonction pour calculer le recouvrement entre deux polygones
def calculate_overlap(poly1, poly2):
    intersection = poly1.intersection(poly2)
    return intersection.area

# Fonction pour calculer le goodness of fit
def calculate_gof(area_reference, area_compared, overlap):
    return (overlap / (area_compared)) * (overlap / (area_reference))

# Charger les autres fichiers et calculer les goodness of fit
other_files = [#'Facua/Test_17_1.shp',
#                'Facua/Test_17_2.shp',
#                'Facua/Test_17_3.shp',
#                'Facua/Test_17_4.shp',
#                'Facua/Test_17_5.shp',
#                'Facua/Test_17_6.shp',
               #'Test_18/Test_18.shp',
               'Wall/Tideloc.shp']

for file in other_files:
    area_compared = calculate_area(file)
    overlaps = []
    for _, row in reference_data.iterrows():
        area_overlap = calculate_overlap(row.geometry, gpd.read_file(file).unary_union)
        overlaps.append(area_overlap)
    total_overlap = sum(overlaps)
    gof = calculate_gof(area_reference, area_compared, total_overlap)
    print("Goodness of fit pour", file, ":", gof)