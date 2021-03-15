import os
import app
import unittest
import cv2
from io import BytesIO
from app import extract_data, resize_image

PATH = "C:/Users/naren/PycharmProjects/imagenA4/files/taiwan.jpg"


class AppTestCase(unittest.TestCase):

    def setUp(self):
        print("===> Setting up the env for test")
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_index(self):
        resp = self.app.get('/')
        assert "200 OK" == resp.status

    def test_uploader(self):
        data = {'image': (BytesIO(b'FILE CONTENT'), 'taiwan.jpg')}
        rv = self.app.post("/uploader", buffered=True, content_type='multipart/form-data', data=data)
        assert rv.status == "200 OK"

    def test_extract_data(self):
        image = cv2.imread(PATH)
        orientation, height, wide = extract_data(image)
        self.assertEqual(orientation, "Horizontal")
        self.assertEqual(height, 272)
        self.assertEqual(wide, 1155)

    def test_resize_image(self):
        image = cv2.imread(PATH)
        orientation, resize = resize_image(image)
        self.assertEqual(orientation, "Horizontal")
        self.assertEqual(resize, (1123, 264))


if __name__ == '__main__':
    unittest.main()
