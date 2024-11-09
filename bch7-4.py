import random
import galois


def encode_bch(data, generator):
    gf2 = galois.GF(2)
    data_poly = galois.Poly(data, field=gf2)
    generator_poly = galois.Poly(generator, field=gf2)

    degree = generator_poly.degree
    shifted_data = data_poly * galois.Poly([1] + [0] * degree, field=gf2)

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


def decode_bch(input_data, generator):
    gf2 = galois.GF(2)
    data_poly = galois.Poly(input_data, field=gf2)
    generator_poly = galois.Poly(generator, field=gf2)

    syndrome = data_poly % generator_poly
    if syndrome == 0:
        return data_poly.coeffs, 0

    # TODO
    return 0, 0


def true_decode_bch(input_data):
    bch_code = galois.BCH(n=7, k=4, field=galois.GF(2))
    decoded_codeword, errors = bch_code.decode(input_data, output="codeword", errors=True)
    return decoded_codeword, errors


# ============================
data_bits = [1, 0, 0, 1]
gen_poly_bits = [1, 0, 1, 1]
error_count = 1

gen_poly, parity_bits, codeword_bits = encode_bch(data_bits, gen_poly_bits)
print(f"Generator: {gen_poly}")
print(f"Parity bits: {parity_bits}")
print(f"Codeword: {codeword_bits}")
print("===============================")

true_gen_poly, true_parity_bits, true_codeword_bits = true_encode_bch(data_bits)
print(f"True generator: {true_gen_poly}")
print(f"True parity bits: {true_parity_bits}")
print(f"True codeword: {true_codeword_bits}")
print("===============================")

true_codeword_bits = flip_bits(true_codeword_bits, error_count)
codeword_bits = flip_bits(codeword_bits, error_count)
print(f"Errors introduced: {error_count}")
print(f"Codeword with errors: {codeword_bits}")
print(f"True codeword with errors: {codeword_bits}")
print("===============================")

decoded_bits, error_count = decode_bch(codeword_bits, gen_poly_bits)
true_decoded_bits, true_errors = true_decode_bch(true_codeword_bits)
print(f"Decoded codeword: {decoded_bits}, errors identified: {error_count}")
print(f"True decoded codeword: {true_decoded_bits}, errors identified: {true_errors}")
