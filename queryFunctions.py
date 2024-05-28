def calculateProbabilities(conn, schemaName, tableName):
    cur = conn.cursor()

    calculate_probabilities_query = """
        (select t._sentence, prob(d.dict, t._sentence) AS probability from """ + schemaName + "." + tableName + """ t, """ + schemaName + """._dict d)
    """
    cur.execute(cur.mogrify('explain analyze ' + calculate_probabilities_query))
    analyze_fetched = cur.fetchall()
    executionTime = float(analyze_fetched[-1][0][16:21])
    cur.close()

    return executionTime

def getCachedProbabilities(conn, schemaName, tableName):
    cur = conn.cursor()

    get_cached_probabilities_query = """
        (select _sentence, probability from """ + schemaName + "." + tableName + """)
    """

    cur.execute(cur.mogrify('explain analyze ' + get_cached_probabilities_query))
    analyze_fetched = cur.fetchall()
    executionTime = float(analyze_fetched[-1][0][16:21])
    cur.close()

    return executionTime

def selectTable(conn, schemaName, tableName):
    cur = conn.cursor()

    select_table_query = """
        (select * from """ + schemaName + "." + tableName + """)
    """

    cur.execute(cur.mogrify('explain analyze ' + select_table_query))
    analyze_fetched = cur.fetchall()
    executionTime = float(analyze_fetched[-1][0][16:21])
    cur.close()

    return executionTime

def updateDictionary(conn, schemaName, tableName, amountOfPossibilities = 10):
    cur = conn.cursor()

    update_dictionary_query = """
        UPDATE """ + schemaName + """._dict SET dict = upd(dict, 'aaa=1:1
    """
    for i in range(amountOfPossibilities - 1):
        update_dictionary_query += ";aaa=" + str(i+2) + ":0"
    update_dictionary_query += "');"

    cur.execute("BEGIN;")
    cur.execute(cur.mogrify('explain analyze ' + update_dictionary_query))
    analyze_fetched = cur.fetchall()
    cur.execute("ROLLBACK;")
    executionTime = float(analyze_fetched[-1][0][16:21])
    cur.close()

    return executionTime

def updateDictionaryWithCache(conn, schemaName, tableName, amountOfPossibilities = 10):
    cur = conn.cursor()

    update_dictionary_query = """
        UPDATE """ + schemaName + """._dict SET dict = upd(dict, 'aaa=1:1
    """
    for i in range(amountOfPossibilities - 1):
        update_dictionary_query += ";aaa=" + str(i+2) + ":0"
    update_dictionary_query += "');"

    update_table_query = """
        UPDATE """ + schemaName + """."""+ tableName + """
        SET probability = prob(d.dict, _sentence)
        FROM """ + schemaName + """._dict d;
    """

    cur.execute("BEGIN;")
    cur.execute(cur.mogrify('explain analyze ' + update_dictionary_query))
    analyze_fetched = cur.fetchall()
    cur.execute(cur.mogrify('explain analyze ' + update_table_query))
    analyze_fetched2 = cur.fetchall()
    cur.execute("ROLLBACK;")
    executionTime = float(analyze_fetched[-1][0][16:21])
    executionTime2 = float(analyze_fetched2[-1][0][16:21])
    totalExecutionTime = executionTime + executionTime2
    cur.close()

    return totalExecutionTime

def smartUpdateDictionaryWithCache(conn, schemaName, tableName, amountOfPossibilities = 10):
    cur = conn.cursor()

    update_dictionary_query = """
        UPDATE """ + schemaName + """._dict SET dict = upd(dict, 'aaa=1:1
    """
    for i in range(amountOfPossibilities - 1):
        update_dictionary_query += ";aaa=" + str(i+2) + ":0"
    update_dictionary_query += "');"

    update_table_query = """
        UPDATE """ + schemaName + """."""+ tableName + """
        SET probability = prob(d.dict, _sentence)
        FROM """ + schemaName + """._dict d
        WHERE """ + schemaName + """."""+ tableName + """.person LIKE '%rank%';
    """

    cur.execute("BEGIN;")
    cur.execute(cur.mogrify('explain analyze ' + update_dictionary_query))
    analyze_fetched = cur.fetchall()
    cur.execute(cur.mogrify('explain analyze ' + update_table_query))
    analyze_fetched2 = cur.fetchall()
    cur.execute("ROLLBACK;")
    executionTime = float(analyze_fetched[-1][0][16:21])
    executionTime2 = float(analyze_fetched2[-1][0][16:21])
    totalExecutionTime = executionTime + executionTime2
    cur.close()

    return totalExecutionTime
