import sqlite3

conn = sqlite3.connect("BookList.sqlite")
cursor = conn.cursor()

sql_query = """CREATE TABLE BookList(
id integer PRIMARY KEY ,
author text NOT NULL ,
year integer NOT NULL ,
title text NOT NULL
)"""

cursor.execute(sql_query)

