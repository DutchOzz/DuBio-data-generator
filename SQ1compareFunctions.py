import numpy as np
from numpy.polynomial import Polynomial as P
import matplotlib.pyplot as plt

functionNames = ["Calculate Probabilities", "Select Query", "Recalculate Probabilities"]
functions = [
]
#calculateProbabilities
# 250.926592 + 199.84242709 x
# 252.522323 + 199.320003 x
# 253.115369 + 200.61535773 x

# official functions
## 240.54485079 + 222.83946281 x - 28.27162552 x**2
# 230.9305943 + 222.83946281 x

#SELECT query
# 100 iterations
# -0.09766424 - 0.07913497 x + 0.02910906 x**2
# -0.0877652 - 0.07913497 x

# 50 iterations
# -0.11027633 - 0.07019941 x + 0.06038855 x**2
# -0.0893252 - 0.07019941 x
# -0.10701187 - 0.08840129 x + 0.02625498 x**2
# -0.097903 - 0.08840129 x

#Recalculate Probabilities


Rowcount = 2520
weights = [1, 1, 1, 1, 1]

assert len(functionNames) == len(functions) == len(weights)

# calculate the weighted sum of all functions
def weighted_sum(x):
    return sum([weights[i] * functions[i](x) for i in range(len(functions))])
print("Weighted sum: ", weighted_sum(Rowcount))

# plot all functions
for i in range(len(functions)):
    x = [Rowcount * i for i in range(len(functions)) + 1]
    y = functions[i](x)
    plt.plot(x, y, label=functionNames[i])

plt.xlabel('Amount of rows')
plt.ylabel('Milliseconds')
plt.title('Function Plot')
plt.grid(True)
plt.legend()
plt.show()

