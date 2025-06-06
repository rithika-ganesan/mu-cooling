import numpy as np
import matplotlib.pyplot as plt

x = np.array([+0.5, -0.3, -0.6, +0.9])
y = np.array([+0.8, +0.2, -0.2, -0.3])

x_ = np.array([+0.5, -0.5, -0.5, +0.5])
y_ = np.array([+0.5, +0.5, -0.5, -0.5])

r = np.sqrt(x**2 + y**2)
correct_phi = np.array([0.25*np.pi, 0.75*np.pi, 1.25*np.pi, 1.75*np.pi])

b = np.array([0, 0.5*np.pi, np.pi, 1.5*np.pi])
a = np.array([1, -1, 1, -1])
#phi = a*np.arctan(y / x) + b

phi = np.arctan2(y, x)

#signs = list(zip(np.sign(x).astype(int), np.sign(y).astype(int)))

#sign = np.sign(x[1])
#print(sign, type(sign))

xr = r * np.cos(phi)
yr = r * np.sin(phi)

def position_vector(x, y):
    xc = [0.0, x]
    yc = [0.0, y]
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
plotswitch = 1

if plotswitch != 0:
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


