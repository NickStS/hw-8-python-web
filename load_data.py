import json
from mongoengine import connect
from models import Author, Quote

connect('Nick', host='mongodb+srv://Nick:123@cluster0.wwcxrz8.mongodb.net/')

with open('authors.json', 'r', encoding='utf-8') as authors_file:
    authors_data = json.load(authors_file)
    for author_data in authors_data:
        author = Author(**author_data)
        author.save()

with open('qoutes.json', 'r', encoding='utf-8') as quotes_file:
    quotes_data = json.load(quotes_file)
    for quote_data in quotes_data:
        author_name = quote_data.pop('author')
        author = Author.objects(fullname=author_name).first()
        quote = Quote(author=author, **quote_data)
        quote.save()
