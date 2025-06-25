import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Arc
import matplotlib.colors as mcolors
colors = mcolors.BASE_COLORS
names = list(colors)

print(names, colors)

#### Rotated lines:



### Cartesian components
x = np.array([+0.8, 0, +0.8])
y = np.array([+0, +0.4, +0.4])

### Angle

center = (0, 0)
width, height = 0.2, 0.2
rang = 0
theta1, theta2 = 0, np.arctan2(y[-1], x[-1])
### Polar components
xp = np.array([+0.4, -0.2])
yp = np.array([+0.2, +0.4])

xpp = np.array([+0.3, -0.1])
ypp = np.array([+0.1, +0.3])

xlines = np.array([+4, -2])
ylines = np.array([+2, +4])

phi = np.pi + np.arctan2(y[-1], x[-1])

rtwist = 2
xtwist = rtwist * np.cos(phi)
ytwist = rtwist * np.sin(phi)


#x_ = np.array([+0.5, -0.5, -0.5, +0.5])
#y_ = np.array([+0.5, +0.5, -0.5, -0.5])

#r = np.sqrt(x**2 + y**2)
#correct_phi = np.array([0.25*np.pi, 0.75*np.pi, 1.25*np.pi, 1.75*np.pi])

#b = np.array([0, 0.5*np.pi, np.pi, 1.5*np.pi])
#a = np.array([1, -1, 1, -1])
#phi = a*np.arctan(y / x) + b

#phi = np.arctan2(y, x)

#signs = list(zip(np.sign(x).astype(int), np.sign(y).astype(int)))

#sign = np.sign(x[1])
#print(sign, type(sign))

#xr = r * np.cos(phi)
#yr = r * np.sin(phi)

def position_vector(x, y):
    xc = np.array([0.0, x])
    yc = np.array([0.0, y])
    return xc, yc

#xc1, yc1 = position_vector(x[0], y[0])

# plt.scatter(x, y)
# plt.axvline(0, c='k', lw=0.5)
# plt.axhline(0, c='k', lw=0.5)
# 
# for i in range(len(x)):
#     xc, yc = position_vector(x[i], y[i])
#     plt.plot(xc, yc, lw=0.5, c='blue')
# 
# plt.xlim([-1, 1])
# plt.ylim([-1, 1])
# plt.show()
bfield = 1

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

def darken_color(color, amount=0.7):
    c = mcolors.to_rgb(color)
    return tuple(amount * np.array(c))

if bfield != 0:
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(2, 2, figsize=(10, 10))  # Two subplots side by side

    #==== BACKGROUND AXES ====
    ax1.axvline(0, c='k', lw=0.25)
    ax1.axhline(0, c='k', lw=0.25)
    ax2.axvline(0, c='k', lw=0.25)
    ax2.axhline(0, c='k', lw=0.25)
    ax3.axvline(0, c='k', lw=0.25)
    ax3.axhline(0, c='k', lw=0.25)
    ax4.axvline(0, c='k', lw=0.25)
    ax4.axhline(0, c='k', lw=0.25)
    
    #==== SET LABELS, LIMITS, TITLES ====
    lims = [-1, 1]

    ax1.set_title("Position in transverse plane")
    
    ax1.set_xlabel('$\hat{x}$')
    ax1.set_ylabel('$\hat{y}$')
    ax1.set_xlim(lims)
    ax1.set_ylim(lims)
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    ax2.set_title("B-field in the transverse plane")
    
    ax2.set_xlabel('$\hat{B_x}$')
    ax2.set_ylabel('$\hat{B_y}$')
    ax2.set_xlim(lims)
    ax2.set_ylim(lims)
    ax2.set_xticks([])
    ax2.set_yticks([])
    
    ax3.set_title("Coincident frames")
   
    ax3.set_xlabel('$\hat{x}$')
    ax3.set_ylabel('$\hat{y}$')
    ax3.set_xlim(lims)
    ax3.set_ylim(lims)
    ax3.set_xticks([])
    ax3.set_yticks([])

    ax4.set_title("Real(?) frames")

    ax4.set_xlabel('$\hat{x}$')
    ax4.set_ylabel('$\hat{y}$')
    ax4.set_xlim(lims)
    ax4.set_ylim(lims)
    ax4.set_xticks([])
    ax4.set_yticks([])

    #==== ADD POSITION VECTORS ====

    pr = 0.8
    pphi = np.pi/6
    vectors = np.array([pr * np.cos(pphi), pr * np.sin(pphi)])
    Br = 0.9
    
    for i, (x, y) in enumerate(vectors):
        color = colors[i % len(colors)]
        darker_color = darken_color(color)

        # Draw x component
        ax1.plot([0, x], [0, 0], linestyle=':', color=color, linewidth=1.5)
        # Draw y component
        ax1.plot([x, x], [0, y], linestyle=':', color=color, linewidth=1.5)
        # Draw main vector
        ax1.plot([0, x], [0, y], linestyle='-', color=darker_color, linewidth=1.5)
        # Draw dot at end
        ax1.plot(x, y, 'o', color=color, markersize=5)

    ax1.set_aspect('equal')

























