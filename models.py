class AddCardRecurrence(object):
    def __init__(self, board_id, list_id, rrule, name, desc,
            last_run_date = None, is_deleted = 0, row_id = None):
        self.row_id = row_id
        self.board_id = board_id
        self.list_id = list_id
        self.rrule = rrule
        self.name = name
        self.desc = desc
        self.last_run_date = last_run_date
        self.is_deleted = is_deleted
