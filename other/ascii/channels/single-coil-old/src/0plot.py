import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors

def darken_color(color, amount=0.7):
    c = mcolors.to_rgb(color)
    return tuple(amount * np.array(c))

def setup_axes(ax):
    ax.set_aspect('equal')
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    for spine in ['right', 'top']:
        ax.spines[spine].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

def draw_vector(ax, r, phi, label_prefix, color='tab:blue'):
    # Convert to Cartesian
    x = r * np.cos(phi)
    y = r * np.sin(phi)

    darker_color = darken_color(color)

    # Draw components
    ax.plot([0, x], [0, 0], linestyle=':', color=color, linewidth=1.5)
    ax.plot([x, x], [0, y], linestyle=':', color=color, linewidth=1.5)

    # Draw main vector
    ax.plot([0, x], [0, y], linestyle='-', color=darker_color, linewidth=1.5)
    ax.plot(x, y, 'o', color=color, markersize=5)

    # Angle arc
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

    # Component labels
    ax.text(x / 2, -0.05, f"{label_prefix}x", ha='center', va='top', fontsize=9)
    ax.text(x + 0.05*np.sign(x), y / 2, f"{label_prefix}y", fontsize=9)
    ax.text(x / 2, y / 2, f"{label_prefix}r", fontsize=9, fontweight='bold')

    # Unit vectors
    unit_r = [np.cos(phi), np.sin(phi)]
    unit_phi = [-np.sin(phi), np.cos(phi)]

    ax.plot([0, unit_r[0]*0.8], [0, unit_r[1]*0.8], color='gray', linewidth=1)
    ax.plot([0, unit_phi[0]*0.8], [0, unit_phi[1]*0.8], color='gray', linewidth=1)

    ax.text(unit_r[0]*0.9, unit_r[1]*0.9, r'$\hat{r}$', fontsize=9)
    ax.text(unit_phi[0]*0.9, unit_phi[1]*0.9, r'$\hat{\phi}$', fontsize=9)

# === Data ===
pr = 0.8
pphi = np.pi / 6

Br = 0.9
bphi = np.pi / 3
bphi_override = np.pi / 6  # for subplot 3

# === Plot ===
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))

# Subplot 1
setup_axes(ax1)
draw_vector(ax1, pr, pphi, label_prefix='p', color='tab:blue')
ax1.set_title("1. Position Vector (pr, pphi)")

# Subplot 2
setup_axes(ax2)
draw_vector(ax2, Br, bphi, label_prefix='B', color='tab:green')
ax2.set_title("2. Magnetic Field Vector (Br, Bphi)")

# Subplot 3: combine 1 and 2, use same angle (π/6)
setup_axes(ax3)
draw_vector(ax3, pr, pphi, label_prefix='p', color='tab:blue')
draw_vector(ax3, Br, bphi_override, label_prefix='B', color='tab:green')
ax3.set_title("3. Combined Vectors (Shared Angle π/6)")

# Subplot 4: combine 1 and 2 with original angles
setup_axes(ax4)
draw_vector(ax4, pr, pphi, label_prefix='p', color='tab:blue')
draw_vector(ax4, Br, bphi, label_prefix='B', color='tab:green')
ax4.set_title("4. Combined Vectors (Original Angles)")

fig.suptitle("Polar Vector Decomposition with Unit Vectors", fontsize=14)
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

