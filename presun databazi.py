import sqlite3

# Otevření původního databázového souboru
source_conn = sqlite3.connect('databaza.db')
source_cursor = source_conn.cursor()

# Získání seznamu tabulek v původním souboru
source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = source_cursor.fetchall()
tables = tables[1:]

# Pro každou tabulku vytvořte samostatný soubor a přesuňte data
for table in tables:
    table_name = table[0]
    target_conn = sqlite3.connect(f'{table[0]}.db')
    target_cursor = target_conn.cursor()

    # Vytvoření kopie tabulky v samostatném souboru
    source_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table[0]}';")

    create_table_query = source_cursor.fetchone()[0]
    target_cursor.execute(create_table_query)

    # Přesun dat do samostatného souboru
    source_cursor.execute(f"SELECT * FROM {table[0]};")
    rows = source_cursor.fetchall()
    placeholders = ', '.join('?' * len(rows[0]))  # Vytvoření řetězce s otazníky
    target_cursor.executemany(f"INSERT INTO {table[0]} VALUES ({placeholders})", rows)

    # Potvrzení změn v samostatném souboru
    target_conn.commit()

    # Uzavření spojení se samostatným souborem
    target_conn.close()

# Uzavření spojení s původním souborem
source_conn.close()
