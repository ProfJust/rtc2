import sys
import cv2
import numpy as np

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QMessageBox
)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QPoint

class MapEditGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROS2 PGM Map Editor")
        self.resize(1400, 800)

        # Bilder
        self.orig = None     # Original
        self.proc = None     # Bearbeitet
        self.undo_stack = [] # einfache Undo-History

        # Zeichenparameter
        self.current_tool = "black_brush"
        self.brush_size = 5
        self.drawing = False
        self.last_point = QPoint()
        self.rect_start = None

        # Labels
        self.label_orig = QLabel("Original")
        self.label_proc = QLabel("Bearbeitet")
        for lbl in (self.label_orig, self.label_proc):
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("background-color: #202020; color: white;")

        # Buttons und Controls
        self.btn_load = QPushButton("PGM laden")
        self.btn_save = QPushButton("Bearbeitete Karte als PGM speichern")
        self.btn_undo = QPushButton("Rückgängig")

        self.tool_combo = QComboBox()
        self.tool_combo.addItems([
            "Pinsel Schwarz (Hindernis)",
            "Pinsel Weiß (Freiraum)",
            "Rechteck Hindernis",
            "Rechteck Freiraum"
        ])

        self.brush_size_spin = QSpinBox()
        self.brush_size_spin.setRange(1, 100)
        self.brush_size_spin.setValue(self.brush_size)

        # Layout
        h_imgs = QHBoxLayout()
        h_imgs.addWidget(self.label_orig, stretch=1)
        h_imgs.addWidget(self.label_proc, stretch=1)

        h_tools = QHBoxLayout()
        h_tools.addWidget(self.btn_load)
        h_tools.addWidget(self.btn_save)
        h_tools.addWidget(self.btn_undo)
        h_tools.addWidget(self.tool_combo)
        h_tools.addWidget(QLabel("Pinselgröße:"))
        h_tools.addWidget(self.brush_size_spin)

        v_main = QVBoxLayout()
        v_main.addLayout(h_imgs, stretch=1)
        v_main.addLayout(h_tools)
        self.setLayout(v_main)

        # Verbindungen
        self.btn_load.clicked.connect(self.loadImage)
        self.btn_save.clicked.connect(self.saveImage)
        self.btn_undo.clicked.connect(self.undo)
        self.tool_combo.currentIndexChanged.connect(self.onToolChanged)
        self.brush_size_spin.valueChanged.connect(self.onBrushSizeChanged)

        # Maus-Events auf bearbeitetem Label umleiten
        self.label_proc.mousePressEvent = self.on_mouse_press
        self.label_proc.mouseMoveEvent = self.on_mouse_move
        self.label_proc.mouseReleaseEvent = self.on_mouse_release

    # --- Bild laden / speichern ------------------------------------------------

    def loadImage(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "PGM oder Graubild laden", "",
            "Images (*.pgm *.png *.jpg *.jpeg *.bmp)"
        )
        if not file:
            return

        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
        if img is None:
            QMessageBox.critical(self, "Fehler", f"Bild konnte nicht geladen werden:\n{file}")
            return

        # Auf 8-bit-Graustufe normalisieren, falls nötig
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if img.dtype != np.uint8:
            img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        self.orig = img.copy()
        self.proc = img.copy()
        self.undo_stack.clear()

        self.updateLabel(self.label_orig, self.orig)
        self.updateLabel(self.label_proc, self.proc)

    def saveImage(self):
        if self.proc is None:
            QMessageBox.warning(self, "Warnung", "Kein Bild zum Speichern vorhanden.")
            return
        file, _ = QFileDialog.getSaveFileName(
            self, "PGM speichern", "map_edited.pgm", "PGM Files (*.pgm)"
        )
        if not file:
            return
        if not file.lower().endswith(".pgm"):
            file += ".pgm"

        ok = cv2.imwrite(file, self.proc)
        if ok:
            QMessageBox.information(self, "Erfolg", f"Datei gespeichert:\n{file}")
        else:
            QMessageBox.critical(self, "Fehler", f"Speichern fehlgeschlagen:\n{file}")

    # --- Anzeige ---------------------------------------------------------------

    def updateLabel(self, label, img):
        if img is None:
            return

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

        target_w = label.width() if label.width() > 0 else 800
        target_h = label.height() if label.height() > 0 else 600

        pix = QPixmap.fromImage(qimg).scaled(
            target_w, target_h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(pix)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.orig is not None:
            self.updateLabel(self.label_orig, self.orig)
        if self.proc is not None:
            self.updateLabel(self.label_proc, self.proc)

    # --- Werkzeuge / Parameter -------------------------------------------------

    def onToolChanged(self, index):
        text = self.tool_combo.currentText()
        if text.startswith("Pinsel Schwarz"):
            self.current_tool = "black_brush"
        elif text.startswith("Pinsel Weiß"):
            self.current_tool = "white_brush"
        elif text.startswith("Rechteck Hindernis"):
            self.current_tool = "rect_black"
        elif text.startswith("Rechteck Freiraum"):
            self.current_tool = "rect_white"

    def onBrushSizeChanged(self, val):
        self.brush_size = int(val)

    def push_undo(self):
        if self.proc is not None:
            self.undo_stack.append(self.proc.copy())
            if len(self.undo_stack) > 20:
                self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            return
        self.proc = self.undo_stack.pop()
        self.updateLabel(self.label_proc, self.proc)

    # --- Koordinaten-Mapping Label <-> Bild -----------------------------------

    def label_to_image_coords(self, event):
        """Mappt Mausposition im Label auf Pixelkoordinate im Bild."""
        if self.proc is None or self.label_proc.pixmap() is None:
            return None

        img_h, img_w = self.proc.shape
        label_w = self.label_proc.width()
        label_h = self.label_proc.height()

        x = event.position().x()
        y = event.position().y()

        scale = min(label_w / img_w, label_h / img_h)
        disp_w = img_w * scale
        disp_h = img_h * scale

        offset_x = (label_w - disp_w) / 2
        offset_y = (label_h - disp_h) / 2

        if not (offset_x <= x <= offset_x + disp_w and
                offset_y <= y <= offset_y + disp_h):
            return None

        img_x = int((x - offset_x) / scale)
        img_y = int((y - offset_y) / scale)

        if img_x < 0 or img_x >= img_w or img_y < 0 or img_y >= img_h:
            return None

        return img_x, img_y

    # --- Maus-Events (Zeichenlogik) -------------------------------------------

    def on_mouse_press(self, event):
        if self.proc is None:
            return
        pos = self.label_to_image_coords(event)
        if pos is None:
            return

        self.push_undo()
        self.drawing = True
        self.last_point = QPoint(*pos)
        self.rect_start = QPoint(*pos)

        if self.current_tool in ("black_brush", "white_brush"):
            self.draw_brush(pos)

    def on_mouse_move(self, event):
        if not self.drawing or self.proc is None:
            return
        pos = self.label_to_image_coords(event)
        if pos is None:
            return

        if self.current_tool in ("black_brush", "white_brush"):
            self.draw_brush(pos)
            self.last_point = QPoint(*pos)
        else:
            # Rechteck-Werkzeuge: Live-Vorschau könnte man zeichnen,
            # hier wird aber erst beim Loslassen final gezeichnet.
            pass

    def on_mouse_release(self, event):
        if not self.drawing or self.proc is None:
            return
        pos = self.label_to_image_coords(event)
        if pos is None:
            self.drawing = False
            return

        if self.current_tool in ("rect_black", "rect_white"):
            self.draw_rect(self.rect_start, QPoint(*pos))

        self.drawing = False
        self.updateLabel(self.label_proc, self.proc)

    def draw_brush(self, pos):
        x, y = pos
        color = 0 if self.current_tool == "black_brush" else 255
        r = self.brush_size // 2
        x1 = max(0, x - r)
        x2 = min(self.proc.shape[1], x + r + 1)
        y1 = max(0, y - r)
        y2 = min(self.proc.shape[0], y + r + 1)
        self.proc[y1:y2, x1:x2] = color
        self.updateLabel(self.label_proc, self.proc)

    def draw_rect(self, p1, p2):
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()
        x_min, x_max = sorted((x1, x2))
        y_min, y_max = sorted((y1, y2))
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(self.proc.shape[1]-1, x_max)
        y_max = min(self.proc.shape[0]-1, y_max)

        color = 0 if self.current_tool == "rect_black" else 255
        self.proc[y_min:y_max+1, x_min:x_max+1] = color

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MapEditGUI()
    w.show()
    sys.exit(app.exec())
