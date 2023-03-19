import os
import unittest
from ..app import app


class ImageResizerTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.remove('images/resized_test_image.jpg')

    def test_image_resize(self):
        '''
            Verify if image was correctly saved
        '''

        with open('test_image.jpg', 'rb') as f:
            image_data = f.read()

        response = self.app.post('/api/resize-image', data={'image': ('test_image.jpg', image_data)})
        self.assertEqual(response.status_code, 200)

        self.assertTrue(os.path.isfile('images/resized_test_image.jpg'),"The image was not resized")

if __name__ == '__main__':
    unittest.main()
