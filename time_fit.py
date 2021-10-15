import numpy as np
from matplotlib import pyplot as plt

#  --------------------  Python  --------------------  #
nP, tP = np.loadtxt("a.txt").T

plt.plot(nP, tP, '.', c='black', label="Python")

cut = -9
fit = np.polyfit(nP[cut:], np.log(tP[cut:]), 1)

x = np.arange(nP[cut], nP[-1], 0.1)
y = np.exp( fit[0]*x + fit[1])
plt.plot(x, y, '--', c='black')

print("Python:  time ~ %.2e exp( %.2f n ) seconds" % (np.exp(fit[1]), fit[0]))

#  --------------------  Python  --------------------  #

nN, tN = np.loadtxt("b.txt").T

plt.plot(nN, tN, '+', c='red', label="Numba")

cut = -9
fit = np.polyfit(nN[cut:], np.log(tN[cut:]), 1)

x = np.arange(nN[cut], nN[-1], 0.1)
y = np.exp( fit[0]*x + fit[1])
plt.plot(x, y, '--', c='red')

print("Numba:  time ~ %.2e exp( %.2f n ) seconds" % (np.exp(fit[1]), fit[0]))


#plt.title("time ~ %.2e exp( %.2f n ) seconds" % (np.exp(fit[1]), fit[0]))



plt.xlabel("n")
plt.ylabel("time")

plt.yscale("log")

plt.legend()
plt.show()

