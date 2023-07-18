import os
import json
import sqlite3 as sql3

with open("/home/gabriel/prog/json_config/csvTools.json") as config_file:
    config = json.load(config_file)

conn = sql3.connect(config['DB_ADDRESS'])
cursor = conn.cursor()
query = f""" CREATE TABLE Ponente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    empresa TEXT NOT NULL,
    cargo TEXT NOT NULL,
    tema TEXT NOT NULL,
    titulo TEXT NOT NULL,
    comentarios TEXT NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
); """
cursor.execute(query)
conn.close()

conn = sql3.connect(config['DB_ADDRESS'])
cursor = conn.cursor()
query = f""" CREATE TABLE Participante (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    empresa TEXT NOT NULL,
    cargo TEXT NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
); """
cursor.execute(query)
conn.close()

