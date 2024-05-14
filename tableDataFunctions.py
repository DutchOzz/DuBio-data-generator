import connection
import tableFunctions

# insert random data into the table
def insert_data(conn, schemaName, tableName, columnNames, data):
    cur = conn.cursor()

    insert_data_query = """
        insert into """ + schemaName + "." + tableName + """ (""" + ", ".join(columnNames) + """)
        values (""" + ", ".join(data) + """);
    """

    cur.execute(insert_data_query)
    cur.close()