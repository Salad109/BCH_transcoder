import random


def flip_random_bits(input_data, error_count=1):
    flipped_data = input_data.copy()
    data_length = len(flipped_data)
    if error_count > data_length:
        raise ValueError("Not enough unique numbers in the specified range.")

    flip_indexes = random.sample(range(0, data_length), error_count)
    for index in flip_indexes:
        flipped_data[index] ^= 1

    return flipped_data


def introduce_error(input_data, BER=0.1):
    errors = 0
    for i in range(len(input_data)):
        if random.random() <= BER:  # Bit Error Rate
            input_data[i] ^= 1
            errors += 1
    return errors


if __name__ == "__main__":
    import bch15_7

    data = [1, 0, 1, 0, 1, 0, 1]
    BER = 0.15

    encoded_data = bch15_7.encode_bch(data)
    errors = introduce_error(encoded_data, BER)

    decoded_data = bch15_7.decode_bch(encoded_data)[0].tolist()[:len(data)]

    print(errors)
    print(data)
    print(decoded_data)
