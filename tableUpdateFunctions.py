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



conn = connection.connect()
# tableFunctions.drop_table(conn, "testSchema", "drives")
# tableFunctions.create_table(conn, "testSchema", "drives")
# tableFunctions.add_column(conn, "testSchema", "drives", "probability", "FLOAT")
# tableFunctions.drop_column(conn, "testSchema", "drives", "probability")
insert_data(conn, "testSchema", "drives", ["id", "person", "color", "car", "_sentence", "probability"], [["1", "'huhih'", "100", "25", "Bdd('A = 1')", "0.5"]])

conn.commit()
connection.close(conn)