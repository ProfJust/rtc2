import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class PixelInspector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pixel Inspector (Grauwert anzeigen)")
        self.resize(900, 600)

        self.img = None  # OpenCV-Graustufenbild

        # Bild-Label
        self.label_img = QLabel("Bild laden und anklicken")
        self.label_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_img.setStyleSheet("background-color: #202020; color: white;")

        # Info-Label für Koordinaten + Wert
        self.label_info = QLabel("x=?, y=?, Wert=?")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Button zum Laden
        self.btn_load = QPushButton("Bild laden (PGM / PNG / JPG)")
        self.btn_load.clicked.connect(self.loadImage)

        # Layout
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_img, stretch=1)
        v_layout.addWidget(self.label_info)
        v_layout.addWidget(self.btn_load)
        self.setLayout(v_layout)

        # Maus-Event am Label abfangen
        self.label_img.mousePressEvent = self.on_label_click

    def loadImage(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Graustufenbild laden",
            "",
            "Images (*.pgm *.png *.jpg *.jpeg *.bmp)"
        )
        if not file:
            return

        # Als Graustufenbild laden
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        if img is None:
            QMessageBox.critical(self, "Fehler", f"Bild konnte nicht geladen werden:\n{file}")
            return

        self.img = img
        self.showImage()
        self.label_info.setText("x=?, y=?, Wert=?")

    def showImage(self):
        if self.img is None:
            return

        img = self.img
        h, w = img.shape
        bytes_per_line = w
        qimg = QImage(
            img.data, w, h, bytes_per_line,
            QImage.Format.Format_Grayscale8
        )
        pix = QPixmap.fromImage(qimg).scaled(
            self.label_img.width() if self.label_img.width() > 0 else 800,
            self.label_img.height() if self.label_img.height() > 0 else 500,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label_img.setPixmap(pix)

    def resizeEvent(self, event):
        # Bei Fenstergröße ändern das Bild neu skalieren
        super().resizeEvent(event)
        if self.img is not None:
            self.showImage()

    def on_label_click(self, event):
        if self.img is None or self.label_img.pixmap() is None:
            return

        img = self.img
        img_h, img_w = img.shape

        label_w = self.label_img.width()
        label_h = self.label_img.height()

        # Klickposition im Label
        x = event.position().x()
        y = event.position().y()

        # Skalierung (das Bild wird mit KeepAspectRatio eingepasst)
        scale = min(label_w / img_w, label_h / img_h)
        disp_w = img_w * scale
        disp_h = img_h * scale

        # zentrierter Offset
        offset_x = (label_w - disp_w) / 2
        offset_y = (label_h - disp_h) / 2

        # Prüfen, ob Klick im Bild liegt
        if not (offset_x <= x <= offset_x + disp_w and
                offset_y <= y <= offset_y + disp_h):
            return

        # Umrechnung Label-Koordinate -> Bildkoordinate
        img_x = int((x - offset_x) / scale)
        img_y = int((y - offset_y) / scale)

        # Sicherheitscheck
        if img_x < 0 or img_x >= img_w or img_y < 0 or img_y >= img_h:
            return

        value = int(img[img_y, img_x])  # Grauwert 0..255

        self.label_info.setText(f"x={img_x}, y={img_y}, Wert={value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PixelInspector()
    w.show()
    sys.exit(app.exec())
