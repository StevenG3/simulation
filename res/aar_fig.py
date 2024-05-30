import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Define a font similar to Matlab's default
font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 12}
plt.rc('font', **font)

# 读取Excel文件
# df1 = pd.read_excel('AAR16.xlsx')
# df2 = pd.read_excel('AAR32.xlsx')
# df3 = pd.read_excel('AAR64.xlsx')

# Paths of the Excel files
excel_files = {
	'16': 'AAR_n16_d1600_v8.xlsx',
    '32': 'AAR_n32_d1600_v8.xlsx',
    '64': 'AAR_n64_d1600_v8.xlsx',
    # '128': 'AAR_n128_d400_v0.xlsx',
}

aar_pdf_path = 'aar_d1600_v8.pdf'

# Read the data from Excel files
data_frames = {key: pd.read_excel(value) for key, value in excel_files.items()}

# Create the first PDF for Rate vs MCS
with PdfPages(aar_pdf_path) as pdf:
    # 假设每个文件都有两列，'Time' 和 'AAR'
    # 画图
	fig, ax = plt.subplots(figsize=(8, 6))

	# ax.plot(df1['Time'], df1['AAR'], marker='o', color='red', label='16')
	# ax.plot(df2['Time'], df2['AAR'], marker='^', color='blue', label='32')
	# ax.plot(df3['Time'], df3['AAR'], marker='s', color='green', label='64')
	# ax.plot(df1['Time'], df1['AAR'], color='red', label='16')
	# ax.plot(df2['Time'], df2['AAR'], color='blue', label='32')
	# ax.plot(df3['Time'], df3['AAR'], color='green', label='64')

    # Plot data from each Excel file
	for key, df in data_frames.items():
		ax.plot(df['Time'], df['AAR'], label=key)

	ax.yaxis.set_ticks_position('both')  # Show ticks on both left and right
	ax.tick_params(axis='y', which='both', direction='in')  # Ticks pointing inwards on the y-axis
	ax.xaxis.set_ticks_position('both')  # Show ticks on both top and bottom
	ax.tick_params(axis='x', which='both', direction='in')  # Ticks pointing inwards on the x-axis

	ax.set_xlabel('Time')
	ax.set_ylabel('Average Awareness Ratio')
	ax.legend()
	ax.grid(True, linestyle='--', linewidth=0.5)  # Use light gray dashed grid lines
	ax.set_facecolor('white')  # Set background to white to remove gray lines
	pdf.savefig(fig)
	plt.close(fig)

# # 添加图例
# plt.legend()

# # 添加标题和轴标签
# plt.xlabel('Time')
# plt.ylabel('Average Awareness Ratio')

# # 显示图表
# plt.show()
