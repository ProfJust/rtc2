import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# ------------------------------------------------------------
# Quaternion -> Rotationsmatrix
# ------------------------------------------------------------
def quaternion_to_matrix(x, y, z, w):

    q = np.array([x, y, z, w], dtype=float)
    norm = np.linalg.norm(q)

    if norm < 1e-8:
        q = np.array([0.0, 0.0, 0.0, 1.0])
    else:
        q = q / norm

    x, y, z, w = q

    R = np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - z*w),     2*(x*z + y*w)],
        [2*(x*y + z*w),     1 - 2*(x*x + z*z), 2*(y*z - x*w)],
        [2*(x*z - y*w),     2*(y*z + x*w),     1 - 2*(x*x + y*y)]
    ])

    return q, R


# ------------------------------------------------------------
# Quaternion -> Achse, Winkel und Rotationsvektor
# ------------------------------------------------------------
def quaternion_to_axis_angle(q):

    q = np.array(q, dtype=float)

    # q und -q beschreiben dieselbe Orientierung.
    # Hier wird die kürzeste Rotation verwendet.
    if q[3] < 0:
        q = -q

    v = q[:3]
    w = np.clip(q[3], -1.0, 1.0)

    s = np.linalg.norm(v)

    if s < 1e-8:
        axis = np.array([1.0, 0.0, 0.0])
        alpha = 0.0
    else:
        axis = v / s
        alpha = 2 * np.arctan2(s, w)

    rotvec = axis * alpha

    return axis, alpha, rotvec

# ------------------------------------------------------------
# Figure
# ------------------------------------------------------------
fig = plt.figure(figsize=(14, 8))

# Platz für Slider unten lassen
plt.subplots_adjust(bottom=0.30)

ax = fig.add_subplot(121, projection="3d")
ax_info = fig.add_subplot(122)

ax_info.axis("off")


# ------------------------------------------------------------
# Slider
# ------------------------------------------------------------
slider_x_ax = plt.axes([0.15, 0.20, 0.65, 0.025])
slider_y_ax = plt.axes([0.15, 0.16, 0.65, 0.025])
slider_z_ax = plt.axes([0.15, 0.12, 0.65, 0.025])
slider_w_ax = plt.axes([0.15, 0.08, 0.65, 0.025])

slider_x = Slider(slider_x_ax, "x", -1, 1, valinit=0.3)
slider_y = Slider(slider_y_ax, "y", -1, 1, valinit=0.5)
slider_z = Slider(slider_z_ax, "z", -1, 1, valinit=0.8)
slider_w = Slider(slider_w_ax, "w", -1, 1, valinit=0.5)


# ------------------------------------------------------------
# Kugel zeichnen
# ------------------------------------------------------------
def draw_sphere(ax):

    u = np.linspace(0, 2*np.pi, 30)
    v = np.linspace(0, np.pi, 15)

    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_wireframe(
        xs, ys, zs,
        linewidth=0.3,
        alpha=0.15
    )


# ------------------------------------------------------------
# Koordinatensystem zeichnen
# ------------------------------------------------------------
def draw_coordinate_system(ax, R=None, length=0.8):

    if R is None:
        R = np.eye(3)

    labels = ["X", "Y", "Z"]

    for i in range(3):

        vec = R[:, i] * length

        ax.quiver(
            0, 0, 0,
            vec[0], vec[1], vec[2],
            linewidth=3
        )

        ax.text(
            vec[0] * 1.1,
            vec[1] * 1.1,
            vec[2] * 1.1,
            labels[i],
            fontsize=12,
            fontweight="bold"
        )


def pfeil(start, richtung, farbe, label, laenge=1.0):

    v = np.array(richtung) * laenge

    ax.quiver(
        *start,
        *v,
        color=farbe,
        linewidth=2.5,
        arrow_length_ratio=0.12
    )

    ende = np.array(start) + v * 1.12

    ax.text(
        *ende,
        label,
        color=farbe,
        fontsize=12,
        fontweight="bold"
    )

