import numpy as np
from matplotlib import pyplot as plt


###########################################  BUILD ADJ  ###########################################
"""
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
"""

#############################################  KRYLOV  ############################################
"""
# 20 t_steps
data = np.loadtxt("ts_tEv.txt").T
data = data[:,data[1]==20]
plt.plot(data[0], data[2], '.', label="t_steps=20")


# 200 t_steps
data = np.loadtxt("ts_tEv.txt").T
data = data[:,data[1]==200]
plt.plot(data[0], data[2], '.', label="t_steps=200")

plt.xlabel("N")
plt.ylabel("t [s]")

#plt.xscale("log")
plt.yscale("log")

plt.legend()
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



#############################################  KRYLOV AGAIN  ############################################

# linear time steps
data = np.loadtxt("ts_lin.txt").T
data = data[:,data[1]==10000]
plt.plot(data[0], data[2], '.', label="lin")


# log time steps
data = np.loadtxt("ts_log.txt").T
data = data[:,data[1]==10000]
plt.plot(data[0], data[2], '.', label="log")

plt.xlabel("N")
plt.ylabel("t [s]")

#plt.xscale("log")
plt.yscale("log")

plt.legend()
plt.show()





