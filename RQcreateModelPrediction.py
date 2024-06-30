import matplotlib.pyplot as plt
import numpy as np

results = []
with open('resultsProcess.txt') as file:
    for line in file:
        results.append([(x.split(': ')[0], float(x.split(': ')[1])) for x in line.rstrip().split(',')])

for x in results:
    x.append(x[5][1] / x[6][1])

x_values_red = []
x_values_green = []
y_values_red = []
y_values_green = []
red = []
green = []
errorMargin = 1.5
for x in results:
    if x[7] > errorMargin or x[7] < 1/errorMargin:
        x_values_red.append(x[5][1])
        y_values_red.append(x[6][1])
        red.append(x)
    else:
        x_values_green.append(x[5][1])
        y_values_green.append(x[6][1])
        green.append(x)

red.sort(key=lambda x: x[7])
green.sort(key=lambda x: x[7])

# with open('resultsModelPrediction.txt', 'a') as file:
#     file.write(f"Results for error margin CALCULATE PROBABILITY\n {errorMargin}\n")
#     file.write("Red: \n")
#     for x in red:
#         file.write(f"{x}\n")

#     file.write("\n")
#     file.write("Green: \n")
#     for x in green:
#         file.write(f"{x}\n")

plt.scatter(x_values_red, y_values_red, color='red')
plt.scatter(x_values_green, y_values_green, color='green')
plt.axline((0, 0), slope=1)
plt.axis([0, 1, 0, 1])
plt.xlabel('Modelled time')
plt.ylabel('Actual time')
plt.grid(True)
plt.show()

x_values_green_logged = [np.log10(x) for x in x_values_green]
y_values_green_logged = [np.log10(y) for y in y_values_green]
x_values_red_logged = [np.log10(x) for x in x_values_red]
y_values_red_logged = [np.log10(y) for y in y_values_red]
plt.scatter(x_values_green_logged, y_values_green_logged, color='green')
plt.scatter(x_values_red_logged, y_values_red_logged, color='red')
plt.axline((0, 0), slope=1)
plt.xlabel('Modelled time')
plt.ylabel('Actual time')
plt.grid(True)
plt.show()