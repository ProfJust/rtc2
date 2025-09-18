import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
from scipy.spatial.transform import Rotation as R

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.30)

init_axis = np.array([0, 0, 1])
init_angle = 0
init_quat = R.from_rotvec(init_angle * init_axis).as_quat()
v = np.array([1, 0, 0])

def plot_quaternion(q):
    ax.cla()
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    r = R.from_quat(q)
    v_rot = r.apply(v)
    ax.quiver(0, 0, 0, v[0], v[1], v[2], color='gray', linewidth=2, label='Original')
    ax.quiver(0, 0, 0, v_rot[0], v_rot[1], v_rot[2], color='blue', linewidth=2, label='Rotiert')
    ax.quiver(0, 0, 0, q[0], q[1], q[2], color='red', linewidth=2, label='Drehachse (x,y,z)')
    ax.legend(loc='upper left')

plot_quaternion(init_quat)

axcolor = 'lightgoldenrodyellow'
ax_x = plt.axes([0.2, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_y = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_z = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_theta = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)

s_x = Slider(ax_x, 'Achse X', -1.0, 1.0, valinit=init_axis[0])
s_y = Slider(ax_y, 'Achse Y', -1.0, 1.0, valinit=init_axis[1])
s_z = Slider(ax_z, 'Achse Z', -1.0, 1.0, valinit=init_axis[2])
s_theta = Slider(ax_theta, 'Winkel (rad)', 0, 2*np.pi, valinit=init_angle)

def update(val):
    axis = np.array([s_x.val, s_y.val, s_z.val])
    if np.linalg.norm(axis) == 0:
        axis = np.array([0, 0, 1])
    axis = axis / np.linalg.norm(axis)
    theta = s_theta.val
    q = R.from_rotvec(theta * axis).as_quat()
    plot_quaternion(q)
    fig.canvas.draw_idle()

s_x.on_changed(update)
s_y.on_changed(update)
s_z.on_changed(update)
s_theta.on_changed(update)

plt.show()
