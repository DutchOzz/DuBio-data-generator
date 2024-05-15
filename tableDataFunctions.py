import bddFunctions

# insert row into a table
def insertRow(conn, schemaName, tableName, columnNames, data):
    cur = conn.cursor()

    insert_data_query = """
        insert into """ + schemaName + "." + tableName + """ (""" + ", ".join(columnNames) + """)
        values (""" + ", ".join(data) + """);
    """

    cur.execute(insert_data_query)
    cur.close()

def insertRowsRandomBdd(conn, schemaName, tableName, rowCount, dictionarySize, amountOfPossibilities, bddSize):
    cur = conn.cursor()

    insert_data_query = """
                insert into """ + schemaName + "." + tableName + """ (id, person, color, car, _sentence) values 
        """
    for i in range(rowCount // amountOfPossibilities):
        randomVar = bddFunctions.generateRandDictValue(dictionarySize)
        for j in range(amountOfPossibilities):
            bdd = bddFunctions.createBdd(bddSize, randomVar, f"{j + 1}")
            insert_data_query += """
                (""" + str(i) + """, 'person""" + str(i) + """', 'color""" + str(j) + """', 'car""" + str(j) + """', """ + bdd + """),"""
    insert_data_query = insert_data_query[:-1] + ";"
    cur.execute(insert_data_query)

    cur.close()

def insertRowsNoRandomness(conn, schemaName, tableName, rowCount, dictionarySize, amountOfPossibilities, bddSize):
    cur = conn.cursor()

    insert_data_query = """
                insert into """ + schemaName + "." + tableName + """ (id, person, color, car, _sentence) values 
        """
    for i in range(rowCount // amountOfPossibilities):
        randomVar = bddFunctions.getDictValue(i, dictionarySize)
        for j in range(amountOfPossibilities):
            bdd = bddFunctions.createBdd(bddSize, randomVar, f"{j + 1}")
            insert_data_query += """
                (""" + str(i) + """, 'person""" + str(i) + """', 'color""" + str(j) + """', 'car""" + str(j) + """', """ + bdd + """),"""
    insert_data_query = insert_data_query[:-1] + ";"
    cur.execute(insert_data_query)

    cur.close()