import numpy as np
from matplotlib import pyplot as plt


###########################################  BUILD ADJ  ###########################################

#  --------------------  stupid  --------------------  #
nP, tP = np.loadtxt("t2.txt").T

plt.plot(nP, tP, '.', c='black', label="no hash")

cut = -9
fit = np.polyfit(nP[cut:], np.log(tP[cut:]), 1)

x = np.arange(nP[cut], nP[-1], 0.1)
y = np.exp( fit[0]*x + fit[1])
plt.plot(x, y, '--', c='black')

print("stupid:  time ~ %.2e exp( %.2f n ) seconds" % (np.exp(fit[1]), fit[0]))

#  --------------------  hash  --------------------  #

nN, tN = np.loadtxt("t3.txt").T

plt.plot(nN, tN, '+', c='red', label="hash")

cut = -9
fit = np.polyfit(nN[cut:], np.log(tN[cut:]), 1)

x = np.arange(nN[cut], nN[-1], 0.1)
y = np.exp( fit[0]*x + fit[1])
plt.plot(x, y, '--', c='red')

print("hash:  time ~ %.2e exp( %.2f n ) seconds" % (np.exp(fit[1]), fit[0]))


#plt.title("time ~ %.2e exp( %.2f n ) seconds" % (np.exp(fit[1]), fit[0]))

plt.xlabel("N")
plt.ylabel("time [s]")

plt.yscale("log")

plt.legend()
plt.show()


#############################################  KRYLOV  ############################################
"""
# 100 t_steps
data = np.loadtxt("ts_tEv.txt").T
data = data[:,data[1]==100]
plt.plot(data[0], data[2], '.', label="t_steps=100")


# 1000 t_steps
data = np.loadtxt("log").T
data = data[:,data[1]==1000]
plt.plot(data[0], data[2], '.', label="t_steps=100")

plt.xlabel("N")
plt.ylabel("t [s]")

#plt.xscale("log")
plt.yscale("log")

plt.show()
"""


###############################################  ED  ##############################################
"""

# 100 t_steps
data = np.loadtxt("ts_ED.txt").T
plt.plot(data[0], data[1], '.', label="t_steps=100")

plt.xlabel("N")
plt.ylabel("t [s]")

#plt.xscale("log")
plt.yscale("log")

plt.show()

"""








