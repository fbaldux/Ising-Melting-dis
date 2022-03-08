import numpy as np
from matplotlib import pyplot as plt

Tin=1e-1
Tfin=1e3

ts = 2**np.arange( 0, np.log2(Tfin/Tin) ) * Tin


for i in range(len(ts)):
    x = ts[i] * np.linspace(1,2,10)
    plt.plot(x, np.sqrt(x), '.')#, c='black')

plt.xscale('log')
plt.yscale('log')
plt.show()