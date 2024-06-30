import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as P
import numpy as np

results = [(224.438275, 2), (225.762995, 3), (227.0008, 4), (224.700245, 5), (225.007865, 6), (225.098195, 7), (227.50953, 8), (225.92083499999998, 9), (224.782985, 10), (224.488175, 11), (224.59636, 12), (223.98425, 13), (224.489595, 14), (225.1247, 15), (225.25688, 16), (224.305195, 17), (226.682865, 18), (229.38492, 19), (230.87871, 20)]
lowestResult = 0

x_values = [results[i][1] for i in range(len(results))]
y_values = [results[i][0] for i in range(len(results))]
y_values_minussed = [y_values[i] - lowestResult for i in range(len(y_values))]
y_values_logged = [np.log10(y_values_minussed[i]) for i in range(len(y_values))]
x_values_logged = [np.log10(x_values[i]) for i in range(len(x_values))]

# plt.plot(x_values, y_values, label="results")
# plt.plot(x_values, y_values_minussed, label="minussed results")
# plt.legend()
# plt.show()

print(y_values)
print(x_values)
print(y_values_minussed)
print(x_values_logged)
print(y_values_logged)
plt.plot(x_values, y_values)
plt.xlabel("Column amount")
plt.ylabel("Milliseconds")
# plt.plot(x_values_logged, y_values_logged, label="logged results")
# polynomial = P.fit(x_values, y_values, 1) # 1 is the degree of the polynomial
# fx, fy = polynomial.linspace(100)
# print(fx)
# print(fy)
# plt.plot(fx, fy, label = "1st degree")
plt.xticks(range(0,21,2))
plt.legend()
plt.show()