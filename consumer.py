import pika
import json
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect('my_database', host='mongodb://username:password@host:port/my_database')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Функція для імітації надсилання електронного листа
def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.email}...")

    # Отримання контакту із бази даних та оновлення логічного поля
    contact.email_sent = True
    contact.save()

    print(f"Email sent to {contact.email}.")

# Callback-функція для обробки повідомлень з черги RabbitMQ
def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    send_email(contact_id)

# Встановлення зв'язку між чергою та callback-функцією
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
