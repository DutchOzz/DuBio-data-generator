import matplotlib.pyplot as plt
import numpy as np

results = []
with open('RQcompareRandomVariables.txt') as file:
    for line in file:
        results.append([(x.split('=')[0], float(x.split('=')[1])) for x in line.rstrip().split(',')])

x_a = [x[0][1] for x in results]
x_d = [x[1][1] for x in results]
x_r = [x[2][1] for x in results]
#correct for mistake in RQcompareRandomVariables.py
x_calProb = [x[3][1]*-1 for x in results]
x_updCache = [x[4][1]*-1 for x in results]
y = [x[5][1] for x in results]

x_a_logged = [np.log10(x) for x in x_a]
x_d_logged = [np.log10(x) for x in x_d]
x_r_logged = [np.log10(x) for x in x_r]
x_calProb_logged = [np.log10(x) for x in x_calProb]
x_updCache_logged = [np.log10(x*-1) for x in x_updCache]
y_logged = [np.log10(z)*-1 for z in y]

# plt.scatter(x_a, y, color='red', label='AOPPV')
plt.scatter(x_d_logged, y, color='green', label='Dictionary size')
plt.scatter(x_r_logged, y, color='blue', label='Row count')
plt.xlabel('Logged execution time')
plt.ylabel('Ratio U/R')
plt.grid(True)
plt.legend()
plt.show()

plt.scatter(x_updCache, y, color='red', label='Update cache')
plt.scatter(x_calProb, y, color='green', label='Retrieve probability')
plt.xlabel('Execution time (ms)')
plt.ylabel('Ratio U/R')
plt.grid(True)
plt.legend()
plt.show()

plt.scatter(x_updCache_logged, y, color='red', label='Update cache')
plt.scatter(x_calProb_logged, y, color='green', label='Retrieve probability')
plt.xlabel('Logged execution time')
plt.ylabel('Ratio U/R')
plt.grid(True)
plt.legend()
plt.show()
