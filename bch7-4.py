import numpy.polynomial.polynomial as nppoly
import numpy as np


def float_to_int(arr):
    int_arr = []
    for i in range(len(arr)):
        int_arr.append(int(arr[i]) % 2)  # Reduce to binary (mod 2)
    return int_arr


def shift_up(px, n=1):
    for i in range(n):
        px = nppoly.polymulx(px)
    return float_to_int(px)


def shift_down(px, n=1):
    if n >= len(px):
        raise ValueError(f"The polynomial cannot be divided by x {n} times (degree is too low).")
    return np.array(px[n:])


def poly_to_array(poly):
    result = []
    for coefficient in poly:
        result.append(coefficient)
    return result


# Data and generator polynomial
data = np.array((1, 0, 0, 0), dtype=int)  # Binary data
generator_polynomial = np.array((1, 1, 0, 1), dtype=int)  # Generator polynomial

# Convert to polynomials
print(f"Data: {data}")
data_poly = nppoly.Polynomial(data)
print(f"Data polynomial: {data_poly}")

print(f"Generator: {generator_polynomial}")
generator_polynomial_poly = nppoly.Polynomial(generator_polynomial)
print(f"Generator polynomial: {generator_polynomial_poly}")

# Shift the data polynomial up by the degree of the generator polynomial
multiplied_data = shift_up(data, np.count_nonzero(generator_polynomial))
print(f"Multiplied data: {multiplied_data}")

# Perform polynomial division, get remainder
remainder = nppoly.polydiv(multiplied_data, generator_polynomial)[1]
remainder = float_to_int(poly_to_array(remainder))  # Reduce remainder to binary (mod 2)
print(f"Remainder: {remainder}")

# Generate the codeword by adding the remainder back to the multiplied data
codeword = nppoly.polyadd(multiplied_data, remainder)
codeword = float_to_int(poly_to_array(codeword))  # Reduce codeword to binary (mod 2)
print(f"Codeword: {codeword}")
