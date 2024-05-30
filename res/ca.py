import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator

markers = ['o', 's', '^', 'D']  # circle, square, triangle_up, diamond

# Load the data from the uploaded image
data = {
    "Number of Nodes": [       4,        8,       12,       16,       20,       24,       28,       32, 
                              36,       40,       44,       48,       52,       56,       60,       64],
    "Shuffle_T":       [0.022760, 0.107845, 0.255464, 0.373095, 0.353335, 0.310560, 0.323346, 0.299285,
                        0.299285, 0.278595, 0.306608, 0.285453, 0.270691, 0.284988, 0.292892, 0.274643],
    "BEB_T":           [0.022179, 0.104775, 0.258329, 0.370584, 0.354381, 0.301726, 0.296263, 0.299745,
                        0.278130, 0.284429, 0.293728, 0.268250, 0.249071, 0.249071, 0.205250, 0.229656],
    "Shuffle_D":       [   0.557,    2.990,    2.990,  355.748,  445.307,  488.033,  482.255,  496.396,
                         498.068,  496.396,  479.670,  500.653,  483.928,  478.910,  461.437,  467.962],
    "BEB_D":           [   1.966,    2.577,    2.577,  323.074,  398.678,  454.871,  459.452,  465.407,
                         468.003,  481.898,  477.928,  466.781,  477.928,  475.943,  461.437,  444.945],
}

# 计算增长率
growth_rates_T = []
for i in range(len(data["Number of Nodes"])):
    growth_rate = (data["Shuffle_T"][i] - data["BEB_T"][i]) / data["BEB_T"][i]
    growth_rates_T.append(growth_rate)

# 计算平均增长率
average_growth_rate_T = sum(growth_rates_T) / len(growth_rates_T)

print(f"NT: {average_growth_rate_T}")

# Data and DataFrame creation remains the same
df = pd.DataFrame(data)

# Define a font similar to Matlab's default
font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 12}
plt.rc('font', **font)

# Path for the PDF files
nt_vs_nodes_pdf_path = 'nt_vs_nodes.pdf'

with PdfPages(nt_vs_nodes_pdf_path) as pdf:
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot each data series with different markers
    ax.plot(df['Number of Nodes'], df['BEB_T'], marker='o', linestyle='-', label='BEB')
    ax.plot(df['Number of Nodes'], df['Shuffle_T'], marker='s', linestyle='-', label='Shuffle')

    ax.yaxis.set_ticks_position('both')  # Show ticks on both left and right
    ax.tick_params(axis='y', which='both', direction='in')  # Ticks pointing inwards on the y-axis
    ax.xaxis.set_ticks_position('both')  # Show ticks on both top and bottom
    ax.tick_params(axis='x', which='both', direction='in')  # Ticks pointing inwards on the x-axis

    # Set ticks and labels
    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Normalized Throughput')

    # 使用 MaxNLocator 确保 x 轴刻度为整数
    # ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Additional plot settings
    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_facecolor('white')  # Set background to white

    # Save the figure to PDF
    pdf.savefig(fig)
    plt.close(fig)

delay_pdf_path = 'delay_vs_nodes.pdf'
with PdfPages(delay_pdf_path) as pdf:
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot each data series with different markers
    ax.plot(df['Number of Nodes'], df['BEB_D'], marker='o', linestyle='-', label='BEB')
    ax.plot(df['Number of Nodes'], df['Shuffle_D'], marker='s', linestyle='-', label='Shuffle')

    ax.yaxis.set_ticks_position('both')  # Show ticks on both left and right
    ax.tick_params(axis='y', which='both', direction='in')  # Ticks pointing inwards on the y-axis
    ax.xaxis.set_ticks_position('both')  # Show ticks on both top and bottom
    ax.tick_params(axis='x', which='both', direction='in')  # Ticks pointing inwards on the x-axis

    # Set ticks and labels
    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Delay (ms)')

    # 使用 MaxNLocator 确保 x 轴刻度为整数
    # ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Additional plot settings
    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_facecolor('white')  # Set background to white

    # Save the figure to PDF
    pdf.savefig(fig)
    plt.close(fig)

growth_rates_D = []
for i in range(len(data["Number of Nodes"])):
    growth_rate = (data["Shuffle_D"][i] - data["BEB_D"][i]) / data["BEB_D"][i]
    growth_rates_D.append(growth_rate)

# 计算平均增长率
average_growth_rate_D = sum(growth_rates_D) / len(growth_rates_D)

print(f"D: {average_growth_rate_D}")