import pika, pickle
from Job import AddCardJob

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue = "addcard")

test_board_id = "5485dda4eb47513ae71bd0b0"
apples_list_id = "5485df9de28db973c841d213"
jobs = [AddCardJob(test_board_id, apples_list_id, "Golden delicious", None),
    AddCardJob(test_board_id, apples_list_id, "Red delicious", "yay delicious")]

for job in jobs:
    channel.basic_publish(exchange = "", routing_key = "addcard",
        body = pickle.dumps(job))
    print pickle.dumps(job)

connection.close()
