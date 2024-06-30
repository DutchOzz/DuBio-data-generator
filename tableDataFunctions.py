import bddFunctions

def insertRows(conn, schemaName, tableName, columnAmount, rowCount, dictionarySize, amountOfPossibilities, bddSize, bddCombiner = '&'):
    cur = conn.cursor()

    insert_data_query = """
                insert into """ + schemaName + "." + tableName + """ values 
        """
    for i in range(rowCount // amountOfPossibilities):
        for j in range(amountOfPossibilities):
            bdd = bddFunctions.createBdd(bddSize, f"{j + 1}", dictionarySize, bddCombiner)
            insert_data_query += """(""" + str(i) + """, """
            for k in range(columnAmount - 2):
                insert_data_query += """'""" + str(k) + str(i) + """', """
            insert_data_query += bdd + """),"""
    insert_data_query = insert_data_query[:-1] + ";"
    cur.execute(insert_data_query)

    cur.close()

def insertRowsWithCache(conn, schemaName, tableName, columnAmount, rowCount, dictionarySize, amountOfPossibilities, bddSize, bddCombiner = '&'):
    cur = conn.cursor()

    insert_data_query = """
                insert into """ + schemaName + "." + tableName + """ values 
        """
    probability = 1/amountOfPossibilities
    for i in range(rowCount // amountOfPossibilities):
        # var = bddFunctions.getDictValue(i, dictionarySize)
        for j in range(amountOfPossibilities):
            bdd = bddFunctions.createBdd(bddSize, f"{j + 1}", dictionarySize, bddCombiner)
            insert_data_query += """
                (""" + str(i) + """, """
            for k in range(columnAmount - 2):
                insert_data_query += """'""" + str(k) + str(i) + """', """
            insert_data_query += bdd + """, """ + str(probability) + """),"""
    insert_data_query = insert_data_query[:-1] + ";"
    cur.execute(insert_data_query)

    cur.close()