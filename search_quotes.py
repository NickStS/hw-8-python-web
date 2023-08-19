import pika
from mongoengine import connect
from models import Author, Quote
from config import rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password, queue_name
from consumer import callback


connect('Nick', host='mongodb+srv://Nick:123@cluster0.wwcxrz8.mongodb.net/')


if __name__ == "__main__":
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password))
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("Waiting for messages from the queue...")

    while True:
        command = input("Enter command (name, tag, tags, exit): ").strip().lower()

        if command == "exit":
            break
        elif command == "name":
            author_name = input("Enter author's name: ")
            if command.startswith('name:'):
                author_name = command.replace('name:', '').strip()
                author = Author.objects(fullname=author_name).first()
                if author:
                    quotes = Quote.objects(author=author)
                    for quote in quotes:
                        print(quote.quote)
                else:
                    print("Author not found.")
                    
        elif command == "tag":
            tag = input("Enter tag: ")
            if command.startswith('tag:'):
                tag = command.replace('tag:', '').strip()
                quotes = Quote.objects(tags=tag)
                for quote in quotes:
                    print(quote.quote)
            
        elif command == "tags":
            tags = input("Enter tags (comma-separated): ").split(',')
            if command.startswith('tags:'):
                tags = command.replace('tags:', '').strip().split(',')
                quotes = Quote.objects(tags__in=tags)
                for quote in quotes:
                    print(quote.quote)
        else:
            print("Wrong command. Try again.")

    channel.start_consuming()
