import os
import sqlite3


pozic = sqlite3.connect('pozicovna.db')

c = pozic.cursor()
c.execute("SELECT * FROM pozicovna ")

xx = c.fetchall()
for i in xx:
    obrazky = i[-3]

    obrazky = obrazky.split("//")
    if len(obrazky) >5:

        id = i[0]
        na_zmazanie = obrazky[5:]
        obrazky = obrazky[:5]
        sql_query = f"UPDATE pozicovna SET obrazky = ? WHERE id = ?"
        pozic.commit()
        obrazky = "//".join(obrazky)
        print(obrazky,id)
        c.execute(sql_query, (obrazky, id))
        for i in na_zmazanie:
            os.remove("/Users/stefanbelusko/Desktop/skola/programovanie/Semestralny_2/Obrazky_aut/"+i)







pozic.close()
