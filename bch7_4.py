import bch_utils


class BCH7_4:
    def __init__(self):
        self.n = 7
        self.k = 4
        self.t = 1
        self.generator = [1, 0, 1, 1]  # BCH generator polynomial

    def encode(self, data, output="codeword"):
        return bch_utils.encode(data, self.generator, self.n, self.k, output=output)

    def validation_encode(self, data, output="codeword"):
        return bch_utils.validation_encode(data, self.n, self.k, output=output)

    def decode(self, codeword):
        return bch_utils.decode(codeword, self.generator, self.t)

    def validation_decode(self, codeword):
        return bch_utils.validation_decode(codeword, self.n, self.k)


if __name__ == "__main__":
    bch_utils.run_bch_interaction(BCH7_4())
