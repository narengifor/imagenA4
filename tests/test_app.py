import app
import unittest
import cv2
from app import extract_data, resize_image
from werkzeug.datastructures import FileStorage

# PATH_BASE = "C:/Users/naren/PycharmProjects/imagenA4/files/"
IMAGES_TEST = [["C:/Users/naren/PycharmProjects/imagenA4/files/taiwan.jpg", "Horizontal", 272, 1155, (1123, 264)],
               ["C:/Users/naren/PycharmProjects/imagenA4/files/300x300.jpg", "Cuadrada", 300, 300, (300, 300)]]


class AppTestCase(unittest.TestCase):

    def setUp(self):
        print("===> Setting up the env for test")
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_index(self):
        resp = self.app.get('/')
        assert "200 OK" == resp.status

    def test_uploader(self):
        # data = {'image': (BytesIO(b'FILE CONTENT'), 'taiwan.jpg')}
        for img in IMAGES_TEST:
            PATH = img[0]
            with open(PATH, 'rb') as fp:
                file = FileStorage(fp)
                data = {'image': file}
                rv = self.app.post("/uploader", buffered=True, content_type='multipart/form-data', data=data)
                assert rv.status == "200 OK"

    def test_extract_data(self):
        for img in IMAGES_TEST:
            PATH = img[0]
            image = cv2.imread(PATH)
            orientation, height, wide = extract_data(image)
            self.assertEqual(orientation, img[1])
            self.assertEqual(height, img[2])
            self.assertEqual(wide, img[3])

    def test_resize_image(self):
        for img in IMAGES_TEST:
            PATH = img[0]
            image = cv2.imread(PATH)
            orientation, resize = resize_image(image)
            self.assertEqual(orientation, img[1])
            self.assertEqual(resize, img[4])


if __name__ == '__main__':
    unittest.main()
