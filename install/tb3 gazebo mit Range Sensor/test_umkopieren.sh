#!/bin/bash
set -e

# Pfade definieren
HOME_DIR="$HOME"
SRC_FILE="$HOME_DIR/Dokumente/test.urdf"
BACKUP_FILE="$HOME_DIR/Dokumente/test(copy).urdf"
NEW_FILE="$HOME_DIR/Dokumente/testordner/test_neu.urdf"
TARGET_FILE="$HOME_DIR/Dokumente/test.urdf"

# 1. Existierende test.urdf umbenennen
if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$BACKUP_FILE"
    echo "Backup erstellt: $BACKUP_FILE"
else
    echo "WARNUNG: $SRC_FILE wurde nicht gefunden. Es wird kein Backup erstellt."
fi

# 2. Neue Datei kopieren und umbenennen
if [ -f "$NEW_FILE" ]; then
    cp "$NEW_FILE" "$TARGET_FILE"
    echo "Neue Datei kopiert nach: $TARGET_FILE"
else
    echo "FEHLER: $NEW_FILE wurde nicht gefunden!"
    exit 1
fi

echo "Vorgang abgeschlossen."

