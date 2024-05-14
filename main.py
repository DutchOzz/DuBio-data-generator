import connection
import tableFunctions
import tableDataFunctions
import dictFunctions
import bddFunctions

conn = connection.connect()

# tableFunctions.drop_table(conn, "testSchema", "drives")
# tableFunctions.create_table(conn, "testSchema", "drives")
# tableFunctions.add_column(conn, "testSchema", "drives", "probability", "FLOAT")
# tableFunctions.drop_column(conn, "testSchema", "drives", "probability")
# tableDataFunctions.insert_data(conn, "testSchema", "drives", ["id", "person", "color", "car", "_sentence", "probability"], [["1", "'huhih'", "100", "25", "Bdd('A = 1')", "0.5"]])
# dictFunctions.dropDictionary(conn, "testSchema")
# dictFunctions.createDictionary(conn, "testSchema")
# dictFunctions.addDictionaryEntries(conn, "testSchema", 3, 3)

for i in range(1000):
    bddFunctions.generateRandDictValue(100000)
conn.commit()

connection.close(conn)