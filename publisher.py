import pika, pickle, time, datetime

from dateutil import rrule, parser

from models import AddCardRecurrence
from data import DbClient

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue = "addcard", durable = True)

db_client = DbClient()

def publish(add_card_recurrence):
    channel.basic_publish(exchange = "", routing_key = "addcard", body =
            pickle.dumps(add_card_recurrence), properties =
            pika.BasicProperties(delivery_mode = 2))
    print "Published", r.name

if __name__ == "__main__":
    while True:
        recurrences = db_client.get_all_recurrences() 
        now = datetime.datetime.now()
        for r in recurrences:
            print "===========", r.name, "============"

            after = None
            if r.last_run_date is None:
                rr = rrule.rrulestr(r.rrule)
                after = rr[0]
            else:
                last_run_date = parser.parse(r.last_run_date)
                rr = rrule.rrulestr(r.rrule, dtstart = last_run_date)
                after = rr.after(last_run_date)

            print "\tLAST RUN: ", last_run_date
            print "\tNOW:      ", now
            print "\tAFTER:    ", after

            if after <= now:
                publish(r)

        time.sleep(10)

    connection.close()
