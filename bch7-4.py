import galois


def encode_bch(input_data, gen_poly):
    gf2 = galois.GF(2)
    data_polynomial = galois.Poly(input_data, field=gf2)
    generator_polynomial = galois.Poly(gen_poly, field=gf2)

    degree = generator_polynomial.degree
    shifted_data = data_polynomial * galois.Poly([1] + [0] * degree, field=gf2)

    parity_poly = shifted_data % generator_polynomial

    codeword_poly = shifted_data + parity_poly
    return generator_polynomial.coeffs, parity_poly.coeffs, codeword_poly.coeffs


# ============================

def true_encode_bch(input_data):
    bch_code = galois.BCH(n=7, k=4, field=galois.GF(2))
    true_gen_poly = bch_code.generator_poly.coeffs
    true_parity_poly = bch_code.encode(input_data, output="parity")
    true_codeword_poly = bch_code.encode(input_data, output="codeword")
    return true_gen_poly, true_parity_poly, true_codeword_poly


# ============================
data_bits = [1, 0, 0, 1]
gen_poly_bits = [1, 0, 1, 1]

gen_poly, parity_bits, codeword_bits = encode_bch(data_bits, gen_poly_bits)
print(f"Generator: {gen_poly}")
print(f"Parity: {parity_bits}")
print(f"Codeword: {codeword_bits}")

true_gen_poly, true_parity_bits, true_codeword_bits = true_encode_bch(data_bits)
print(f"True generator: {true_gen_poly}")
print(f"True parity: {true_parity_bits}")
print(f"True codeword: {true_codeword_bits}")

assert gen_poly.all() == true_gen_poly.all()
assert parity_bits.all() == true_parity_bits.all()
assert codeword_bits.all() == true_codeword_bits.all()
