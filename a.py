import numpy as np
from matplotlib import pyplot as plt


N,t = np.loadtxt("log").T

plt.plot(N,t,'.')


fit = np.polyfit(np.log(N), np.log(t), 1)
print(fit)
f = lambda x: np.exp(fit[1]) * x**fit[0]
plt.plot(N,f(N),'--')

print(f(923))

plt.xscale("log")
plt.yscale("log")


plt.show()








