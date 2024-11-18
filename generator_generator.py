import galois

n = 127
k = 8

bch_code = galois.BCH(n=n, k=k, field=galois.GF(2))
generator_poly = bch_code.generator_poly.coeffs
print(generator_poly.tolist())
