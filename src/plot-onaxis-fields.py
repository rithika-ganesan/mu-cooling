import argparse
import glob
import re
from read import read_files
import matplotlib.pyplot as plt

# Parser set-up
parser = argparse.ArgumentParser()
parser.add_argument("filepaths", help="Path to root file(s)")
args = parser.parse_args()

# Read
paths = sorted(glob.glob(f"{args.filepaths}"))
paths, files = read_files(paths)

# Main

fig, ax = plt.subplots()
ax.set_title(r'$B_z$ for different solenoid lengths')

for key in files:
    lbl = re.search(r'(\d+)\.root$', key).group(1)
    if lbl == "5000":
        ref = files[key][-1]
        z, bz = ref['z'], ref['Bz']
        ax.plot(z, bz, label=f'{lbl}')

ax.set_xlim([-10000, 10000])
ax.set_ylim([0, 0.5])
ax.legend(title='Solenoid length (mm)')
fig.tight_layout()
plt.savefig('plots/sol-length-5000-zoom.png', dpi=300)
plt.show()
