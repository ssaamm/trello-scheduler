import sqlite3

def init_db():
    conn = sqlite3.connect("scheduler.db")
    c = conn.cursor()
    c.execute("CREATE TABLE add_card_recurrences ("
            "    board_id TEXT NOT NULL,"
            "    list_id TEXT NOT NULL,"
            "    rrule TEXT NOT NULL,"
            "    name TEXT NOT NULL,"
            "    desc TEXT,"
            "    last_run_date TEXT,"
            "    is_deleted INTEGER NOT NULL"
            ");")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
