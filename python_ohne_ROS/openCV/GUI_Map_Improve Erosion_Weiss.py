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
        self.btn_erode = QPushButton("Erosion anwenden")
        self.btn_dilate = QPushButton("Dilatation anwenden")
        self.btn_canny = QPushButton("Canny-Kanten")
        self.btn_reset = QPushButton("Reset")
        self.btn_save = QPushButton("Karte speichern (aktuell)")

        # Slider für Erosion/Dilatation-Iterationen
        # Bereich 1..10 Iterationen
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

        # Layout für Slider + Buttons Erosion/Dilatation
        v_layout_morph = QVBoxLayout()
        v_layout_morph.addWidget(QLabel("Erosion Iterationen"))
        v_layout_morph.addWidget(self.slider_erode)
        v_layout_morph.addWidget(self.btn_erode)
        v_layout_morph.addWidget(QLabel("Dilatation Iterationen"))
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

        # Erwartet: 8-Bit Graustufen (PGM von ROS2 map_saver)
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
        # Einfacher rechteckiger Kernel 3x3
        kernel = np.ones((3, 3), np.uint8)
        eroded = cv2.erode(self.proc, kernel, iterations=iterations)
        self.proc = eroded
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyDilate(self):
        if self.proc is None:
            return
        iterations = self.slider_dilate.value()
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(self.proc, kernel, iterations=iterations)
        self.proc = dilated
        self.last_filtered = self.proc.copy()
        self.updateLabel(self.label_proc, self.proc)

    def applyCanny(self):
        if self.proc is None:
            return
        # pragmatische Standardwerte, bei Bedarf weiter parametrisierbar
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
