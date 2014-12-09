import datetime
from recurrent import RecurringEvent
from dateutil import rrule

import itertools

from trello import TrelloClient

from secrets_s import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_OAUTH_KEY, TRELLO_OAUTH_SECRET
from models import AddCardRecurrence
from data import DbClient

client = TrelloClient(TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_OAUTH_KEY,
        TRELLO_OAUTH_SECRET)

if __name__ == "__main__":
    r = RecurringEvent()
    db_client = DbClient()

    boards = client.list_boards()
    print "Boards:"
    for b in boards:
        print " - ", b.name

    s = raw_input("Enter board name: ").strip()
    board = next(itertools.ifilter(lambda b: b.name == s,
        boards), None)
    if not board:
        raise BoardMissingError()

    lists = board.all_lists()
    for l in lists:
        print " - ", l.name
    s = raw_input("Enter list name: ").strip()
    list_ = next(itertools.ifilter(lambda l: l.name == s,
        lists), None)
    if not list_:
        raise ListMissingError()

    s = raw_input("Enter card title: ").strip()
    name = s.strip()

    s = raw_input("Enter card description: ").strip()
    desc = s.strip() if len(s.strip()) > 0 else None

    s = raw_input("Enter recurrence: ").strip()
    r.parse(s)
    recurrence = r.get_RFC_rrule()
    rr = rrule.rrulestr(recurrence)

    print board.name, list_.name, recurrence, name, desc
    recurrence_to_create = AddCardRecurrence(board.id, list_.id, recurrence, name, desc)
    db_client.create_recurrence(recurrence_to_create)

