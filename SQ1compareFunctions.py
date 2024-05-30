import numpy as np
from numpy.polynomial import Polynomial as P
import matplotlib.pyplot as plt

functionNames = ["Calculate Probabilities", "Select Query", "Recalculate Probabilities", "Inserting 1000 rows into table"]
functions = [
    lambda x : 0.0178 * x,
    lambda x : -0.0000075 * x,
    lambda x : -0.03 * x,
    lambda x : 0.06
]

# calculateProbabilities
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
# -417.60819491 - 373.07185966 x + 26.38249946 x**2
# -408.6363685 - 373.07185966 x

# inserting 10 rows into table
# 0.03742775 - 0.00030342 x + 0.00049857 x**2
# 0.0375973 - 0.00030342 x

# inserting 1000 rows into table
# -0.05918668 - 0.00492272 x - 0.01592778 x**2
# -0.0646032 - 0.00492272 x
Rowcount = 2520
maxRowcountInFunction = 100000
weights = [0.2, 0.5, 0.1, 0.2]

assert len(functionNames) == len(functions) == len(weights)

# calculate the weighted sum of all functions
def weighted_sum(x):
    return sum([weights[i] * functions[i](x) for i in range(len(functions))])
print("Weighted sum: ", weighted_sum(Rowcount))

# plot all functions
x = [Rowcount * i for i in range(maxRowcountInFunction // Rowcount)]
for i in range(len(functions)):
    y = [functions[i](count) for count in x]
    plt.plot(x, y, label=functionNames[i])

plt.xlabel('Amount of rows')
plt.ylabel('Milliseconds')
plt.title('Function Plot')
plt.grid(True)
plt.legend()
plt.show()

