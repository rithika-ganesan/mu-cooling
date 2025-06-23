import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors

def darken_color(color, amount=0.7):
    c = mcolors.to_rgb(color)
    return tuple(amount * np.array(c))

def draw_vector(ax, r, phi, label_prefix, color='tab:blue'):
    # Convert to Cartesian
    x = r * np.cos(phi)
    y = r * np.sin(phi)

    darker_color = darken_color(color)

    # Draw x and y components
    ax.plot([0, x], [0, 0], linestyle=':', color=color, linewidth=1.5)
    ax.plot([x, x], [0, y], linestyle=':', color=color, linewidth=1.5)

    # Draw main vector
    ax.plot([0, x], [0, y], linestyle='-', color=darker_color, linewidth=1.5)
    ax.plot(x, y, 'o', color=color, markersize=5)

    # Draw angle arc
    arc_radius = 0.2 * r
    phi_deg = np.degrees(phi)
    arc = patches.Arc((0, 0), 2*arc_radius, 2*arc_radius,
                      angle=0, theta1=0, theta2=phi_deg,
                      color=color, linewidth=1.2)
    ax.add_patch(arc)

    # Angle label
    ax.text(arc_radius * np.cos(phi / 2),
            arc_radius * np.sin(phi / 2),
            f"{label_prefix}ϕ", fontsize=9, color=color)

    # Labels for components
    ax.text(x / 2, -0.05, f"{label_prefix}x", ha='center', va='top', fontsize=9)
    ax.text(x + 0.05*np.sign(x), y / 2, f"{label_prefix}y", fontsize=9)

    # Label for main vector
    ax.text(x / 2, y / 2, f"{label_prefix}r", fontsize=9, fontweight='bold')

    # Draw unit r̂ and ϕ̂
    unit_r = [np.cos(phi), np.sin(phi)]
    unit_phi = [-np.sin(phi), np.cos(phi)]

    ax.quiver(0, 0, *unit_r, color='gray', scale=5, width=0.01)
    ax.quiver(0, 0, *unit_phi, color='gray', scale=5, width=0.01)

    ax.text(unit_r[0]*1.1, unit_r[1]*1.1, r'$\hat{r}$', fontsize=9)
    ax.text(unit_phi[0]*1.1, unit_phi[1]*1.1, r'$\hat{\phi}$', fontsize=9)

    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

# === Data ===
pr = 0.8
pphi = np.pi / 6

Br = 0.9
bphi = np.pi / 3

# === Plot ===
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))

# Subplot 1: pr vector
draw_vector(ax1, pr, pphi, label_prefix='p', color='tab:blue')
ax1.set_title("Position Vector (pr, pphi)")

# Subplot 2: Br vector
draw_vector(ax2, Br, bphi, label_prefix='B', color='tab:green')
ax2.set_title("Magnetic Field Vector (Br, Bphi)")

# Empty subplots
ax3.axis('off')
ax4.axis('off')

fig.suptitle("Polar to Cartesian Vector Decomposition with Unit Vectors", fontsize=14)
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

