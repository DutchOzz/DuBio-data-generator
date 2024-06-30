import psycopg2
import connection

# Create a table in the database
def create_table(conn, schemaName, tableName, columnAmount):
    cur = conn.cursor()
    colAmountToAdd = columnAmount - 2
    create_table_query = """
        create table """ + schemaName + "." + tableName +  """ (id int, """
    for i in range(97, colAmountToAdd+97):
        create_table_query += chr(i) + """ varchar(255), """
    create_table_query += """ _sentence bdd) """

    cur.execute(create_table_query)
    cur.close()

# Drop a table from the database
def drop_table(conn, schemaName, tableName):
    cur = conn.cursor()

    drop_table_query = """
        drop table """ + schemaName + "." + tableName +  """;
    """
    cur.execute(drop_table_query)
    cur.close()

# Add a column to a table in the database
def add_column(conn, schemaName, tableName, columnName, columnType):
    cur = conn.cursor()

    add_column_query = """
        alter table """ + schemaName + "." + tableName +  """
        add column """ + columnName + """ """ + columnType + """;
    """

    cur.execute(add_column_query)
    cur.close()

# Drop a column from a table in the database
def drop_column(conn, schemaName, tableName, columnName):
    cur = conn.cursor()

    drop_column_query = """
        alter table """ + schemaName + "." + tableName +  """
        drop column """ + columnName + """;
    """

    cur.execute(drop_column_query)
    cur.close()
