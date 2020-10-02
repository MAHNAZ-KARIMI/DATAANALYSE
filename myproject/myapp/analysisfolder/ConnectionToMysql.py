import sys
import mysql.connector
def dockerConnection():    
    rootconn = myconnect('root','root')
    return rootconn
def myconnect(user, pw):
    
    conn = mysql.connector.connect( host='localhost', database='ervervsstyrelse',user='root', password='root')
    conn.autocommit = True
    return conn  

def sqlQuery(sqlString, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(sqlString)
        res = cursor.fetchall()
        return res
    except Exception as ex:
        print(str(ex), file=sys.stderr)
    finally:    
        cursor.close()

def sqlDo(sqlString, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(sqlString)
        res = cursor.fetchwarnings()
        return res
    except Exception as ex:
        print(str(ex), file=sys.stderr)
    finally:    
        cursor.close()

"Done"