from math import log
from pathlib import PosixPath

from bitarray import bitarray, decodetree
import cv2


class Tunstall:
    def __init__(self, k=2):
        self.k = k
        self.dictionary_size = 2 ** k - 1
        self.stats = {}

    def _count_symbols(self, data: bytes, image_path: PosixPath) -> dict:
        hist = {}
        get = hist.get
        for i in data:
            b = i.to_bytes(1, 'big')
            hist[b] = get(b, 0) + 1

        import matplotlib.pyplot as plt
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        cv2.imshow('Cat', img)

        dst = cv2.calcHist(img, [0], None, [256], [0, 256])

        plt.hist(img.ravel(), 256, [0, 256])
        plt.title(f'Histogram for gray scale image {image_path}')
        plt.savefig('plots/' + image_path.stem + '_histogram.jpg')
        plt.close()
        return hist

    def _construct_tree(self, data: bytes, image_path: PosixPath) -> dict:
        hist = self._count_symbols(data, image_path)
        # self.stats['histogram'] = hist

        initial_tree = {
            symbol: count / len(data) for symbol, count in hist.items()
        }

        entropy = self._calculate_entropy(list(initial_tree.values()))
        self.stats['entropy'] = entropy

        new_leaves_count = len(initial_tree) - 1

        final_tree = {}
        final_tree.update(initial_tree)

        while len(final_tree) + new_leaves_count <= self.dictionary_size:
            probablest_symbol = max(final_tree,
                                    key=final_tree.get)
            probability = final_tree.pop(probablest_symbol)

            offspring = {probablest_symbol + sym: probability * prob for
                         sym, prob in initial_tree.items()}

            final_tree.update(offspring)

        avg_bit_len = self._calculate_avg_bit_length(list(final_tree.keys()))
        self.stats['avg_bit_length'] = avg_bit_len

        return final_tree

    def _create_encoding(self, codewords: list):
        encoding = {}
        for i, char in enumerate(codewords):
            if i >= self.dictionary_size:
                break
            encoding[char] = bitarray(format(i, f'0{self.k}b'))
        return encoding

    def encode(self, data: bytes) -> tuple[dict, bitarray, bytes]:
        probability_tree = self._construct_tree(data)
        encoding = self._create_encoding(list(probability_tree.keys()))

        encoded_chars = []
        curr_text = b''

        for i in data:
            curr_text += i.to_bytes(1, 'big')
            if curr_text in encoding:
                encoded_chars.append(encoding[curr_text])
                curr_text = b''

        encoded_bits = bitarray()
        for code in encoded_chars:
            encoded_bits += code

        self.stats['encoded_size'] = len(encoded_bits.tobytes())

        keystr = b''
        for key in encoding.keys():
            keystr += key
        valbitarr = bitarray()
        for val in encoding.values():
            valbitarr += val

        encoding_size = len(keystr) + len(valbitarr.tobytes())
        self.stats['encoding_size'] = encoding_size

        self.stats['unencoded_size'] = len(curr_text)
        self.stats['original_size'] = len(data)

        return encoding, encoded_bits, curr_text

    def decode(self, encoding: dict, encoded_bits: bitarray,
               unencoded_bytes: bytes = None) -> bytes:

        t = decodetree(encoding)
        decoded_bytes = encoded_bits.decode(t)
        if unencoded_bytes:
            decoded_bytes.append(unencoded_bytes)

        return b''.join(decoded_bytes)

    def _calculate_entropy(self, probabilities: list) -> float:
        ent = 0.
        for i in probabilities:
            ent -= i * log(i, 2)
        return ent

    def _calculate_avg_bit_length(self, codewords: list) -> float:
        lengths = [len(word) * 8 for word in codewords]
        return sum(lengths) / len(codewords)

    def get_result(self) -> dict:
        return self.stats
