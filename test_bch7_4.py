from unittest import TestCase
import numpy as np
import itertools
from transmission_simulation import flip_random_bits
import bch7_4

class Test(TestCase):
    def test_encode_bch(self, k=4):
        # Test all possible k-bit data combinations for encoding
        for data in itertools.product([0, 1], repeat=k):
            data = list(data)

            # Custom encoding
            codeword_bits, generator_bits, parity_bits = bch7_4.encode_bch(data, output="all")
            # True encoding
            true_codeword_bits, true_generator_bits, true_parity_bits = bch7_4.true_encode_bch(data, output="all")

            # Assertions for the generated codeword, generator, and parity
            assert np.array_equal(codeword_bits, true_codeword_bits), \
                f"Custom encoded codeword {codeword_bits} differs from true encoded codeword {true_codeword_bits} for data {data}"
            assert np.array_equal(generator_bits, true_generator_bits), \
                f"Custom generator {generator_bits} differs from true generator {true_generator_bits} for data {data}"
            assert np.array_equal(parity_bits, true_parity_bits), \
                f"Custom parity {parity_bits} differs from true parity {true_parity_bits} for data {data}"


    def test_decode_bch(self, k=4, t=1):
        # Test all possible k-bit data combinations for decoding with up to `t` errors
        for data in itertools.product([0, 1], repeat=k):
            data = list(data)

            # Encode data to get the codeword
            codeword_bits = bch7_4.encode_bch(data, output="codeword")

            # Introduce up to `t` random errors and test decoding
            for error_count in range(t + 1):  # Test 0, 1, ..., t bit errors
                flipped_codeword_bits = flip_random_bits(codeword_bits, error_count)

                # Decode with custom and true decoding functions
                decoded_bits, custom_error_count = bch7_4.decode_bch(flipped_codeword_bits)
                true_decoded_bits, true_error_count = bch7_4.true_decode_bch(flipped_codeword_bits)

                # Assertions
                assert np.array_equal(decoded_bits, true_decoded_bits), \
                    f"Custom decoded codeword {decoded_bits} does not match true decoded codeword {true_decoded_bits} for data {data} with {error_count} errors"
                assert custom_error_count == true_error_count, \
                    f"Error count mismatch for data {data} with {error_count} errors: custom {custom_error_count}, true {true_error_count}"
                assert np.array_equal(codeword_bits, decoded_bits), \
                    f"Decoded codeword {decoded_bits} does not match original codeword {codeword_bits} for data {data} with {error_count} errors"
