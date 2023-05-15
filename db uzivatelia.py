import hashlib
import sqlite3

# pripojenie k databáze
conn = sqlite3.connect('databaza.db')

c = conn.cursor()
c.execute('''CREATE TABLE pouzivatelia (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 meno TEXT,
                 mail TEXT,
                 heslo TEXT,
                Adresa TEXT,
                 pozicane_auto TEXT

                 )''')

# # pridanie testovacích dát
# meno = "Jozko Mrkvicka"
# mail = "jozko.mrkvicka@gmail.com"
# heslo = "moje_tajne_heslo"
# heslo3 = "moje_tajne_heslo"
# heslo2 = "tajne_heslo"
# # šifrovanie hesla pomocou SHA256
# sifra = hashlib.sha256(heslo.encode('utf-8')).hexdigest()
# sifra2 = hashlib.sha256(heslo2.encode('utf-8')).hexdigest()
# sifra3 = hashlib.sha256(heslo3.encode('utf-8')).hexdigest()
# print(sifra)
# print(sifra2)

# vloženie dát do tabuľky
#conn.execute(f"INSERT INTO uzivatelia (meno, mail, heslo) VALUES (?, ?, ?)", (meno, mail, sifra))

# ukončenie spojenia s databázou
conn.commit()
conn.close()