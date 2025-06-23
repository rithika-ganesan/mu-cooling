#######################

import numpy as np
import matplotlib.pyplot as plt

#######################

L = 0.200 #m

mu_0 = 1.25663706127e-6 # T * m / A = T * (1000 mm) / A
I = 100 #A/mm^2
R = 0.4 #m

#######################

z = np.linspace(-5, 5, 400)

def B(z):
    return mu_0 * I * 0.5 * R**2 * (R**2 + z**2)**(-1.5)

Bz = B(z)

#######################

plt.plot(z*1000, Bz, lw=1, c='k')
plt.axvline(-0.1*1000, ls='--', lw=0.5)
plt.axvline(0.1*1000, ls='--', lw=0.5)
plt.xlabel('z (mm)')
plt.ylabel('B (T)')
plt.show()
