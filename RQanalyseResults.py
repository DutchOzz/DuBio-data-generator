import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as P
import numpy as np

results = [(-596.99512, 1), (-418.37001, 2), (-384.849875, 3), (-351.98123, 4), (-290.35629, 5), (-341.72219, 6), (-346.16906, 7), (-322.075805, 8), (-306.607865, 9), (-294.26586, 10)]
# maxMean = 320.579735
lowestResult = 260

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
plt.plot(x_values, y_values, label="logged results")
polynomial = P.fit(x_values, y_values, 1) # 1 is the degree of the polynomial
fx, fy = polynomial.linspace(100)
print(fx)
print(fy)
plt.plot(fx, fy, label = "1st degree")
plt.legend()
plt.show()