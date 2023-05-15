import sqlite3

# Vytvoríme pripojenie k databáze
conn = sqlite3.connect('databaza.db')

# Vytvoríme kurzor
c = conn.cursor()

# Vytvoríme tabuľku pre ukladanie objednávok
c.execute('''CREATE TABLE objednavky
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              id_auta INTEGER,
              id_uzivatela INTEGER,
              datum_od DATE,
              datum_do DATE,
              cena REAL)''')

# Uložíme zmeny a ukončíme pripojenie
conn.commit()
conn.close()