# This script plots the reference particle trajectory in the transverse plane. 

# Dependencies
import read
import plot
import matplotlib.pyplot as plt
import numpy as np
import argparse

# Get path
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Path to g4bl output file")
parser.add_argument("-p", "--plotpath", help="Directory to store plots in", default='/plots/')
args = parser.parse_args()

# Open file and get reference particle
data, label = read.read_trace(args.input)
ref = data[-1]

# Get x, y
x, y, z = ref['x'], ref['y'], ref['z']
px, py, pz = ref['Px'], ref['Py'], ref['Pz']

# Make x_v_z plot
fig, ax = plot.plot_long('x (mm)')
ax.plot(z, x, lw=1)
fig.tight_layout()
#plt.savefig(f'{args.plotpath}/xvz.png')
plt.show()

# Make y_v_z plot
fig, ax = plot.plot_long('y (mm)')
ax.plot(z, y, lw=1)
fig.tight_layout()
#plt.savefig(f'{args.plotpath}/yvz.png')
plt.show()

# Make x_v_y plot
fig, ax = plot.plot_transverse(100)
ax.plot(x, y, lw=1)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Reference particle in transverse plane')
fig.tight_layout()
#plt.savefig(f'{args.plotpath}/xvy.png')
plt.show()

# Make px_v_z plot
fig, ax = plot.plot_long(r'$p_x$ (MeV/c)')
ax.plot(z, px, lw=1)
fig.tight_layout()
#plt.savefig(f'{args.plotpath}/pxvz.png')
plt.show()

# Make py_v_z plot
fig, ax = plot.plot_long(r'$p_y$ (MeV/c)')
ax.plot(z, py, lw=1)
fig.tight_layout()
#plt.savefig(f'{args.plotpath}/pyvz.png')
plt.show()

# Make pz_v_z plot
fig, ax = plot.plot_long(r'$p_z$ (MeV/c)')
ax.plot(z, pz, lw=1)
fig.tight_layout()
#plt.savefig(f'{args.plotpath}/pzvz.png')
plt.show()

# # # Add cut on z
# min_z, max_z = 4200, 4200*1.5
# ref = ref[ref['z'] > min_z]
# ref = ref[ref['z'] < max_z]
# x, y, z = ref['x'], ref['y'], ref['z']

# # Make x_v_z plot
# fig, ax = plot.plot_long('x (mm)')
# ax.plot(z, x, lw=1)
# fig.tight_layout()
# plt.savefig(f'{args.plotpath}/xvz-clipped.png')
# #plt.show()

# # Make y_v_z plot
# fig, ax = plot.plot_long('y (mm)')
# ax.plot(z, y, lw=1)
# fig.tight_layout()
# plt.savefig(f'{args.plotpath}/yvz-clipped.png')
# #plt.show()

# # Make x_v_y plot
# fig, ax = plot.plot_transverse(50)
# ax.plot(x, y, lw=1)
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# if min_z != None and max_z != None:
#     ax.set_title(f'Reference particle in HFOFO: z={min_z} to z={max_z}')
# else:
#     ax.set_title('Reference particle in HFOFO')
# fig.tight_layout()
# plt.savefig(f'{args.plotpath}/xvy-clipped.png')
# #plt.show()

