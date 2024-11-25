import unittest
import numpy as np
import bch15_11


class TestBCH15_11(unittest.TestCase):
    def setUp(self):
        self.data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
        self.bad_codes = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1]]
        self.messages = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1],
                         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]

    def test_bch_encoding(self):
        for test in self.data:
            with self.subTest(test=test):
                true_encoded_data = bch15_11.true_encode_bch(test, "codeword")
                our_encoded_data = bch15_11.encode_bch(test, "codeword")
                self.assertTrue(np.array_equal(our_encoded_data, true_encoded_data),
                                f"Encoding does not match for input {test}")

    def test_bch_decoding(self):
        for bad_code, message in zip(self.bad_codes, self.messages):
            with self.subTest(bad_code=bad_code, message=message):
                true_decoded_data = bch15_11.true_decode_bch(bad_code)[0][:bch15_11.k].tolist()
                decoded_data = bch15_11.decode_bch(bad_code)[0][:bch15_11.k].tolist()
                self.assertTrue(np.array_equal(decoded_data[:len(message)], message),
                                f"Bad decoding for input {bad_code}")
                self.assertTrue(np.array_equal(true_decoded_data, decoded_data),
                                f"Decoding does not match for input {bad_code}")


if __name__ == '__main__':
    unittest.main()
