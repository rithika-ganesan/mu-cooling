from read import read_trace
from analyse import *
from plot import *

path1 = '../output/solshapel2000.root'
path2 = '../other/ascii/channels/matching/src/solenoids-2.root'
path3 = '../other/ascii/channels/matching/src/solenoids-3.root'
path2p5 = '../other/ascii/channels/matching/src/solenoids-*.root'

path = path1

data, labels = read_trace(path)
print(data.keys())

data = data[-1]

df = get_polar_coordinates(data)
df = get_Bt(df)

rx = np.array([0.4])
ry = np.array([0.3])
r = vecnorm([rx, ry])
phi = np.arctan2(ry, rx)

Vx = np.array([+0.5, -0.3, -0.8, +0.5])
Vy = np.array([+0.5, +0.4, -0.6, -0.5])
phiV = np.arctan2(Vy, Vx)
rV = vecnorm([Vx, Vy])

r = r[0]
phi = phi[0]

Vr = rV * np.cos(phi - phiV)
Vphi = rV * np.sin(phi - phiV)

print(Vr, Vphi)

fig, ax = plot_transverse(1.2, ticks=None)
ax = add_vector(ax, x=rx[0], y=ry[0], label='Position vector')
ax = add_vector(ax, x=Vx[0], y=Vy[0], label='B0', clr='tab:orange')
ax.legend()
fig.tight_layout()
plt.show()


