import itertools, datetime

from trello import TrelloClient
import pika, pickle

from secrets_s import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_OAUTH_KEY, TRELLO_OAUTH_SECRET
from models import AddCardRecurrence
from data import DbClient

class BoardMissingError(Exception):
    pass

class ListMissingError(Exception):
    pass

client = TrelloClient(TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_OAUTH_KEY,
        TRELLO_OAUTH_SECRET)
db_client = DbClient()

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
    created_card = create_card(job.board_id, job.list_id, job.name, job.desc)
    db_client.update_recurrence_run_time(job, datetime.datetime.now())
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print "Created", created_card

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue = "addcard", durable = True)
    channel.basic_qos(prefetch_count = 1)
    channel.basic_consume(callback, queue = "addcard")
    channel.start_consuming()
