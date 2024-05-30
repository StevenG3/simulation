import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import nakagami

# 定义r的范围
r = np.linspace(0, 5, 1000)

# 定义不同的m值和Ω值
ms = [0.5, 1, 1, 1, 2, 2, 5]
omegas = [1, 1, 2, 3, 1, 2, 1]  # 定义Ω值

# 绘制PDF和CDF的图，横向排列
fig, axs = plt.subplots(1, 2, figsize=(16, 6))

# 绘制PDF
for m, omega in zip(ms, omegas):
    pdf = nakagami.pdf(r, m, scale=np.sqrt(omega))
    axs[0].plot(r, pdf, label=f'm = {m}, Ω = {omega}')

axs[0].set_title('Nakagami-m Distribution PDF')
axs[0].set_xlabel('r')
axs[0].set_ylabel('Probability Density Function (PDF)')
axs[0].set_xlim(0)
axs[0].set_ylim(0)
axs[0].legend()
axs[0].grid(True)

# 绘制CDF
for m, omega in zip(ms, omegas):
    cdf = nakagami.cdf(r, m, scale=np.sqrt(omega))
    axs[1].plot(r, cdf, label=f'm = {m}, Ω = {omega}')

axs[1].set_title('Nakagami-m Distribution CDF')
axs[1].set_xlabel('r')
axs[1].set_ylabel('Cumulative Distribution Function (CDF)')
axs[1].set_xlim(0)
axs[1].set_ylim(0)
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
