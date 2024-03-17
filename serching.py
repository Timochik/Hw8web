from mongoengine import connect
from models import Author, Quote

def search_quotes(command):
    if command.startswith('name:'):
        author_name = command.split(':')[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(f"Author: {author.fullname}")
                print(f"Quote: {quote.quote}")
                print("Tags:", ', '.join(quote.tags))
                print()
        else:
            print("Author not found.")
    
    elif command.startswith('tag:'):
        tag = command.split(':')[1].strip()
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print(f"Author: {quote.author.fullname}")
            print(f"Quote: {quote.quote}")
            print("Tags:", ', '.join(quote.tags))
            print()

    elif command.startswith('tags:'):
        tags = command.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(f"Author: {quote.author.fullname}")
            print(f"Quote: {quote.quote}")
            print("Tags:", ', '.join(quote.tags))
            print()
    
    elif command == 'exit':
        return False
    
    else:
        print("Invalid command.")
    
    return True

if __name__ == '__main__':
    connect('my_database', host='mongodb+srv://ttimofej983:19072007Tt@cluster0.sw9tzpg.mongodb.net/')
    while True:
        command = input("Enter command: ")
        if not search_quotes(command):
            break
