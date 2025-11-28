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

    # Zur starkes Erodieren
    # def applyErode(self):
    #     if self.proc is None:
    #         return
    #     iterations = self.slider_erode.value()
    #     kernel = np.ones((3, 3), np.uint8)

    #     # Hindernisse sind schwarz (0), freier Raum hell/weiß (nahe 255)
    #     # Um Erosion auf „schwarze Hindernisse“ anzuwenden:
    #     # 1. Invertieren -> Hindernisse werden weiß
    #     # 2. Erosion auf invertiertem Bild
    #     # 3. Zurück invertieren
    #     inv = 255 - self.proc
    #     eroded_inv = cv2.erode(inv, kernel, iterations=iterations)
    #     eroded = 255 - eroded_inv

    #     self.proc = eroded
    #     self.last_filtered = self.proc.copy()
    #     self.updateLabel(self.label_proc, self.proc)

    def applyErode(self):
        if self.proc is None:
            return
        iterations = self.slider_erode.value()

        # schwächerer Kernel: Kreuz statt vollem 3x3-Quadrat
        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)

        # Hindernisse sind schwarz -> invertieren, auf Weiß erodieren, zurück invertieren
        inv = 255 - self.proc
        eroded_inv = cv2.erode(inv, kernel, iterations=iterations)
        eroded = 255 - eroded_inv

        self.proc = eroded
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyDilate(self):
        if self.proc is None:
            return
        iterations = self.slider_dilate.value()
        kernel = np.ones((3, 3), np.uint8)

        # Für „Hindernisse dicker“: gleiche Logik -> auf Schwarz arbeiten
        inv = 255 - self.proc
        dilated_inv = cv2.dilate(inv, kernel, iterations=iterations)
        dilated = 255 - dilated_inv

        self.proc = dilated
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyCanny(self):
        if self.proc is None:
            return
        low = 50
        high = 150
        edges = cv2.Canny(self.proc, low, high)
        self.last_filtered = edges
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
            
    # def fill_small_gray_holes(self, checked=False, 
    #                           gray_min=200, 
    #                           gray_max=210, 
    #                           kernel_size=11):
    #     """
    #     Nur kleine hellgraue Löcher im freien (weißen) Raum auffüllen:
    #     - Schwarz (Hindernisse) bleiben unverändert.
    #     - Nur Pixel, die vorher in [gray_min, gray_max] lagen, dürfen auf Weiß gesetzt werden.
    #     """
    #     if self.proc is None:
    #         return

    #     img = self.proc.copy()

    #     # 1) Maske der hellgrauen Flächen (Kandidaten, die weiß werden dürfen)
    #     gray_mask = cv2.inRange(img, gray_min, gray_max)  # 255 = hellgrau, 0 = sonst
    #     # cv2.imshow("gray_mask", gray_mask)

    #     # 2) Binärbild für weißen freien Raum (weiß + hellgrau)
    #     _, binary = cv2.threshold(img, gray_min, 255, cv2.THRESH_BINARY)
    #     # cv2.imshow("binary", binary)

    #     # 3) Morphological Closing auf diesem Binärbild
    #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    #     cv2.imshow("kernel", kernel)
    #     closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    #     #cv2.imshow("closed", closed)

    #     # 4) Neue weiße Pixel: Stellen, die vorher NICHT binär-weiß waren, nach Closing aber schon
    #     new_white = cv2.bitwise_and(closed, cv2.bitwise_not(binary))
    #     #cv2.imshow("new_white_raw", cv2.bitwise_and(closed, cv2.bitwise_not(binary)))
    #     # Auf hellgraue Kandidaten einschränken
    #     new_white = cv2.bitwise_and(new_white, gray_mask)
    #     #cv2.imshow("new_white_final", new_white)

    #     # 5) Nur diese neuen weißen Pixel in die Karte übernehmen
    #     img[new_white == 255] = 255

    #     self.proc = img
    #     self.last_filtered = self.proc.copy()
    #     self.updateLabel(self.label_proc, self.proc)

    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    def gray_2_white(self, checked=False, gray_min=200, gray_max=210):
        if self.proc is None:
            return
        img = self.proc.copy()
        gray_mask = cv2.inRange(img, gray_min, gray_max)
        img[gray_mask == 255] = 255
        self.proc = img
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)



    def reinforce_obstacles_with_canny(self, checked=False,
                                             low_thresh=50, high_thresh=150,
                                             dilate_iterations=1,
                                             obstacle_thresh=50,
                                             obstacle_neighborhood_radius=1):
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

        # 4) Kanten optional etwas verbreitern
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEnhanceGUI()
    window.show()
    sys.exit(app.exec())
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
        self.btn_canny = QPushButton("Canny-Kanten")
        self.btn_reset = QPushButton("Reset")
        self.btn_save = QPushButton("Karte speichern (aktuell)")

        # Slider für Erosion/Dilatation-Iterationen
        self.slider_erode = QSlider(Qt.Orientation.Horizontal)
        self.slider_erode.setRange(1, 10)
        self.slider_erode.setValue(1)
        self.slider_erode.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_erode.setTickInterval(1)

        self.slider_dilate = QSlider(Qt.Orientation.Horizontal)
        self.slider_dilate.setRange(1, 10)
        self.slider_dilate.setValue(1)
        self.slider_dilate.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_dilate.setTickInterval(1)

        # Layout für Bilder
        h_layout_images = QHBoxLayout()
        h_layout_images.addWidget(self.label_orig)
        h_layout_images.addWidget(self.label_proc)

        # Layout für Morphologie
        v_layout_morph = QVBoxLayout()
        v_layout_morph.addWidget(QLabel("Erosion Iterationen (Hindernisse dünner)"))
        v_layout_morph.addWidget(self.slider_erode)
        v_layout_morph.addWidget(self.btn_erode)
        v_layout_morph.addWidget(QLabel("Dilatation Iterationen (Hindernisse dicker)"))
        v_layout_morph.addWidget(self.slider_dilate)
        v_layout_morph.addWidget(self.btn_dilate)

        # Hauptlayout
        v_layout_main = QVBoxLayout()
        v_layout_main.addLayout(h_layout_images)
        v_layout_main.addWidget(self.btn_load)
        v_layout_main.addLayout(v_layout_morph)
        v_layout_main.addWidget(self.btn_hist)
        v_layout_main.addWidget(self.btn_canny)
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
        kernel = np.ones((3, 3), np.uint8)

        # Hindernisse sind schwarz (0), freier Raum hell/weiß (nahe 255)
        # Um Erosion auf „schwarze Hindernisse“ anzuwenden:
        # 1. Invertieren -> Hindernisse werden weiß
        # 2. Erosion auf invertiertem Bild
        # 3. Zurück invertieren
        inv = 255 - self.proc
        eroded_inv = cv2.erode(inv, kernel, iterations=iterations)
        eroded = 255 - eroded_inv

        self.proc = eroded
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyDilate(self):
        if self.proc is None:
            return
        iterations = self.slider_dilate.value()
        kernel = np.ones((3, 3), np.uint8)

        # Für „Hindernisse dicker“: gleiche Logik -> auf Schwarz arbeiten
        inv = 255 - self.proc
        dilated_inv = cv2.dilate(inv, kernel, iterations=iterations)
        dilated = 255 - dilated_inv

        self.proc = dilated
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyCanny(self):
        if self.proc is None:
            return
        low = 50
        high = 150
        edges = cv2.Canny(self.proc, low, high)
        self.last_filtered = edges
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEnhanceGUI()
    window.show()
    sys.exit(app.exec())
