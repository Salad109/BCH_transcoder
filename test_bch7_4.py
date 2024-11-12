from unittest import TestCase
import random
import numpy as np
import bch7_4


class Test(TestCase):
    def test_encode_bch(self, k=4):
        # Build a sample data set consisting of all 1s, all 0s, and 98 random samples
        data_samples = [[0, 0, 0, 0], [1, 1, 1, 1]]  # Edge cases
        for i in range(98):
            sample = []
            for j in range(k):
                sample.append(random.randint(0, 1))

            data_samples.append(sample)

        for data_sample in data_samples:
            # Custom encoding
            codeword_bits, generator_bits, parity_bits = bch7_4.encode_bch(data_sample, output="all")
            # True encoding
            true_codeword_bits, true_generator_bits, true_parity_bits = bch7_4.true_encode_bch(data_sample,
                                                                                               output="all")
            # Assertions for the generated codeword, generator, and parity
            assert np.array_equal(codeword_bits, true_codeword_bits), \
                f"Custom encoded codeword {codeword_bits} differs from true encoded codeword {true_codeword_bits} for data {data_sample}"

    def test_decode_bch(self, k=4):
        assert 1 == 1
        # TODO Użyć assertów aby porównać decode_bch i true_decode bch, oraz ilość wykrytych błędów z rzeczywistymi.
