import pika

from config.env_utils import get_env_value

RABBITMQ_URL = get_env_value('RABBITMQ_URL')
def send_message(queue_name, message):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                             delivery_mode=2,  # make message persistent
                          ))
    print(" [x] Sent %r" % message)
    connection.close()

def receive_message(queue_name, callback):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
