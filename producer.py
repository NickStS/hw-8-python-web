import pika
import random
import string
from mongoengine import connect
from config import rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password, queue_name
from models import Author

connect('Nick', host='mongodb+srv://Nick:123@cluster0.wwcxrz8.mongodb.net/')


def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_authors(num_authors):
    for _ in range(num_authors):
        fullname = random_string(10)
        born_date = "2020-01-01"
        born_location = "Somewhere"
        description = "Some description"
        author = Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
        author.save()

def send_to_queue(author_id):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password))
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=str(author_id))
    connection.close()

if __name__ == "__main__":
    num_authors = 10
    generate_authors(num_authors)
    
    for author in Author.objects:
        send_to_queue(str(author.id))
