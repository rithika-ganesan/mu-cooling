from sympy import symbols, cos, sin, integrate
from sympy.physics.mechanics import *
from sympy import pi

# Set up a reference frame:
N = ReferenceFrame('N')

# Declaring some symbols:
# R -> radius of the loop
# e -> electric charge
# I -> current in the loop
R, I, e = symbols('R I e')

# Position vector for the particle
x, y, z = symbols('x y z')
P = x * N.x + y * N.y + z * N.z

print(P)

# Position vector for the current element
phi = symbols('phi')
I = R * cos(phi) * N.x + R * sin(phi) * N.y + 0 * N.z

print(I)

# Current vector 
dl1, dl2 = symbols('dl1 dl2')
dl = -R * sin(phi) * N.x + R * cos(phi) * N.y 

print(dl)

# Vector from current element to particle
r = P - I
r_mag = r.magnitude()

r_hat = r / r_mag

print(r_hat)

# Inside the integral:
integrand = dl.cross(r_hat) / r_mag**2
i_x, i_y, i_z = integrand.dot(N.x), integrand.dot(N.y), integrand.dot(N.z)

print(i_z)

#b_z = integrate(i_z, (phi, 0, 2*pi))

#print('B')
#print(b_z)





