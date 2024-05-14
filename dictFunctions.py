import tableFunctions as tf
import random

# create a dictionary table
def createDictionary(conn, schemaName):
    cur = conn.cursor()
    create_table_query = """
        CREATE TABLE """ + schemaName + """._dict (name varchar(20), dict dictionary);
    """
    cur.execute(create_table_query)
    cur.close()

    insertValueIntoDictionary(conn, schemaName)

def insertValueIntoDictionary(conn, schemaName):
    cur = conn.cursor()
    insert_data_query = """
        INSERT INTO """ + schemaName + """._dict(name,dict) VALUES ('mydict',dictionary(''));
    """
    cur.execute(insert_data_query)
    cur.close()

# drop a dictionary table
def dropDictionary(conn, schemaName):
    tf.drop_table(conn, schemaName, "_dict")

# add dictionary entries to the dictionary table
def addDictionaryEntries(conn, schemaName, number_of_letters, number_of_possibilities):
    cur = conn.cursor()

    add_dict_entry_query = """
        update """ + schemaName + """._dict
        set dict = add(dict,\'""" + generate_string(number_of_letters, number_of_possibilities) + """\')
    """
    cur.execute(add_dict_entry_query)

    cur.close()


def generate_string(num_letters, num_numbers):
    assert num_letters <= 26*26*26, "The number of letters must be less than or equal to 26*26*26"

    result = ''
    for i in range(num_letters):
        letter = chr(ord('a') + (i // (26*26))) + chr(ord('a') + ((i // 26) % 26)) + chr(ord('a') + (i % 26))  # Generate letters 'aaa' to 'zzz'
        
        remaining_probability = 1.0
        for j in range(1, num_numbers + 1):
            if j == num_numbers:
                probability = remaining_probability
            else:
                probability = random.uniform(0, remaining_probability)
            result += f"{letter}={j}:{probability:.2f};"
            remaining_probability -= probability
    return result[:-1]  # Remove the last ';' character