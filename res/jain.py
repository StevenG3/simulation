import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator

markers = ['o', 's', '^', 'D']  # circle, square, triangle_up, diamond

# Load the data from the uploaded image
data = {
    "Number of Nodes": [2,       4,       6,       8,       10,      12,      14,      16,      18,      20],
    "Proposed":        [0.95321, 0.95997, 0.96565, 0.96777, 0.97565, 0.97722, 0.98301, 0.98547, 0.98880, 0.99546],
    "DCF Broadcast":  [0.97811, 0.97141, 0.96953, 0.96521, 0.94250, 0.92356, 0.91040, 0.90953, 0.90866, 0.90357]
}

# Data and DataFrame creation remains the same

df = pd.DataFrame(data)

# Define a font similar to Matlab's default
font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 12}
plt.rc('font', **font)

# Path for the PDF files
pdf_path = 'jain_vs_nodes.pdf'

# Create the PDF for proposed and DCF broadcast
with PdfPages(pdf_path) as pdf:
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot each data series with different markers
    ax.plot(df['Number of Nodes'], df['DCF Broadcast'], marker='s', linestyle='-', label='DCF Broadcast')
    ax.plot(df['Number of Nodes'], df['Proposed'], marker='o', linestyle='-', label='Proposed')

    ax.yaxis.set_ticks_position('both')  # Show ticks on both left and right
    ax.tick_params(axis='y', which='both', direction='in')  # Ticks pointing inwards on the y-axis
    ax.xaxis.set_ticks_position('both')  # Show ticks on both top and bottom
    ax.tick_params(axis='x', which='both', direction='in')  # Ticks pointing inwards on the x-axis

    # Set ticks and labels
    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Jain\'s Fairness Index')

    # 使用 MaxNLocator 确保 x 轴刻度为整数
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Additional plot settings
    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_facecolor('white')  # Set background to white

    # Save the figure to PDF
    pdf.savefig(fig)
    plt.close(fig)

growth_rates = []
for i in range(len(data["Number of Nodes"])):
    growth_rate = (data["Proposed"][i] - data["DCF Broadcast"][i]) / data["DCF Broadcast"][i]
    growth_rates.append(growth_rate)

# 计算平均增长率
average_growth_rate = sum(growth_rates) / len(growth_rates)

print(f"avg: {average_growth_rate}")