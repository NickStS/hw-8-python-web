import pika
from mongoengine import connect
from config import rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password, queue_name
from models import Author, Quote

connect('Nick', host='mongodb+srv://Nick:123@cluster0.wwcxrz8.mongodb.net/')


def send_email(contact_id):
    print(f"Sending a message to the email address of a contact with ID {contact_id}")

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    author = Author.objects(id=contact_id).first()
    if author:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(quote.quote)
    else:
        print(f"Author with ID {contact_id} not found")

if __name__ == "__main__":
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password))
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("Waiting for messages from the queue...")
    channel.start_consuming()
