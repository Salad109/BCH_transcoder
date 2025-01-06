import galois
import numpy as np
import pyinputplus as pyip
from transmission_simulation import flip_random_bits, introduce_error


def encode(data, generator, n, k, output="codeword"):
    field = galois.GF(2)

    data_poly = galois.Poly(data, field=field)
    generator_poly = galois.Poly(generator, field=field)

    degree = generator_poly.degree
    shifted_data = data_poly * galois.Poly([1] + [0] * degree, field=field)

    parity_poly = shifted_data % generator_poly
    codeword_poly = shifted_data + parity_poly

    # Ensure codeword has a length of n
    codeword_coeffs = codeword_poly.coeffs
    if len(codeword_coeffs) < n:
        codeword_coeffs = np.pad(codeword_coeffs, (n - len(codeword_coeffs), 0), 'constant', constant_values=0)

    if output == "codeword":
        return codeword_coeffs
    elif output == "all":
        # Generator polynomial (no padding required)
        generator_coeffs = generator_poly.coeffs
        # Parity polynomial should be exactly n-k bits (no padding beyond n-k)
        parity_coeffs = parity_poly.coeffs
        if len(parity_coeffs) < n - k:
            parity_coeffs = np.pad(parity_coeffs, (n - k - len(parity_coeffs), 0), 'constant', constant_values=0)
        return codeword_coeffs, generator_coeffs, parity_coeffs


def validation_encode(data, n, k, output="codeword"):
    field = galois.GF(2)
    bch_code = galois.BCH(n=n, k=k, field=field)
    generator_poly = bch_code.generator_poly.coeffs
    parity_poly = bch_code.encode(data, output="parity")
    codeword_poly = bch_code.encode(data, output="codeword")
    if output == "codeword":
        return codeword_poly
    elif output == "all":
        return codeword_poly, generator_poly, parity_poly


def decode(codeword, generator, t):
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
            # Add the syndrome to the current vector
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


def validation_decode(codeword, n, k):
    field = galois.GF(2)
    bch_code = galois.BCH(n=n, k=k, field=field)
    decoded_codeword, errors = bch_code.decode(codeword, output="codeword", errors=True)
    return decoded_codeword, errors


def run_bch_interaction(bch_code):
    # Prompt the user to choose the error method
    error_method = pyip.inputMenu(
        ["Fixed number of errors", "Probability of error (BER)"],
        numbered=True,
        prompt="Choose the error method:\n"
    )

    # Get a valid string of bits
    bit_string = pyip.inputRegex(
        f"^[01]{{{bch_code.k}}}$",
        prompt=f"Enter a string of {bch_code.k} bits (0 and 1 only): "
    )
    data = [int(bit) for bit in bit_string]

    # Encode the data
    codeword_bits = bch_code.encode(data, output="codeword")
    validation_codeword_bits = bch_code.validation_encode(data, output="codeword")

    # Handle the chosen error method
    if error_method == "Fixed number of errors":
        error_count = pyip.inputInt(
            prompt=f"Enter the number of errors (integer between 0 and {bch_code.n}): ",
            min=0, max=bch_code.n
        )
        flipped_codeword_bits = flip_random_bits(codeword_bits, error_count)
        print(f"Errors introduced: {error_count}")

    elif error_method == "Probability of error (BER)":
        ber = pyip.inputFloat(
            prompt="Enter the bit error rate (float between 0.0 and 1.0): ",
            min=0.0, max=1.0
        )
        flipped_codeword_bits = introduce_error(codeword_bits, ber)
        print(f"Errors introduced based on BER: {ber}")

    # Decode the data
    decoded_bits, error_count = bch_code.decode(flipped_codeword_bits)
    validation_decoded_bits, validation_error_count = bch_code.validation_decode(flipped_codeword_bits)

    # Display results
    print("======== ENCODED DATA ========")
    print(f"Codeword: {codeword_bits}")
    print(f"Validation codeword: {validation_codeword_bits}")
    print("\n====== DATA WITH ERRORS ======")
    print(f"Codeword with errors: {flipped_codeword_bits}")
    print("\n======== DECODED DATA ========")
    print(f"Decoded codeword: {decoded_bits}, errors identified: {error_count}")
    print(f"Validation decoded codeword: {validation_decoded_bits}, errors identified: {validation_error_count}")
    print("\n======== RESULTS =============")

    if np.array_equal(codeword_bits, validation_decoded_bits):
        print("Decoding successful")
    else:
        print("Decoding failed")
