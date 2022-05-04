from pathlib import Path
from unittest import TestCase

from tunstall import Tunstall


class Test(TestCase):
    def test_calculate_probabilities(self):
        tun = Tunstall(k=3)
        self.assertAlmostEqual(9 / 50,
                               tun._construct_tree(b'ABCABABAAA')[b'AB'])
        self.assertAlmostEqual(1 / 4, tun._construct_tree(b'ABBC')[b'C'])

        tun = Tunstall(k=4)
        self.assertAlmostEqual(9 / 121,
                               tun._construct_tree(b'hello_world')[b'll'])

    def test_encode_decode_iamges(self):
        images_dir = Path('./data/obrazy')
        for image in images_dir.iterdir():
            content = image.read_bytes()

            tun = Tunstall(k=8)
            args = tun.encode(content)
            decoded = tun.decode(*args)
            self.assertEqual(content, decoded)

    def test_encode_decode_data(self):
        data_dir = Path('./data/rozklady')
        for data in data_dir.iterdir():
            content = data.read_bytes()

            tun = Tunstall(k=8)
            args = tun.encode(content)
            decoded = tun.decode(*args)
            self.assertEqual(content, decoded)
