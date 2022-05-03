from bitarray import bitarray, decodetree


class Tunstall:
    def __init__(self, k=2):
        self.k = k
        self.dictionary_size = 2 ** k - 1
        self.stats = {}

    def _count_symbols(self, data: bytes) -> dict:
        hist = {}
        get = hist.get
        for i in data:
            b = i.to_bytes(1, 'big')
            hist[b] = get(b, 0) + 1
        return hist

    def _construct_tree(self, data: bytes) -> dict:
        hist = self._count_symbols(data)

        initial_tree = {
            symbol: count / len(data) for symbol, count in hist.items()
        }

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

        return encoding, encoded_bits, curr_text

    def decode(self, encoding: dict, encoded_bits: bitarray,
               unencoded_bytes: bytes = None) -> bytes:

        t = decodetree(encoding)
        decoded_bytes = encoded_bits.decode(t)
        if unencoded_bytes:
            decoded_bytes.append(unencoded_bytes)

        return b''.join(decoded_bytes)
