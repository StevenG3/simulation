import numpy as np
import matplotlib.pyplot as plt

# Define a font similar to Matlab's default
font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 12}
plt.rc('font', **font)

# Define the range for the number of nodes
nodes = np.arange(1, 101, 8)

# Define the throughput as an exponentially decreasing function of the number of nodes
throughput = 1000 * np.exp(-0.05 * nodes)

# Plot the curve
fig, ax = plt.subplots(figsize=(10, 6))
# plt.plot(nodes, throughput, label='Throughput', color='blue', linestyle='-', marker='o')
ax.plot(nodes, throughput, color='blue', linestyle='-')
ax.set_title('Throughput vs. Number of Nodes')
ax.set_xlabel('Number of Nodes')
ax.set_ylabel('Throughput')
# Hide ticks and labels
ax.xaxis.set_major_locator(plt.NullLocator())
ax.yaxis.set_major_locator(plt.NullLocator())
# ax.xaxis.set_ticks([])
# ax.yaxis.set_ticks([])
# ax.xaxis.set_ticklabels([])
# ax.yaxis.set_ticklabels([])
# fig.xlabel('Number of Nodes')
# fig.ylabel('Throughput')
# fig.title('Throughput vs. Number of Nodes')
# plt.legend()
# plt.grid(True)
# Save the plot as a JPG file
plt.savefig('throughput_vs_nodes_ppt.jpg', format='jpg')
plt.show()
