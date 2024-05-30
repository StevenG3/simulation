import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams

# 修改图中的默认字体
plt.rc('font',family='Times New Roman') 
# 修改公式中默认字体

rcParams['mathtext.default'] = 'regular'

# Data for plotting
# Assuming the values are roughly similar to the ones in the provided image
stations = np.array([2, 3, 4, 5, 10, 20])
dcf = np.array([0.91, 0.90, 0.91, 0.92, 0.93, 0.96])
our_method = np.array([0.97, 0.97, 0.98, 0.97, 0.98, 0.99])

# Adjusting the font size to 22 for all text in the plot
plt.rc('font', family='Times New Roman', size=22)  # Set the global font size

# Plot the data
fig, ax = plt.subplots(figsize=(8, 6))  # 8:6 is equivalent to 4:3 aspect ratio

ax.plot(stations, dcf, 'k*-', label='802.11 DCF')
ax.plot(stations, our_method, 'r^-', label='Our')

# Adding scatter plots to make the data points more visible
ax.scatter(stations, dcf, color='k')
ax.scatter(stations, our_method, color='r')

# Set labels with updated font size
ax.set_xlabel('Number of stations')
ax.set_ylabel("Jain's fairness index")
ax.set_title("Jain's fairness index comparison")

# Update legend with larger font
ax.legend(loc='center right', fontsize='large')

# Set axis limits
ax.set_xlim(2, 20)
ax.set_ylim(0.4, 1.0)

# Add borders/spines on the top and right sides
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)

# Adjust layout to prevent clipping of ylabel and legend
fig.tight_layout()

# Save the figure to a PDF file
pdf_path = 'fairness_index_comparison.pdf'
plt.savefig(pdf_path)

# Show the plot
plt.show()

# Return the path to the saved PDF file
pdf_path