import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout,
    QMessageBox, QSlider
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class MapEnhanceGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROS2 PGM Map Enhancer")
        self.resize(1100, 650)

        self.orig = None          # Original PGM
        self.proc = None          # Aktuell bearbeitet (Graustufe)
        self.last_filtered = None # Was gespeichert werden soll

        # Labels für Original und Ergebnis
        self.label_orig = QLabel("Original")
        self.label_proc = QLabel("Verbessert / Filter")
        self.label_orig.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_proc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.btn_load = QPushButton("PGM laden")
        self.btn_hist = QPushButton("Histogramm-Equalisierung")
        self.btn_erode = QPushButton("Erosion (Hindernisse dünner)")
        self.btn_dilate = QPushButton("Dilatation (Hindernisse dicker)")
        self.btn_holes = QPushButton(" Grau => WeißS ")
        self.btn_canny = QPushButton("Canny-Kanten")
        self.btn_canny_repair = QPushButton("Hindernisse mit Canny ergänzen")
        self.btn_remove_islands = QPushButton("Hindernis-Inseln entfernen")
        self.btn_reset = QPushButton("Reset")
        self.btn_save = QPushButton("Karte speichern (aktuell)")

        # Slider für Erosion/Dilatation-Iterationen
        self.slider_erode = QSlider(Qt.Orientation.Horizontal)
        self.slider_erode.setRange(1, 3)
        self.slider_erode.setValue(1)
        self.slider_erode.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_erode.setTickInterval(1)

        self.slider_dilate = QSlider(Qt.Orientation.Horizontal)
        self.slider_dilate.setRange(1, 3)
        self.slider_dilate.setValue(1)
        self.slider_dilate.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_dilate.setTickInterval(1)

        # Layout für Bilder
        h_layout_images = QHBoxLayout()
        h_layout_images.addWidget(self.label_orig)
        h_layout_images.addWidget(self.label_proc)

        h_layout_slider = QHBoxLayout()
        h_layout_slider.addWidget(QLabel("Erosion Iterationen (Hindernisse dünner)"))
        h_layout_slider.addWidget(self.slider_erode)
        h_layout_slider.addWidget(self.btn_erode)

        h_layout_slider2 = QHBoxLayout()
        h_layout_slider2.addWidget(QLabel("Dilatation Iterationen (Hindernisse dicker)"))
        h_layout_slider2.addWidget(self.slider_dilate)
        h_layout_slider2.addWidget(self.btn_dilate)
        
        # Hauptlayout
        v_layout_main = QVBoxLayout()
        v_layout_main.addLayout(h_layout_images)
        v_layout_main.addWidget(self.btn_load)
        v_layout_main.addLayout(h_layout_slider)
        v_layout_main.addLayout(h_layout_slider2)
        v_layout_main.addWidget(self.btn_hist)
        v_layout_main.addWidget(self.btn_holes) 
        v_layout_main.addWidget(self.btn_canny)
        v_layout_main.addWidget(self.btn_canny_repair)
        v_layout_main.addWidget(self.btn_remove_islands)
        v_layout_main.addWidget(self.btn_reset)
        v_layout_main.addWidget(self.btn_save)
        self.setLayout(v_layout_main)

        # Verbindungen
        self.btn_load.clicked.connect(self.loadImage)
        self.btn_hist.clicked.connect(self.applyHistogram)
        self.btn_erode.clicked.connect(self.applyErode)
        self.btn_dilate.clicked.connect(self.applyDilate)
        self.btn_canny.clicked.connect(self.applyCanny)
        self.btn_reset.clicked.connect(self.resetImage)
        self.btn_save.clicked.connect(self.saveMap)
        self.btn_holes.clicked.connect(self.gray_2_white)
        self.btn_canny_repair.clicked.connect(self.reinforce_obstacles_with_canny)
        self.btn_remove_islands.clicked.connect(self.remove_small_obstacle_islands)

    def loadImage(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "PGM laden", "", "PGM Files (*.pgm)"
        )
        if not file:
            return

        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
        if img is None:
            QMessageBox.critical(self, "Fehler", f"Karte konnte nicht geladen werden:\n{file}")
            return

        if len(img.shape) != 2 or img.dtype != np.uint8:
            QMessageBox.warning(self, "Hinweis",
                                "Map ist nicht im erwarteten 8-Bit-Graustufenformat (PGM).")

        self.orig = img.copy()
        self.proc = img.copy()
        self.last_filtered = self.proc.copy()

        self.slider_erode.setValue(1)
        self.slider_dilate.setValue(1)

        self.updateLabel(self.label_orig, self.orig)
        self.updateLabel(self.label_proc, self.proc)

    def applyHistogram(self):
        if self.proc is None:
            return
        self.proc = cv2.equalizeHist(self.proc)
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyErode(self):
        if self.proc is None:
            return
        iterations = self.slider_erode.value()

        # schwächerer Kernel: Kreuz statt vollem 3x3-Quadrat
        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)

        # weiß erodieren: eroded = cv2.erode(self.proc, kernel, iterations=iterations)        
        # Hindernisse schwarz -> invertieren, auf Weiß erodieren
        inv = 255 - self.proc
        eroded_inv = cv2.erode(inv, kernel, iterations=iterations)
        eroded = 255 - eroded_inv  # dann zurück invertieren

        self.proc = eroded
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyDilate(self):
        if self.proc is None:
            return
        iterations = self.slider_dilate.value()
        kernel = np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]], dtype=np.uint8)

         # Hindernisse schwarz -> invertieren, auf Weiß dilatieren
        inv = 255 - self.proc
        dilated_inv = cv2.dilate(inv, kernel, iterations=iterations)
        dilated = 255 - dilated_inv

        self.proc = dilated
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyCanny(self):
        if self.proc is None:
            return
        low = 50  # Untere Schwellwertgrenze für den Canny-Algorithmus. 
        # Gradienten unterhalb dieses Werts werden als „kein Edge“ verworfen.
        
        high = 150  # Obere Schwellwertgrenze. 
        # Gradienten oberhalb werden als „sichere Kanten“ akzeptiert.
        # Werte zwischen den Schwellwerten gelten als „unsichere Kanten“
        # und werden nur übernommen, wenn mit sicheren Kanten verbunden
        # (Hysterese-Prinzip von Canny).​

        edges = cv2.Canny(self.proc, low, high)
        # Führt die Canny-Kantendetektion auf dem aktuellen Graustufenbild self.proc aus.
        # Ergebnis edges ist ein Binärbild:
        # 255 = erkannte Kante
        # 0 = kein Kante-Pixel
        self.last_filtered = edges  # Speichere Ergebnis
        self.updateLabel(self.label_proc, edges)

    def resetImage(self):
        if self.orig is None:
            return
        self.proc = self.orig.copy()
        self.last_filtered = self.proc.copy()
        self.slider_erode.setValue(1)
        self.slider_dilate.setValue(1)
        self.updateLabel(self.label_proc, self.proc)

    def updateLabel(self, label, img):
        if len(img.shape) == 2:
            h, w = img.shape
            bytes_per_line = w
            qimg = QImage(
                img.data, w, h, bytes_per_line,
                QImage.Format.Format_Grayscale8
            )
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img_rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(
                img_rgb.data, w, h, bytes_per_line,
                QImage.Format.Format_RGB888
            )

        pix = QPixmap.fromImage(qimg).scaled(
            label.width() if label.width() > 0 else 500,
            label.height() if label.height() > 0 else 500,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(pix)

    def saveMap(self):
        if self.last_filtered is None:
            QMessageBox.warning(self, "Warnung", "Keine Karte zum Speichern vorhanden.")
            return

        file, _ = QFileDialog.getSaveFileName(
            self, "Karte speichern", "map_enhanced.pgm", "PGM Files (*.pgm)"
        )
        if not file:
            return

        if not file.lower().endswith(".pgm"):
            file += ".pgm"

        success = cv2.imwrite(file, self.last_filtered)
        if success:
            QMessageBox.information(self, "Erfolg",
                                    f"Karte erfolgreich gespeichert:\n{file}")
        else:
            QMessageBox.critical(self, "Fehler",
                                 f"Speichern fehlgeschlagen:\n{file}")
            
    def gray_2_white(self, checked=False, gray_min=200, gray_max=210):
        """Die Funktion gray_2_white ersetzt gezielt alle Pixel im Graubereich 
           zwischen gray_min und gray_max durch reines Weiß 
           und lässt alle anderen Bildbereiche unverändert."""
        
        if self.proc is None:  # Abbruch, falls kein Bild geladen
            return
        img = self.proc.copy()  # Arbeitskopie des Bilds anlegen
        # Bild nur  mit grauen Pixeln erzeugen
        gray_mask = cv2.inRange(img, gray_min, gray_max)
        # Nur diese Pixel  auf weiß setzen
        img[gray_mask == 255] = 255  # Python's List Comprehension
        self.proc = img  # Ergebnis übernehmen, neuer Arbeitsstand
        self.last_filtered = self.proc.copy()  # übernehmen zum Speichern
        self.updateLabel(self.label_proc, self.proc)  # GUI aktualisieren

    def reinforce_obstacles_with_canny(self, checked=False,
                                             low_thresh=50, high_thresh=150,
                                             dilate_iterations=1,
                                             obstacle_thresh=50,
                                             obstacle_neighborhood_radius=2):
        """
        Nutzt Canny, um fehlende schwarze Pixel NUR an bestehenden Hindernissen zu ergänzen.
        Hellgraue Bereiche werden nicht zu Hindernissen gemacht.
        - obstacle_thresh: Maximaler Grauwert, der als 'Hindernis' zählt (z.B. <= 50).
        - obstacle_neighborhood_radius: Radius in Pixeln, um eine Nachbarschaftsmaske zu bilden.
        """
        if self.proc is None:
            return

        img = self.proc.copy()

        # 1) Maske der aktuellen schwarzen/dunklen Hindernisse
        #    (alles <= obstacle_thresh gilt als Hindernis)
        obstacle_mask = (img <= obstacle_thresh).astype(np.uint8) * 255  # 0/255

        # 2) Invertierte Map für Canny (damit Hindernisstrukturen hell sind)
        inv = 255 - img

        # 3) Kanten berechnen
        edges = cv2.Canny(inv, low_thresh, high_thresh)

        # 4) Kanten optional etwas verbreitern per Dilatation
        if dilate_iterations > 0:
            kernel3 = np.ones((3, 3), np.uint8)
            edges = cv2.dilate(edges, kernel3, iterations=dilate_iterations)

        # 5) Nachbarschaft der Hindernisse berechnen:
        #    Hindernismaske leicht dilatieren, damit wir eine Umgebung erhalten
        if obstacle_neighborhood_radius > 0:
            ksize = 2 * obstacle_neighborhood_radius + 1
            kernel_neigh = np.ones((ksize, ksize), np.uint8)
            obstacle_neigh = cv2.dilate(obstacle_mask, kernel_neigh, iterations=1)
        else:
            obstacle_neigh = obstacle_mask

        # 6) Nur Kanten in der Hindernis-Nachbarschaft zulassen
        candidate_edges = cv2.bitwise_and(edges, obstacle_neigh)

        # 7) Diese Kandidaten als neue Hindernisse einzeichnen:
        #    Pixel nur dort auf schwarz setzen, wo candidate_edges=255
        img[candidate_edges == 255] = 0

        self.proc = img
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def remove_small_obstacle_islands(self, checked=False, 
                                      min_area=10, connectivity=8):
        """
        Entfernt kleine isolierte Hindernisinseln (Blobs) mittels Connected-Component-Analyse.
        - min_area: Minimale Fläche in Pixeln (z.B. 10 = Blobs < 10 Pixel löschen).
        - connectivity: 4 (nur orthogonal) oder 8 (inkl. Diagonalen).
        """
        if self.proc is None:
            return

        img = self.proc.copy()

        # 1) Binärmaske der Hindernisse: schwarz (0) -> 255, Rest -> 0
        # (Schwellwert anpassen, z.B. dunklere Pixel als Hindernisse)
        obstacle_thresh = 50  # Alles <= 50 gilt als Hindernis
        obstacle_mask = (img <= obstacle_thresh).astype(np.uint8) * 255

        # 2) Connected Components mit Statistiken
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            obstacle_mask, connectivity=connectivity, ltype=cv2.CV_32S
        )

        # 3) Labels 1 bis num_labels-1 sind Hindernis-Komponenten
        #    stats[label, cv2.CC_STAT_AREA] gibt die Fläche
        for label in range(1, num_labels):
            area = stats[label, cv2.CC_STAT_AREA]
            if area < min_area:
                # Kleine Insel: alle Pixel dieses Labels auf 0 setzen (in Maske)
                obstacle_mask[labels == label] = 0

        # 4) Maske zurück auf Originalbild übertragen:
        #    Wo Maske 0 ist, wird das Original weiß (255) gesetzt
        #    (nur Hindernisse bleiben schwarz, wo sie groß genug sind)
        img[obstacle_mask == 0] = 255  # Freiraum weiß machen

        self.proc = img
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEnhanceGUI()
    window.show()
    sys.exit(app.exec())
