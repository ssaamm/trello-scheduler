import itertools

from trello import TrelloClient
import pika, pickle

from secrets_s import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_OAUTH_KEY, TRELLO_OAUTH_SECRET
from Job import AddCardJob

class BoardMissingError(Exception):
    pass

class ListMissingError(Exception):
    pass

client = TrelloClient(TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_OAUTH_KEY,
        TRELLO_OAUTH_SECRET)

def create_card(board_id, list_id, name, desc = None):
    board = next(itertools.ifilter(lambda b: b.id == board_id,
        client.list_boards()), None)
    if not board:
        raise BoardMissingError()
    list_ = next(itertools.ifilter(lambda l: l.id == list_id, board.all_lists()),
        None)
    if not list_:
        raise ListMissingError()
    return list_.add_card(name, desc)

def callback(ch, method, properties, body):
    job = pickle.loads(body)
    print create_card(job.board_id, job.list_id, job.name, job.desc)

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue = "addcard")
    channel.basic_consume(callback, queue = "addcard", no_ack = True)
    channel.start_consuming()
