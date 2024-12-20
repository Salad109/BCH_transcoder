import bch_utils


class BCH31_6:
    def __init__(self):
        self.n = 31
        self.k = 6
        self.t = 7
        self.generator = [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, ]

    def encode(self, data, output="codeword"):
        return bch_utils.encode(data, self.generator, self.n, self.k, output=output)

    def validation_encode(self, data, output="codeword"):
        return bch_utils.validation_encode(data, self.n, self.k, output=output)

    def decode(self, codeword):
        return bch_utils.decode(codeword, self.generator, self.t)

    def validation_decode(self, codeword):
        return bch_utils.validation_decode(codeword, self.n, self.k)


if __name__ == "__main__":
    bch_utils.run_bch_interaction(BCH31_6())
