def calculateProbabilities(conn, schemaName, tableName):
    cur = conn.cursor()

    calculate_probabilities_query = """
        (select t._sentence, prob(d.dict, t._sentence) AS probability from """ + schemaName + "." + tableName + """ t, """ + schemaName + """._dict d)
    """
    # select t._sentence, prob(d.dict, t._sentence) AS probability from testSchema.drives t, testSchema._dict d
    cur.execute(calculate_probabilities_query)
    # for table in cur.fetchall():
    #     print(table)
    cur.close()

def getCachedProbabilities(conn, schemaName, tableName):
    cur = conn.cursor()

    get_cached_probabilities_query = """
        (select _sentence, probability from """ + schemaName + "." + tableName + """)
    """

    cur.execute(get_cached_probabilities_query)
    cur.close()