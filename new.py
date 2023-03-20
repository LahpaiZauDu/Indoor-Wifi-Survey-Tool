import numpy as np
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging

# Generate some random data
x = np.random.rand(50)
y = np.random.rand(50)
z = np.sin(x * 2 * np.pi) * np.cos(y * 2 * np.pi)

# Fit the kriging model to the data
OK = OrdinaryKriging(x, y, z)

# Define the grid for interpolation
gridx = np.linspace(0, 1, 100)
gridy = np.linspace(0, 1, 100)

# Interpolate the grid using the kriging model
z_pred, ss = OK.execute('grid', gridx, gridy)

# Plot the input data and interpolated surface
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))
ax1.scatter(x, y, c=z, cmap='viridis')
ax1.set_title('Input Data')
ax2.contourf(gridx, gridy, z_pred, cmap='viridis')
ax2.scatter(x, y, c=z, cmap='viridis')
ax2.set_title('Interpolated Surface')
plt.show()
