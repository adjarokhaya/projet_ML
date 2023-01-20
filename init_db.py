from flask import Flask

import sqlite3
connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user (adressemail, mdp) VALUES (?, ?)",
            ('adja@ca.fr', 'mdp1')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('erwyn@ca.fr', 'mdp2')
            )

connection.commit()
connection.close()