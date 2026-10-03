import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
rng = np.random.default_rng(42)

n = 500
mu, sigma = 0, 1

sample = rng.normal(loc=mu, scale=sigma, size=n)

x = np.linspace(sample.min(), sample.max(), 300)
plt.hist(sample, bins=30, density=True, alpha=0.6, label="Выборка")
plt.plot(x, stats.norm.pdf(x, mu, sigma), "r-", lw=2, label="Теоретическая плотность")
plt.title(f"N({mu}, {sigma}²), n = {n}")
plt.legend()
plt.show()


