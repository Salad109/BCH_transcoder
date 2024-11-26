import galois
import numpy as np
from transmission_simulation import flip_random_bits

n = 15
k = 7
t = 2
generator = [1, 1, 1, 0, 1, 0, 0, 0, 1]  # BCH generator polynomial


def encode_bch(data, output="codeword"):
    field = galois.GF(2)
    data_poly = galois.Poly(data, field=field)
    generator_poly = galois.Poly(generator, field=field)

    degree = generator_poly.degree
    shifted_data = data_poly * galois.Poly([1] + [0] * degree, field=field)

    parity_poly = shifted_data % generator_poly
    codeword_poly = shifted_data + parity_poly

    # Ensure codeword has a length of 15
    codeword_coeffs = codeword_poly.coeffs
    if len(codeword_coeffs) < n:
        codeword_coeffs = np.pad(codeword_coeffs, (n - len(codeword_coeffs), 0), 'constant', constant_values=0)

    if output == "codeword":
        return codeword_coeffs
    elif output == "all":
        # Generator polynomial (no padding required)
        generator_coeffs = generator_poly.coeffs
        # Parity polynomial should be exactly 8 bits (no padding beyond 8)
        parity_coeffs = parity_poly.coeffs
        if len(parity_coeffs) < n - k:
            parity_coeffs = np.pad(parity_coeffs, (n - k - len(parity_coeffs), 0), 'constant', constant_values=0)
        return codeword_coeffs, generator_coeffs, parity_coeffs


def true_encode_bch(data, output="codeword"):
    field = galois.GF(2)
    bch_code = galois.BCH(n=n, k=k, field=field)
    generator_poly = bch_code.generator_poly.coeffs
    parity_poly = bch_code.encode(data, output="parity")
    codeword_poly = bch_code.encode(data, output="codeword")
    if (output == "codeword"):
        return codeword_poly
    elif (output == "all"):
        return codeword_poly, generator_poly, parity_poly


def decode_bch(codeword, t=2):
    field = galois.GF(2)
    codeword_poly = galois.Poly(codeword, field=field)
    generator_poly = galois.Poly(generator, field=field)
    max_shifts = len(codeword)  # maximum number of cyclic shifts

    for i in range(max_shifts):
        # Calculate the syndrome as the remainder of the division by the generator polynomial
        syndrome_poly = codeword_poly % generator_poly
        syndrome = syndrome_poly.coeffs

        # Pad the syndrome to the required length (if necessary)
        while len(syndrome) < len(generator) - 1:
            syndrome = np.append(syndrome, field(0))

        # Calculate the Hamming weight of the syndrome
        hamming_weight = sum(1 for s in syndrome if s != field(0))
        # print(f"Syndrome: {syndrome}, Hamming weight: {hamming_weight}")

        if hamming_weight <= t:
            # Correction: add the syndrome to the current vector
            corrected_codeword = (codeword_poly + syndrome_poly).coeffs
            # Restore the original position only if there was a shift
            # Ensure corrected_codeword has the same length as codeword
            if len(corrected_codeword) < len(codeword):
                # Add zeros to the start of corrected_codeword
                corrected_codeword = np.pad(corrected_codeword, (len(codeword) - len(corrected_codeword), 0),
                                            'constant', constant_values=0)
            if i > 0:
                corrected_codeword = np.roll(corrected_codeword, -i)
            # print(f"Corrected codeword: {corrected_codeword}")
            return corrected_codeword, hamming_weight  # Return the corrected code and the number of errors

        # Cyclic shift to the right
        codeword_poly = galois.Poly(np.roll(codeword, i + 1), field=field)
        # print(f"Codeword after {i + 1}-th shift: {codeword_poly.coeffs}")

    # If correction is not possible
    # print("Uncorrectable errors")
    return None, None


def true_decode_bch(input_data):
    field = galois.GF(2)
    bch_code = galois.BCH(n=n, k=k, field=field)
    decoded_codeword, errors = bch_code.decode(input_data, output="codeword", errors=True)
    return decoded_codeword, errors


# ============================
if __name__ == "__main__":
    data = [1, 0, 1, 0, 1, 0, 1]
    error_count = t

    codeword_bits, generator_bits, parity_bits = encode_bch(data, output="all")
    print(f"Codeword: {codeword_bits}")
    print(f"Generator: {generator_bits}")
    print(f"Parity bits: {parity_bits}")
    print("-------------------------------")
    true_codeword_bits, true_generator_bits, true_parity_bits = true_encode_bch(data, output="all")
    print(f"True codeword: {true_codeword_bits}")
    print(f"True generator: {true_generator_bits}")
    print(f"True parity bits: {true_parity_bits}")
    print("===============================")

    flipped_codeword_bits = flip_random_bits(codeword_bits, error_count)
    print(f"Errors introduced: {error_count}")
    print(f"Codeword with errors: {flipped_codeword_bits}")
    print("===============================")

    decoded_bits, error_count = decode_bch(flipped_codeword_bits, t)
    true_decoded_bits, true_error_count = true_decode_bch(flipped_codeword_bits)
    print(f"Decoded codeword: {decoded_bits}, errors identified: {error_count}")
    print(f"True decoded codeword: {true_decoded_bits}, errors identified: {true_error_count}")
