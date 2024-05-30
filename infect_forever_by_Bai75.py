import numpy as np
import matplotlib.pyplot as plt

# Define the parameters for the equation
n = 128  # Assume n=1 for demonstration, adjust based on actual requirement
f = 4    # Assume f=0.5 for demonstration, adjust based on actual requirement

# Define the range of r
r = np.linspace(0, 10, 400)

# Calculate Y_r
Y_r = 1 / (1 + n * np.exp(-f * r))

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(r, Y_r, label='Y_r = 1 / (1 + n * exp(-f * r))')
plt.title('Plot of Y_r against r')
plt.xlabel('r')
plt.ylabel('Y_r')
plt.legend()
plt.grid(True)
plt.show()

