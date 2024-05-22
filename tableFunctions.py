import psycopg2
import connection

# Create a table in the database
def create_table(conn, schemaName, tableName):
    cur = conn.cursor()

    create_table_query = """
        create table """ + schemaName + "." + tableName +  """ (like pp2324_37.drives including all);
    """

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
