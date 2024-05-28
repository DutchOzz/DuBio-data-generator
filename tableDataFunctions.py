import bddFunctions

def insertRows(conn, schemaName, tableName, rowCount, dictionarySize, amountOfPossibilities, bddSize, bddCombiner = '&'):
    cur = conn.cursor()

    insert_data_query = """
                insert into """ + schemaName + "." + tableName + """ (id, person, color, car, _sentence) values 
        """
    for i in range(rowCount // amountOfPossibilities):
        # var = bddFunctions.getDictValue(i, dictionarySize)
        for j in range(amountOfPossibilities):
            bdd = bddFunctions.createBdd(bddSize, f"{j + 1}", dictionarySize, bddCombiner)
            insert_data_query += """
                (""" + str(i) + """, 'person""" + str(i) + """', 'color""" + str(j) + """', 'car""" + str(j) + """', """ + bdd + """),"""
    insert_data_query = insert_data_query[:-1] + ";"
    cur.execute(insert_data_query)

    cur.close()

def insertRowsWithCache(conn, schemaName, tableName, rowCount, dictionarySize, amountOfPossibilities, bddSize, bddCombiner = '&', name = "person"):
    cur = conn.cursor()

    insert_data_query = """
                insert into """ + schemaName + "." + tableName + """ (id, person, color, car, _sentence, probability) values 
        """
    probability = 1/amountOfPossibilities
    for i in range(rowCount // amountOfPossibilities):
        # var = bddFunctions.getDictValue(i, dictionarySize)
        for j in range(amountOfPossibilities):
            bdd = bddFunctions.createBdd(bddSize, f"{j + 1}", dictionarySize, bddCombiner)
            insert_data_query += """
                (""" + str(i) + """, '""" + name + str(i) + """', 'color""" + str(j) + """', 'car""" + str(j) + """', """ + bdd + """, """ + str(probability) + """),"""
    insert_data_query = insert_data_query[:-1] + ";"
    cur.execute(insert_data_query)

    cur.close()