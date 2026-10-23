import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Anfangswinkel
winkel_start = 90

# Figure mit zwei Bereichen
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
plt.subplots_adjust(bottom=0.25, wspace=0.4)

# --------------------------------------------------
# Links: Rotation in der XY-Ebene
# --------------------------------------------------
ax1.set_title("Rotation um die Z-Achse")
ax1.set_xlim(-1.3, 1.3)
ax1.set_ylim(-1.3, 1.3)
ax1.set_aspect("equal")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.grid(True)

# Einheitskreis
kreis = plt.Circle((0, 0), 1, fill=False,
                   linestyle="--", color="gray")
ax1.add_patch(kreis)

# Ausgangsvektor (X-Achse)
ax1.plot([0, 1], [0, 0], "--", color="gray",
         label="Ausgangsrichtung")

# Rotierter Vektor
vektor, = ax1.plot([], [], "b-", linewidth=3,
                   marker="o", label="Rotierter Vektor")
ax1.legend(loc="upper right")

# --------------------------------------------------
# Rechts: Quaternion-Komponenten
# --------------------------------------------------
ax2.set_title("Quaternion (x, y, z, w)")
ax2.set_ylim(-1.1, 1.1)
ax2.grid(axis="y")

balken = ax2.bar(["x", "y", "z", "w"], [0, 0, 0, 0],
                 color=["red", "green", "blue", "orange"])

# Textausgabe
text = ax2.text(
    0.5, 1.05, "",
    transform=ax2.transAxes,
    ha="center",
    fontsize=11
)

# --------------------------------------------------
# Slider
# --------------------------------------------------
slider_ax = plt.axes([0.2, 0.08, 0.6, 0.04])

slider = Slider(
    ax=slider_ax,
    label="Winkel [Grad]",
    valmin=0,
    valmax=360,
    valinit=winkel_start,
    valstep=1
)

# --------------------------------------------------
# Aktualisierung der Grafik
# --------------------------------------------------

def update(winkel):

    alpha = np.radians(winkel)

    # Quaternion für Rotation um Z
    qx = 0
    qy = 0
    qz = np.sin(alpha / 2)
    qw = np.cos(alpha / 2)

    quaternion = [qx, qy, qz, qw]

    # Rotierter Einheitsvektor
    vx = np.cos(alpha)
    vy = np.sin(alpha)

    vektor.set_data([0, vx], [0, vy])

    # Balkendiagramm aktualisieren
    for balken_objekt, wert in zip(balken, quaternion):
        balken_objekt.set_height(wert)

    # Alte Zahlenbeschriftungen entfernen
    for beschriftung in ax2.texts[:]:
        if beschriftung != text:
            beschriftung.remove()

    # Alle vier Werte anzeigen, auch bei Null
    for i, wert in enumerate(quaternion):
        ax2.text(
            i,
            wert + 0.05 if wert >= 0 else wert - 0.08,
            f"{wert:.3f}",
            ha="center",
            va="center",
            fontsize=11
        )

    # Quaternion anzeigen
    text.set_text(
        f"q = ({qx:.3f}, {qy:.3f}, "
        f"{qz:.3f}, {qw:.3f})"
    )

    fig.canvas.draw_idle()


# Slider mit Funktion verbinden
slider.on_changed(update)

# Anfangszustand
update(winkel_start)

plt.show()