import connection as c
import queryFunctions as qf
import RQcreateFunction as rqf
import matplotlib.pyplot as plt
import statistics as stat

schemaName = "testSchema"

rqf.setupTables(2)
rqf.addRows(2, 10, 10, 1, 2520)
rqf.setupDictionary(10, 10)

results = []
conn = c.connect()
for i in range(200):
    results.append(rqf.runQuery(conn, qf.getCachedProbabilities, qf.calculateProbabilities, i))
conn.commit()
c.close(conn)

print("Mean: ", stat.mean(results))
print("Standard Deviation: ", stat.stdev(results))
plt.hist(results, bins=50)
plt.xlabel('Milliseconds with - without cache')
plt.ylabel('Amount of Runs')
plt.title('Function Plot')
plt.grid(True)
plt.show()