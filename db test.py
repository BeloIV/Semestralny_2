import sqlite3

tab = sqlite3.connect('databaza.db')
c = tab.cursor()
c.execute("""CREATE TABLE "pozicovna" (
	"id"	INTEGER COLLATE BINARY,
	"nazov"	TEXT COLLATE BINARY,
	"popis"	TEXT COLLATE BINARY,
	"km" INTEGER COLLATE BINARY,
	"rok" INTEGER COLLATE BINARY,
	"kw" INTEGER COLLATE BINARY,
	"objem" INTEGER COLLATE BINARY,
	"spotreba" REAL COLLATE BINARY,
	"cenaden" REAL COLLATE BINARY,
	"cenatyzden" REAL COLLATE BINARY,
	"typ" TEXT COLLATE BINARY,
	"obrazky" TEXT COLLATE BINARY,
	"rented"	INTEGER DEFAULT 0 COLLATE BINARY,
	
	
	PRIMARY KEY("id" AUTOINCREMENT)
);
""")
# c.execute("INSERT INTO pozicovna (nazov,popis,cena,rent) VALUES    ('audi','je to super auto', 40,1)")
# #c.execute("DELETE FROM pozicovna WHERE id = 5 or id = 6 ")
c.execute("SELECT * FROM pozicovna")
my = c.fetchall()
print(my)
tab.commit()
tab.close()