# First subplot (your original plot goes here)
    ax1.scatter(x[-1], y[-1], s=15, c='blue')
    ax1.scatter(x[:2], y[:2], s=2, c='b')

    for i in range(len(x-1)):
        xc, yc = position_vector(x[i], y[i])
        ax1.plot(xc, yc, lw=1.25, ls='--', c='blue', alpha=0.6)
    xc, yc = position_vector(x[-1], y[-1])
    ax1.plot(xc, yc, lw=1.5, c='blue')

    ax1.text(x[0]-0.05, 0-0.1, '$B_x$', c='blue')
    ax1.text(0-0.1, y[1]-0.05, '$B_y$', c='blue')
    ax1.text(x[-1]/2, y[-1]/2 + 0.1, '$B_\perp$', c='blue')
    ax1.set_xlim([-1, 1])
    ax1.set_xticks([])
    ax1.set_ylim([-1, 1])
    ax1.set_yticks([])
    ax1.set_xlabel('X-axis')
    ax1.set_ylabel('Y-axis')

    # Second subplot (empty for now or add your content here)
    ax2.scatter(x[-1], y[-1], s=15, c='blue')
    ax2.axvline(0, c='k', lw=0.25)
    ax2.axhline(0, c='k', lw=0.25)

    xc, yc = position_vector(x[-1], y[-1])
    ax2.plot(xc, yc, lw=1.5, c='blue')
    ax2.text(x[-1]/2, y[-1]/2 + 0.1, '$B_\perp$', c='blue')
    
    arc = Arc(center, width, height, angle=rang, theta1=0, theta2=theta2, lw=2)
    ax2.add_patch(arc)
    ax2.set_aspect('equal', adjustable='box')

    for i in range(len(xp-1)):
        xc, yc = position_vector(xp[i], yp[i])
        ax2.plot(xc, yc, lw=2, c='k') 

    
    ax2.text(0+0.1, 0, '$\phi$', c='k')
    ax2.text(xp[0]-0.05, yp[0]-0.1, '$\hat{e_r}$', c='k')
    ax2.text(xp[1]-0.1, yp[1]-0.05, '$\hat{e_\phi}$', c='k')
    
    ax2.set_xlim([-1, 1])
    ax2.set_xticks([])
    ax2.set_ylim([-1, 1])
    ax2.set_yticks([])
    ax2.set_xlabel('X-axis')
    ax2.set_ylabel('Y-axis')
    ax2.set_title("Polar coordinates")
    
    # Second subplot (empty for now or add your content here)
    #### axes
    ax3.axvline(0, c='k', lw=0.25)
    ax3.axhline(0, c='k', lw=0.25)
    ax3.plot([-6, 6], [-2, 2], c='k', lw=0.25)
    ax3.plot([2, -2], [-6, 6], c='k', lw=0.25)

    #### full vector
    ax3.scatter(x[-1], y[-1], s=15, c='blue')
    xc, yc = position_vector(x[-1], y[-1])
    ax3.plot(xc, yc, lw=1.5, c='blue')
    ax3.text(x[-1]/2, y[-1]/2 + 0.1, '$B_\perp$', c='blue')
    
    #### components
    scale31 = 2.8
    xc, yc = position_vector(xpp[0], ypp[0])
    ax3.plot(xc*scale31, yc*scale31, lw=1.5, ls='--', c='b') 
    ax3.scatter(xpp[0]*scale31, ypp[0]*scale31, s=15, c='b')
    
    #### unit vectors
    for i in range(len(xpp-1)):
        xc, yc = position_vector(xpp[i], ypp[i])
        ax3.plot(xc*1.5, yc*1.5, lw=2, c='k') 
    ax3.text(xpp[0]*1.5, ypp[0]*1.5, '$\hat{e_r}$', c='k')
    ax3.text(xpp[1]*1.5, ypp[1]*1.5, '$\hat{e_\phi}$', c='k')

    scale32 = 0.28
    ax3.scatter(xpp[1]*scale32, ypp[1]*scale32, s=15, c='b')
    xc, yc = position_vector(xpp[1], ypp[1])
    ax3.plot(xc*scale32, yc*scale32, lw=2.5, ls='--', c='b') 
    
    #### angle 
    arc = Arc(center, width, height, angle=rang, theta1=0, theta2=theta2, lw=2)
    ax3.add_patch(arc)
    ax3.set_aspect('equal', adjustable='box')

    

    #xc, yc = position_vector(x[i], y[i])
    #ax1.plot(xc, yc, lw=1.25, ls='--', c='blue', alpha=0.6)
    #xc, yc = position_vector(xtwist, ytwist)
   # ax3.plot(xc, yc, lw=2, c='k') 
    
    #ax3.text(0+0.1, 0, '$\phi$', c='k')
    
    ax3.set_xlim([-1, 1])
    ax3.set_xticks([])
    ax3.set_ylim([-1, 1])
    ax3.set_yticks([])
    ax3.set_xlabel('X-axis')
    ax3.set_ylabel('Y-axis')
    ax3.set_title("'Polar'(?) coordinates")

    plt.tight_layout()
    plt.show()


transform = 0

if transform != 0:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # Two subplots side by side

    # First subplot (your original plot goes here)
    ax1.scatter(x, y)
    ax1.axvline(0, c='k', lw=0.25)
    ax1.axhline(0, c='k', lw=0.25)

    for i in range(len(x)):
        xc, yc = position_vector(x[i], y[i])
        ax1.plot(xc, yc, lw=0.5, c='blue')

    ax1.set_xlim([-1, 1])
    ax1.set_ylim([-1, 1])
    ax1.set_title("Original position vectors")

    # Second subplot (empty for now or add your content here)
    ax2.scatter(xr, yr)
    ax2.axvline(0, c='k', lw=0.25)
    ax2.axhline(0, c='k', lw=0.25)

    for i in range(len(x)):
        xc, yc = position_vector(xr[i], yr[i])
        ax2.plot(xc, yc, lw=0.5, c='blue')

    ax2.set_xlim([-1, 1])
    ax2.set_ylim([-1, 1])
    ax2.set_title("Polar coordinate vectors")

    plt.tight_layout()
    plt.show()


