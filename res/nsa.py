# 同时生成AAR.xlsx和AAR.pdf
# Uasge: python script_name.py --input nodes_stats.csv --output_prefix AAR_output

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages

import argparse

# Define and parse command-line arguments
parser = argparse.ArgumentParser(description='Generate AAR from node stats and export to both Excel and PDF.')
parser.add_argument('--input', type=str, help='Input CSV file containing node stats')
parser.add_argument('--output_prefix', type=str, help='Prefix for the output files, without extension')
args = parser.parse_args()

# Define a font similar to Matlab's default
font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 12}
plt.rc('font', **font)

# Load and prepare the data
df = pd.read_csv(args.input, delimiter=' ', header=None)
df.columns = ['time', 'label_node', 'node', 'label_has', 'label_awared', 'x', 'label_nodes']
df = df[['time', 'node', 'x']]

# Initialize perceptions for each node at time 0, each node perceives only itself
node_ids = df['node'].unique()
perceptions = {node_id: 1 for node_id in node_ids}

# To hold average perception ratios for each timestamp
avg_perception_ratios = []
timestamps = sorted(df['time'].unique())

# List to hold data for Excel output
excel_data = []

for time in timestamps:
    if time == 0:
        num_nodes = len(node_ids)
        avg_perception_ratio = num_nodes / (num_nodes ** 2)
    else:
        current_perceptions = perceptions.copy()
        current_data = df[df['time'] == time]

        for _, row in current_data.iterrows():
            current_perceptions[row['node']] = row['x']

        total_perceptions = sum(current_perceptions.values())
        avg_perception_ratio = total_perceptions / (len(node_ids) ** 2)
        perceptions.update(current_perceptions)

    avg_perception_ratios.append(avg_perception_ratio)
    excel_data.append([time, avg_perception_ratio])
    print(f"Timestamp: {time}, Average Perception Ratio: {avg_perception_ratio:.4f}")

# Create DataFrame for Excel
excel_df = pd.DataFrame(excel_data, columns=['Time', 'AAR'])

# Save DataFrame to Excel
excel_output = f"{args.output_prefix}.xlsx"
excel_df.to_excel(excel_output, index=False)

# Path for the PDF files
pdf_output = f"{args.output_prefix}.pdf"

# Create the first PDF for AAR
with PdfPages(pdf_output) as pdf:
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(timestamps, avg_perception_ratios, marker='o')

    # Set labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Average Awareness Ratio')

    # Customize ticks on both axes
    ax.yaxis.set_ticks_position('both')  # Show ticks on both left and right
    ax.tick_params(axis='y', which='both', direction='in')  # Ticks pointing inwards on the y-axis
    ax.xaxis.set_ticks_position('both')  # Show ticks on both top and bottom
    ax.tick_params(axis='x', which='both', direction='in')  # Ticks pointing inwards on the x-axis

    # ax.legend() # 线条说明
    ax.grid(True, linestyle='--', linewidth=0.5)  # Use light gray dashed grid lines
    ax.set_facecolor('white')  # Set background to white to remove gray lines

    pdf.savefig(fig)
    # Close the plot
    plt.close(fig)
