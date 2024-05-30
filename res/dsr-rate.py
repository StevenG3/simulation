import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

markers = ['o', 's', '^', 'D']  # circle, square, triangle_up, diamond

# Load the data from the uploaded image
data = {
    "MCS": [0, 1, 2, 3, 4, 5, 6, 7],
    "64": [1.37, 2.35, 6.92, 7.07, 7.16, 7.17, 7.28, 7.29],
    "256": [2.05, 7.54, 8.22, 8.57, 9.02, 9.11, 9.17, 8.95],
    "1024": [2.56, 8.09, 9.76, 10.95, 12.11, 13.2, 13.06, 12.58],
    "2048": [2.65, 8.54, 10.78, 12.07, 14.32, 15.68, 15.44, 12.15],
    "Situ-Based DSR": [2.605, 7.391, 9.30, 9.77, 10.70, 11.12, 11.54, 11.365],
    "DSR":            [ 2.57,  4.52, 6.25, 7.15,  8.95, 10.25,  10.8,   10.6]
}

# 计算增长率
growth_rates = []
for i in range(len(data["Situ-Based DSR"])):
    growth_rate = (data["Situ-Based DSR"][i] - data["DSR"][i]) / data["DSR"][i]
    growth_rates.append(growth_rate)

# 计算平均增长率
average_growth_rate = sum(growth_rates) / len(growth_rates)

print(average_growth_rate)

# Data and DataFrame creation remains the same
df = pd.DataFrame(data)

# Define a font similar to Matlab's default
font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 12}
plt.rc('font', **font)

# Path for the PDF files
rate_vs_mcs_pdf_path = 'rate_vs_mcs.pdf'
relay_udp_vs_mcs_pdf_path = 'dsr_vs_mcs.pdf'

# Create the first PDF for Rate vs MCS
with PdfPages(rate_vs_mcs_pdf_path) as pdf:
    fig, ax = plt.subplots(figsize=(8, 6))
    for idx, column in enumerate(["64", "256", "1024", "2048"]):
        ax.plot(df["MCS"], df[column], marker=markers[idx], label=f'{column}B')
    ax.yaxis.set_ticks_position('both')  # Show ticks on both left and right
    ax.tick_params(axis='y', which='both', direction='in')  # Ticks pointing inwards on the y-axis
    ax.xaxis.set_ticks_position('both')  # Show ticks on both top and bottom
    ax.tick_params(axis='x', which='both', direction='in')  # Ticks pointing inwards on the x-axis

    ax.set_xlabel('MCS')
    ax.set_ylabel('Throughput (Mbps)')
    # ax.set_title('Rate vs MCS for Different Packet Sizes')
    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5)  # Use light gray dashed grid lines
    ax.set_facecolor('white')  # Set background to white to remove gray lines
    pdf.savefig(fig)
    plt.close(fig)

# Create the second PDF for RELAY and UDP
with PdfPages(relay_udp_vs_mcs_pdf_path) as pdf:
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.yaxis.set_ticks_position('both')  # Show ticks on both left and right
    ax.tick_params(axis='y', which='both', direction='in')  # Ticks pointing inwards on the y-axis
    ax.xaxis.set_ticks_position('both')  # Show ticks on both top and bottom
    ax.tick_params(axis='x', which='both', direction='in')  # Ticks pointing inwards on the x-axis

    positions = range(len(df['MCS']))
    width = 0.4
    # ax.plot(df["MCS"], df["RELAY"], marker='o', label='RELAY')
    # ax.plot(df["MCS"], df["UDP"], marker='^', label='UDP')
    # Plotting the bars for RELAY and UDP
    ax.bar([p - width/2 for p in positions], df['Situ-Based DSR'], width=width, color='orange', alpha=0.5, label='Situ-Based DSR', edgecolor='black')
    ax.bar([p + width/2 for p in positions], df['DSR'], width=width, color='green', alpha=0.5, label='DSR', edgecolor='black')
    ax.set_xlabel('MCS')
    ax.set_ylabel('Throughput(Mbps)')
    # ax.set_title('Rate vs MCS for RELAY and UDP')
    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5)  # Use light gray dashed grid lines
    ax.set_facecolor('white')  # Set background to white to remove gray lines
    pdf.savefig(fig)
    plt.close(fig)
