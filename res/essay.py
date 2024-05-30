import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages

# 修改图中的默认字体
plt.rc('font',family='Times New Roman') 
# 修改公式中默认字体

rcParams['mathtext.default'] = 'regular'

# 假设数据是这样的，您需要替换为您的实际数据
stations = np.array([50, 100, 150, 200])
flooding = np.array([20, 40, 60, 80])
self_pruning = np.array([10, 20, 30, 40])
sba = np.array([5, 10, 15, 20])
e_sba = np.array([3, 6, 9, 12])
it_sba = np.array([1, 2, 3, 4])

# 开始绘图
fig, ax = plt.subplots(figsize=(10, 6))

# 设置横纵坐标轴等长
ax.set_aspect('equal', adjustable='datalim')
ax.plot(stations, stations)  # 这行用于设置纵轴的比例

# 绘制每一条线，并添加标记和标签
ax.plot(stations, flooding, marker='o', linestyle='-', color='red', label='Flooding')
ax.plot(stations, self_pruning, marker='s', linestyle='-', color='blue', label='Self-pruning')
ax.plot(stations, sba, marker='D', linestyle='-', color='purple', label='SBA')
ax.plot(stations, e_sba, marker='^', linestyle='-', color='magenta', label='E-SBA')
ax.plot(stations, it_sba, marker='v', linestyle='-', color='green', label='IT-SBA')

# 添加标题和坐标轴标签
ax.set_title('Number of forwarding stations vs. Number of stations')
ax.set_xlabel('Number of stations')
ax.set_ylabel('Number of forwarding stations')

# 添加图例
ax.legend()

# 显示网格
ax.grid(True)

# 使用 PdfPages 导出到PDF
with PdfPages('example.pdf') as export_pdf:
    export_pdf.savefig(fig)
    plt.close()

# 显示图表
plt.show()
