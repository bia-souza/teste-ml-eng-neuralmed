import pika
from flask import Flask, request, jsonify
from gateway.img_resizer_queue import ImageResizer

'''
    Class responsible to manage API, containing methods:
    - start: start a Flask API and call the gateway responsible to manager queue in application
    - run: call the routes presents in API and run the API
    - _register_routes: private method that register all routes presents in API
    - _handle_resize_request: private static method that publish image in queue and handling http error
'''

class ImageResizerAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.resizer = ImageResizer(host='rabbitmq')

    def start(self):
        self.resizer.start()
        self.app.run(debug=True)

    @staticmethod
    def _handle_resize_request(self, image_file):
        if not image_file:
            return jsonify({'error': 'No image file provided'})

        image_path = 'images/' + image_file.filename
        image_file.save(image_path)

        channel = self.resizer.channel
        channel.basic_publish(exchange='', routing_key=self.resizer.queue_name, body=image_path,
                              properties=pika.BasicProperties(delivery_mode=2))  # make message persistent

        return jsonify({'success': True})

    def _register_routes(self):
        @self.app.route('/api/resize-image', methods=['POST'])
        def resize_image_api():
            return self._handle_resize_request(request.files.get('image'))

    def run(self):
        self._register_routes()
        self.start()