# ------------------------------------------------------------
# Update
# ------------------------------------------------------------
def update(val=None):
    # Quaternion aus den vier vorhandenen Slidern
    x = slider_x.val
    y = slider_y.val
    z = slider_z.val
    w = slider_w.val

    # Normiertes Quaternion und Rotationsmatrix
    q, R = quaternion_to_matrix(x, y, z, w)

    # Rotationsachse, Winkel und Rotationsvektor
    axis, angle, rotvec = quaternion_to_axis_angle(q)
    # 3D-Grafik
    ax.cla()
    ax.set_title("Rotation im 3D-Raum", fontsize=14)

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_zlim(-1.3, 1.3)
    ax.set_box_aspect([1, 1, 1])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=23, azim=-60)

    # Einheitskugel
    u = np.linspace(0, 2*np.pi, 35)
    v = np.linspace(0, np.pi, 20)

    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))

    ax.plot_wireframe(
        xs, ys, zs,
        color="gray", alpha=0.15, linewidth=0.5
    )

    ursprung = np.zeros(3)
    achsen = np.eye(3)

    # Ursprüngliches Koordinatensystem: GRÜN
    for i, name in enumerate(["X", "Y", "Z"]):
        pfeil(
            ursprung, achsen[:, i],
            "green", name, laenge=0.9
        )

    # Rotiertes Koordinatensystem: ROT
    for i, name in enumerate(["X'", "Y'", "Z'"]):
        pfeil(
            ursprung, R[:, i],
            "red", name, laenge=0.9
        )

    # Rotationsachse und Rotationsvektor: ROT
    if angle > 1e-8:

        # Rotationsachse (gestrichelt)
        ax.plot(
            [-axis[0], axis[0]],
            [-axis[1], axis[1]],
            [-axis[2], axis[2]],
            color="red",
            linestyle="--",
            linewidth=1.5,
            alpha=0.5
        )

        # Rotationsvektor r = alpha * u
        # Zur Darstellung auf 1.15 skaliert
        pfeil(
            ursprung, axis,
            "darkred", "r",
            laenge=1.15
        )

    # Informationen rechts
    ax_info.cla()
    ax_info.axis("off")

    winkel_grad = np.degrees(angle)

    info = (
        "NORMIERTES QUATERNION\n"
        f"x = {q[0]: .4f}\n"
        f"y = {q[1]: .4f}\n"
        f"z = {q[2]: .4f}\n"
        f"w = {q[3]: .4f}\n\n"

        "ROTATIONSWINKEL\n"
        f"alpha = {winkel_grad:.2f} Grad "
        f"({angle:.4f} rad)\n\n"

        "ROTATIONSVEKTOR [rad]\n"
        f"rx = {rotvec[0]: .4f}\n"
        f"ry = {rotvec[1]: .4f}\n"
        f"rz = {rotvec[2]: .4f}\n\n"

        "ROTATIONSMATRIX\n"
        f"{np.array2string(R, precision=2, suppress_small=True)}"
    )

    ax_info.text(
        0.02, 0.98, info,
        va="top", ha="left",
        fontsize=10,
        family="monospace"
    )

    fig.canvas.draw_idle()


# ------------------------------------------------------------
# Buttons für Standardrotationen um die Z-Achse
# ------------------------------------------------------------

standardwinkel = [0, 90, 180, 270, 360]

buttons = []

for i, winkel in enumerate(standardwinkel):

    # Button-Position
    ax_button = fig.add_axes([
        0.15 + i * 0.14,
        0.015,
        0.12,
        0.045
    ])

    button = Button(ax_button, f"{winkel}°")

    # Callback mit festem Winkelwert
    def set_winkel(event, winkel=winkel):

        alpha = np.radians(winkel)

        # Quaternion für Rotation um Z
        qx = 0.0
        qy = 0.0
        qz = np.sin(alpha / 2)
        qw = np.cos(alpha / 2)

        # Slider einstellen
        slider_x.set_val(qx)
        slider_y.set_val(qy)
        slider_z.set_val(qz)
        slider_w.set_val(qw)

    button.on_clicked(set_winkel)

    # Referenz speichern
    buttons.append(button)


# ------------------------------------------------------------
# Slider mit Update verbinden
# ------------------------------------------------------------
slider_x.on_changed(update)
slider_y.on_changed(update)
slider_z.on_changed(update)
slider_w.on_changed(update)


# Anfangsdarstellung
update()

plt.show()