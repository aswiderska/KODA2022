from pathlib import Path

from tunstall import Tunstall


class Test(TestCase):
    def setUp(self) -> None:
        self.tun = Tunstall()

    def test_calculate_probabilities(self):
        self.tun = Tunstall(k=3)
        self.assertAlmostEqual(9 / 50,
                               self.tun._construct_tree(b'ABCABABAAA')[b'AB'])
        self.assertAlmostEqual(1 / 4, self.tun._construct_tree(b'ABBC')[b'C'])

        self.tun = Tunstall(k=4)
        self.assertAlmostEqual(9 / 121,
                               self.tun._construct_tree(b'hello_world')[b'll'])

    def test_encode_decode(self):
        file = Path('data/obrazy/lena.pgm')
        content = file.read_bytes()

        encoding, encoded_bits, unencoded_bytes = self.tun.encode(content)
        decoded = self.tun.decode(encoding, encoded_bits, unencoded_bytes)
        self.assertEqual(content, decoded)
