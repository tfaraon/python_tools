import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QProgressBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import Xbeach_reader as XBr
import numpy as np
import os
import csv

def save_matrix_to_csv(matrix, filename):
    """ Sauvegarde une matrice numpy dans un fichier CSV. """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(matrix)

class XBeachGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("XBeach Data Viewer")
        self.setGeometry(100, 100, 700, 1000)

        layout = QVBoxLayout()

        # Bouton pour sélectionner le dossier principal
        self.load_button = QPushButton("Select XB SuperFolder")
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)

        # Création de la figure matplotlib et de la zone de dessin
        self.fig, self.ax = plt.subplots(figsize=(6, 9))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Champs pour entrer le nombre d'entités géomorphologiques
        self.num_entities_label = QLabel("Number of geomorphologic entities:")
        layout.addWidget(self.num_entities_label)
        self.num_entities_entry = QLineEdit()
        layout.addWidget(self.num_entities_entry)

        # Champs pour entrer le chemin de sauvegarde
        self.savepath_label = QLabel("Save Path:")
        layout.addWidget(self.savepath_label)
        self.savepath_entry = QLineEdit()
        layout.addWidget(self.savepath_entry)

        # Bouton pour charger les entités
        self.load_entities_button = QPushButton("Load Entities")
        self.load_entities_button.clicked.connect(self.load_entities)
        layout.addWidget(self.load_entities_button)

        # Bouton pour sauvegarder les données
        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_initial_data)
        layout.addWidget(self.save_button)

        # Label pour afficher les coordonnées
        self.coord_label = QLabel("Coordinates:")
        layout.addWidget(self.coord_label)

        # Initialisation des variables
        self.start_bed = None
        self.sim_name = None
        self.superfolder = None

        self.current_entity = 0
        self.entity_data = []
        self.entity_names = []
        self.corners = []

        self.setLayout(layout)
        
    def load_data(self):
        # Sélection du superdossier contenant les simulations
        self.superfolder = QFileDialog.getExistingDirectory(self, "Select Superfolder")
        if not self.superfolder:
            QMessageBox.critical(self, "Error", "No folder selected.")
            return

        subfolders = [f.path for f in os.scandir(self.superfolder) if f.is_dir()]
        data_loaded = False

        # Parcours des sous-dossiers pour charger les données
        for subfolder in subfolders:
            self.sim_name = os.path.basename(subfolder)
            xb_output = os.path.join(subfolder, 'xboutput.nc')
            if os.path.exists(xb_output):
                xb_data = XBr.XB_Loader(xb_output)
                self.start_bed = xb_data.zb[0, :, :].data
                xb_data.close()
                data_loaded = True
                break  # Charger seulement le premier jeu de données disponible

        if data_loaded:
            print(f"Data loaded for {self.sim_name}. Start bed shape: {self.start_bed.shape}")
            self.ax.clear()
            self.ax.imshow(self.start_bed, cmap='viridis')
            self.ax.set_title(f'Start Bed for {self.sim_name}')
            self.ax.invert_yaxis()
            self.canvas.draw_idle()
        else:
            QMessageBox.critical(self, "Error", "No xboutput.nc file found in any subfolder.")

    def on_click(self, event):
        # Gestion des clics sur la figure matplotlib
        if event.inaxes == self.ax:
            x, y = int(event.xdata), int(event.ydata)
            self.coord_label.setText(f"Coordinates: ({x}, {y})")

    def save_initial_data(self):
        # Sauvegarde des données initiales
        num_entities = self.num_entities_entry.text()
        savepath = self.savepath_entry.text()

        if not num_entities.isdigit():
            QMessageBox.critical(self, "Input Error", "Number of Entities must be an integer.")
            return

        if not os.path.exists(savepath):
            os.makedirs(savepath)

        num_entities = int(num_entities)
        self.num_entities = num_entities
        self.savepath = savepath

        # Sauvegarde du lit initial et du nombre d'entités
        np.save(os.path.join(savepath, f'start_bed_{self.sim_name}.npy'), self.start_bed)
        with open(os.path.join(savepath, f'num_entities_{self.sim_name}.txt'), 'w') as f:
            f.write(str(num_entities))

        self.open_entity_window()        

    def open_entity_window(self):
        # Ouverture de la fenêtre pour entrer les données des entités
        self.entity_window = QWidget()
        self.entity_window.setWindowTitle("Entity Data Entry")
        self.entity_window.setGeometry(100, 100, 700, 800)  # Largeur augmentée pour accommoder les deux colonnes

        main_layout = QVBoxLayout()
        
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 9))
        self.canvas2 = FigureCanvas(self.fig2)
        main_layout.addWidget(self.canvas2)
        self.canvas2.mpl_connect("button_press_event", self.on_click_entity_window)

        self.ax2.imshow(self.start_bed, cmap='viridis')
        self.ax2.set_title(f'Start Bed for {self.sim_name}')
        self.ax2.invert_yaxis()
        self.canvas2.draw_idle()

        self.coord_label2 = QLabel("Coordinates:")
        main_layout.addWidget(self.coord_label2)

        # Champs pour entrer le nom des entités
        self.entity_name_label = QLabel("Entity Name:")
        main_layout.addWidget(self.entity_name_label)
        self.entity_name_entry = QLineEdit()
        main_layout.addWidget(self.entity_name_entry)

        # Ajout du bouton "Add Point"
        self.add_point_button = QPushButton("Add Point")
        self.add_point_button.clicked.connect(self.add_point)
        main_layout.addWidget(self.add_point_button)

        # Ajout du bouton "Finish Polygon"
        self.finish_polygon_button = QPushButton("Finish Polygon")
        self.finish_polygon_button.clicked.connect(self.finish_polygon)
        main_layout.addWidget(self.finish_polygon_button)

        # Ajout du bouton "Next Entity"
        self.next_entity_button = QPushButton("Next Entity")
        self.next_entity_button.clicked.connect(self.process_entity)
        main_layout.addWidget(self.next_entity_button)

        # Ajout du bouton "Finish"
        self.finish_button = QPushButton("Finish")
        self.finish_button.clicked.connect(self.finish_entities)
        main_layout.addWidget(self.finish_button)

        self.entity_window.setLayout(main_layout)
        self.entity_window.show()

    def on_click_entity_window(self, event):
        # Gestion des clics sur la figure matplotlib dans la fenêtre des entités
        if event.inaxes == self.ax2:
            x, y = int(event.xdata), int(event.ydata)
            self.coord_label2.setText(f"Coordinates: ({x}, {y})")

            self.corners.append((x, y))
            self.ax2.plot(x, y, 'x', color='red', markersize=10)
            self.canvas2.draw_idle()

    def add_point(self):
        # Ajouter un point au polygone en cours
        if len(self.corners) == 0:
            QMessageBox.critical(self, "Input Error", "Click on the image to add points.")
            return

    def finish_polygon(self):
        # Terminer la définition du polygone actuel
        if len(self.corners) < 3:
            QMessageBox.critical(self, "Input Error", "A polygon must have at least 3 points.")
            return

        entity_name = self.entity_name_entry.text()
        if not entity_name:
            QMessageBox.critical(self, "Input Error", "Entity name must be provided.")
            return

        self.entity_names.append(entity_name)
        self.entity_data.append(self.corners)
        self.corners = []

        self.entity_name_entry.clear()
        self.ax2.clear()
        self.ax2.imshow(self.start_bed, cmap='viridis')
        self.ax2.set_title(f'Start Bed for {self.sim_name}')
        self.ax2.invert_yaxis()
        self.canvas2.draw_idle()

    def process_entity(self):
        # Traitement de l'entité courante et préparation de la suivante
        self.finish_polygon()
        self.current_entity += 1
        if self.current_entity >= self.num_entities:
            self.finish_entities()

    def finish_entities(self):
        # Finir la définition de toutes les entités
        self.entity_window.close()

    def load_entities(self):
        # Charger les entités à partir d'un fichier
        filepath, _ = QFileDialog.getOpenFileName(self, "Load Entities", "", "Text Files (*.txt);;All Files (*)")
        if not filepath:
            return

        # Mise à jour du chemin de sauvegarde avec le dossier contenant le fichier chargé
        self.savepath = os.path.dirname(filepath)
        self.savepath_entry.setText(self.savepath)

        with open(filepath, 'r') as f:
            lines = f.readlines()

        entities = []
        for line in lines:
            name, corners_str = line.strip().split(':')
            corners = eval(corners_str)
            entities.append({
                "name": name,
                "corners": corners
            })

        self.entity_entries = []
        self.num_entities = len(entities)

        self.open_entity_window()

        for i, entity in enumerate(entities):
            entity_name_entry, corners_entries = self.entity_entries[i]
            entity_name_entry.setText(entity['name'])
            for j, (x, y) in enumerate(entity['corners']):
                corners_entries[j][1].setText(str(x))
                corners_entries[j][2].setText(str(y))
                corners_entries[j][0].setText(f"Corner {j+1} (x, y): ({x}, {y})")

    def calculate_differences(self):
        if not self.superfolder:
            QMessageBox.critical(self, "Error", "Superfolder path is not set.")
            return

        subfolders = [f.path for f in os.scandir(self.superfolder) if f.is_dir()]
        progress_window = QWidget()
        progress_window.setWindowTitle("Calculating Differences")
        progress_window.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()
        progress_label = QLabel("Calculating differences, please wait...")
        layout.addWidget(progress_label)
        progress_bar = QProgressBar()
        progress_bar.setMaximum(len(subfolders))
        layout.addWidget(progress_bar)
        self.subfolder_name_label = QLabel("Current subfolder: ")
        layout.addWidget(self.subfolder_name_label)
        progress_window.setLayout(layout)
        progress_window.show()

        results = []

        for i, subfolder in enumerate(subfolders):
            if not progress_window.isVisible():
                return

            progress_bar.setValue(i)
            self.subfolder_name_label.setText(f"Current subfolder: {os.path.basename(subfolder)}")
            progress_window.repaint()

            xb_output = os.path.join(subfolder, 'xboutput.nc')
            if os.path.exists(xb_output):
                xb_data = XBr.XB_Loader(xb_output)
                zb = xb_data.zb[-1, :, :].data
                xb_data.close()

                subfolder_results = []

                for entity in zip(self.entity_names, self.entity_data):
                    name = entity[0]
                    corners = entity[1]

                    # Extraction des coordonnées des coins
                    x_coords = [corner[0] for corner in corners]
                    y_coords = [corner[1] for corner in corners]

                    min_x, max_x = min(x_coords), max(x_coords)
                    min_y, max_y = min(y_coords), max(y_coords)

                    # Extraction des sections pour les coins définis
                    section_start_bed = self.start_bed[min_y:max_y, min_x:max_x]
                    section_zb = zb[min_y:max_y, min_x:max_x]
                    
                    volume_start_bed = np.sum(section_start_bed)
                    volume_zb = np.sum(section_zb)
                    volume_difference = volume_zb - volume_start_bed

                    subfolder_results.append((name, volume_start_bed, volume_zb, volume_difference))

                results.append((os.path.basename(subfolder), subfolder_results))

        progress_window.close()

        self.save_results(results)

    def save_results(self, results):
        savepath = self.savepath_entry.text()
        if not savepath:
            QMessageBox.critical(self, "Error", "Save path is not set.")
            return

        for subfolder, subfolder_results in results:
            filename = os.path.join(savepath, f'differences_{subfolder}.csv')
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Entity", "Start Bed Volume", "End Bed Volume", "Volume Difference"])
                for result in subfolder_results:
                    writer.writerow(result)

        QMessageBox.information(self, "Success", "Data successfully saved.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = XBeachGUI()
    main_window.show()
    sys.exit(app.exec_())
