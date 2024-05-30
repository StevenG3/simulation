import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rcParams

# 修改图中的默认字体
plt.rc('font',family='Times New Roman') 
# 修改公式中默认字体

rcParams['mathtext.default'] = 'regular'

# 构建数据
data = {
    'n': [64, 128, 256, 512, 1024, 64, 128, 256, 512, 1024, 64, 128, 256, 512, 1024, 64, 128, 256, 512, 1024],
    'N_f': [64, 128, 256, 512, 1024, 64, 128, 256, 512, 1024, 64, 128, 256, 512, 1024, 64, 128, 256, 512, 1024],
    'AMR': [7.59, 13.51, 25.21, 53.31, 106.83, 7.59, 13.51, 25.21, 53.31, 106.83, 7.59, 13.51, 25.21, 53.31, 106.83, 7.59, 13.51, 25.21, 53.31, 106.83],
    'SRB': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'RDN': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    'ABD': [0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139, 0.0139]
}

# 创建 DataFrame
df = pd.DataFrame(data)

# 修改绘图设置为一行两张图，总共三行
fig, axs = plt.subplots(3, 2, figsize=(15, 15))  # 3 rows, 2 columns

# 绘制 N_f 图
axs[0, 0].plot(df['n'], df['N_f'], marker='o')
axs[0, 0].set_title('N_f vs n')
axs[0, 0].set_xlabel('n (Number of Nodes)')
axs[0, 0].set_ylabel('N_f')
axs[0, 0].grid(True)

# 绘制 AMR 图
axs[0, 1].plot(df['n'], df['AMR'], marker='o', color='red')
axs[0, 1].set_title('AMR vs n')
axs[0, 1].set_xlabel('n (Number of Nodes)')
axs[0, 1].set_ylabel('AMR')
axs[0, 1].grid(True)

# 绘制 SRB 图
axs[1, 0].plot(df['n'], df['SRB'], marker='o', color='green')
axs[1, 0].set_title('SRB vs n')
axs[1, 0].set_xlabel('n (Number of Nodes)')
axs[1, 0].set_ylabel('SRB')
axs[1, 0].set_ylim(-0.2, 1)  # 设置纵轴范围为 0 到 1
axs[1, 0].grid(True)

# 绘制 RDN 图
axs[1, 1].plot(df['n'], df['RDN'], marker='o', color='purple')
axs[1, 1].set_title('RDN vs n')
axs[1, 1].set_xlabel('n (Number of Nodes)')
axs[1, 1].set_ylabel('RDN')
axs[1, 1].set_ylim(0, 1.2)  # 设置纵轴范围为 0 到 1
axs[1, 1].grid(True)

# 绘制 ABD 图
axs[2, 0].plot(df['n'], df['ABD'], marker='o', color='brown')
axs[2, 0].set_title('ABD vs n')
axs[2, 0].set_xlabel('n (Number of Nodes)')
axs[2, 0].set_ylabel('ABD')
axs[2, 0].grid(True)

# 第六个位置（2, 1）没有图表，隐藏该坐标轴
axs[2, 1].axis('off')

plt.tight_layout()

# 使用 PdfPages 导出到PDF
with PdfPages('example.pdf') as export_pdf:
    export_pdf.savefig(fig)
    plt.close()

# 显示图表
plt.show()
