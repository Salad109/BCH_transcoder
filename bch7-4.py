import random
import galois
import numpy as np


def encode_bch(data, generator, field):
    data_poly = galois.Poly(data, field=field)
    generator_poly = galois.Poly(generator, field=field)

    degree = generator_poly.degree
    shifted_data = data_poly * galois.Poly([1] + [0] * degree, field=field)

    parity_poly = shifted_data % generator_poly

    codeword_poly = shifted_data + parity_poly
    return generator_poly.coeffs, parity_poly.coeffs, codeword_poly.coeffs


def true_encode_bch(data):
    bch_code = galois.BCH(n=7, k=4, field=galois.GF(2))
    generator_poly = bch_code.generator_poly.coeffs
    parity_poly = bch_code.encode(data, output="parity")
    codeword_poly = bch_code.encode(data, output="codeword")
    return generator_poly, parity_poly, codeword_poly


def flip_bits(input_data, error_count=1):
    data_length = len(input_data)
    if error_count > data_length:
        raise ValueError("Not enough unique numbers in the specified range.")

    flip_indexes = random.sample(range(0, data_length), error_count)
    for index in flip_indexes:
        input_data[index] ^= 1

    return input_data

def decode_bch(codeword, generator, field, t=1):
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
        print(f"Syndrome: {syndrome}, Hamming weight: {hamming_weight}")

        if hamming_weight <= t:
            # Correction: add the syndrome to the current vector
            corrected_codeword = (codeword_poly + syndrome_poly).coeffs
            # Restore the original position only if there was a shift
            if i > 0:
                corrected_codeword = np.roll(corrected_codeword, -i)
            print(f"Corrected codeword: {corrected_codeword}")
            return corrected_codeword, hamming_weight  # Return the corrected code and the number of errors

        # Cyclic shift to the right
        codeword_poly = galois.Poly(np.roll(codeword, i + 1), field=field)
        print(f"Codeword after {i + 1}-th shift: {codeword_poly.coeffs}")

    # If correction is not possible
    print("Uncorrectable errors")
    return None, None


def true_decode_bch(input_data, field):
    bch_code = galois.BCH(n=7, k=4, field=field)
    decoded_codeword, errors = bch_code.decode(input_data, output="codeword", errors=True)
    return decoded_codeword, errors


# ============================
data = [1, 0, 0, 1]
generator = [1, 0, 1, 1]
error_count = 1
field = galois.GF(2)

generator_bits, parity_bits, codeword_bits = encode_bch(data, generator, field)
print(f"Generator: {generator_bits}")
print(f"Parity bits: {parity_bits}")
print(f"Codeword: {codeword_bits}")
print("-------------------------------")
true_gen_poly, true_parity_bits, true_codeword_bits = true_encode_bch(data)
print(f"True generator: {true_gen_poly}")
print(f"True parity bits: {true_parity_bits}")
print(f"True codeword: {true_codeword_bits}")

assert codeword_bits.all() == true_codeword_bits.all()
print("===============================")

codeword_bits = flip_bits(codeword_bits, error_count)
print(f"Errors introduced: {error_count}")
print(f"Codeword with errors: {codeword_bits}")
print("===============================")

decoded_bits, error_count = decode_bch(codeword_bits, generator_bits, field)
true_decoded_bits, true_error_count = true_decode_bch(codeword_bits, field)
print(f"Decoded codeword: {decoded_bits}, errors identified: {error_count}")
print(f"True decoded codeword: {true_decoded_bits}, errors identified: {true_error_count}")
