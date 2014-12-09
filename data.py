import sqlite3
from models import AddCardRecurrence

class DbClient(object):
    def create_recurrence(self, add_card_recurrence):
        conn = sqlite3.connect("scheduler.db")
        c = conn.cursor()
        c.execute("INSERT INTO add_card_recurrences (board_id, list_id, rrule, "
                "name, desc, last_run_date, is_deleted) VALUES (?, ?, ?, ?, ?, "
                "?, ?);", (add_card_recurrence.board_id,
                    add_card_recurrence.list_id, add_card_recurrence.rrule,
                    add_card_recurrence.name, add_card_recurrence.desc,
                    add_card_recurrence.last_run_date,
                    add_card_recurrence.is_deleted))
        conn.commit()
        conn.close()

    def get_all_recurrences(self):
        recurrences = []
        conn = sqlite3.connect("scheduler.db")
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM add_card_recurrences;")
        for r in c:
            recurrences.append(AddCardRecurrence(r[1], r[2], r[3], r[4], r[5],
                r[6], r[7], r[0]))
        conn.close()
        return recurrences

    def update_recurrence_run_time(self, recurrence, new_date):
        conn = sqlite3.connect("scheduler.db")
        c = conn.cursor()
        c.execute("UPDATE add_card_recurrences "
                "SET last_run_date = ?"
                "WHERE rowid = ?;",
                (new_date, recurrence.row_id,))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    db_client = DbClient()
    rs = db_client.get_all_recurrences()
    for r in rs:
        print r.row_id, r.board_id, r.list_id, r.rrule, r.name, r.desc, r.last_run_date, r.is_deleted
