import sqlite3 as sql


# Crea la db
def createDB():
    conn=sql.connect("/home/gabriel/prog/sena/congres/instance/IVcongress.db")
    conn.commit()
    conn.close()


# Crea la tabla en la db
def createTableAsistente():
    conn=sql.connect("/home/gabriel/prog/sena/congres/instance/IVcongress.db")
    cursor=conn.cursor()
    cursor.execute(
        """CREATE TABLE Asistente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            empresa TEXT NOT NULL,
            cargo TEXT
        )"""
    )
    conn.commit()
    conn.close()


# Crea la tabla en la db
def createTablePonente():
    conn=sql.connect("/home/gabriel/prog/sena/congres/instance/IVcongress.db")
    cursor=conn.cursor()
    cursor.execute(
        """CREATE TABLE Ponente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            empresa TEXT NOT NULL,
            cargo TEXT,
            tema TEXT NOT NULL,
            titulo TEXT NOT NULL,
            comentarios TEXT
        )"""
    )
    conn.commit()
    conn.close()


createDB()
createTableAsistente()
createTablePonente()
