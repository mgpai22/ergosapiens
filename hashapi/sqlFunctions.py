import sqlite3


def createHashTable():
    connection = sqlite3.connect('hash.db')
    cursor = connection.cursor()
    command1 = """CREATE TABLE IF NOT EXISTS
    hashTable(hash TEXT)"""
    cursor.execute(command1)
    connection.commit()
    connection.close()


def writeToHash(hash):
    connection = sqlite3.connect('hash.db')
    cursor = connection.cursor()
    command1 = """CREATE TABLE IF NOT EXISTS
    hashTable(hash TEXT)"""
    cursor.execute(command1)
    cursor.execute("INSERT INTO hashTable VALUES (?)", (hash,))
    connection.commit()
    connection.close()


def queryHashTable(query):
    connection = sqlite3.connect('hash.db')
    cursor = connection.cursor()
    sqlite_select_query = """SELECT * from hashTable WHERE hash = ?"""
    cursor.execute(sqlite_select_query, (query,))
    results = cursor.fetchone()
    connection.close()
    return results


def HashTable():
    connection = sqlite3.connect('hash.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM hashTable")
    results = cursor.fetchall()
    connection.close()
    return results


def createHashTableTest():
    connection = sqlite3.connect('hashTest.db')
    cursor = connection.cursor()
    command1 = """CREATE TABLE IF NOT EXISTS
    hashTableTest(hash TEXT)"""
    cursor.execute(command1)
    connection.commit()
    connection.close()


def writeToHashTest(hash):
    connection = sqlite3.connect('hashTest.db')
    cursor = connection.cursor()
    command1 = """CREATE TABLE IF NOT EXISTS
    hashTableTest(hash TEXT)"""
    cursor.execute(command1)
    cursor.execute("INSERT INTO hashTableTest VALUES (?)", (hash,))
    connection.commit()
    connection.close()


def queryHashTableTest(query):
    connection = sqlite3.connect('hashTest.db')
    cursor = connection.cursor()
    sqlite_select_query = """SELECT * from hashTableTest WHERE hash = ?"""
    cursor.execute(sqlite_select_query, (query,))
    results = cursor.fetchone()
    connection.close()
    return results


def validateHash(hash):
    if queryHashTable(hash) is not None:
        return True
    return False


def validateHashTest(hash):
    if queryHashTableTest(hash) is not None:
        return True
    return False
