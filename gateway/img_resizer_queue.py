import cv2
import os
import pika


'''
    Class responsible to manage queue service, containing methods:
    - start: make the new queue connection
    - stop: close queue connection created before
    - callback: standard method of RabbitMQ that make pre-coded actions
    - resize_image: method that resize received image by API and saves in a temporary path
'''

class ImageResizer:
    def __init__(self, host):
        self.host = host
        self.connection = None
        self.channel = None
        self.queue_name = 'image_queue'

    def start(self):
        amqp_url = os.environ['AMQP_URL']
        parameters = pika.URLParameters(amqp_url)
        #self.connection = pika.SelectConnection(parameters)
        #credentials = pika.PlainCredentials('guest', 'guest')
        #parameters = pika.ConnectionParameters(self.host,
        #                               5672,
        #                               '/',
        #                               credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self._callback, auto_ack=True)

    def stop(self):
        self.connection.close()

    def _callback(self, ch, method, properties, body):
        image_path = body.decode('utf-8')
        self.resize_image(image_path)
        os.remove(image_path)

    @staticmethod
    def resize_image(image_path):
        img = cv2.imread(image_path)
        resized_img = cv2.resize(img, (384, 384))
        cv2.imwrite(image_path, resized_img)
