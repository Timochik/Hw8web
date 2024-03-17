import pika
import json
from faker import Faker
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect('my_database', host='mongodb+srv://ttimofej983:19072007Tt@cluster0.sw9tzpg.mongodb.net/')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Генерування фейкових контактів та їх збереження в базі даних
fake = Faker()

for _ in range(5):  # Генеруємо 5 контактів для прикладу
    fullname = fake.name()
    email = fake.email()
    contact = Contact(fullname=fullname, email=email)
    contact.save()

    # Відправляємо ID контакту до RabbitMQ
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=json.dumps({'contact_id': str(contact.id)})
    )

    print(f"Contact {fullname} with email {email} added to email queue.")

connection.close()
