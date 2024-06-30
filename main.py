import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf
import RQcreateFunction as rqf

schemaName = "testSchema"

rqf.setupTables(2)
rqf.addRows(2, 2520, 1, 1, 2520)
rqf.setupDictionary(2520, 1)

conn = c.connect()
# rqf.runQuery(conn, qf.updateDictionaryWithCache, qf.updateDictionary, 2)
qf.updateDictionary(conn, schemaName, "without")
conn.commit()
c.close(conn)