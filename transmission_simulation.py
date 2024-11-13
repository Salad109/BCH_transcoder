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
    import bch7_4
    import matplotlib.pyplot as plt

    Max_BER = 0.6
    BER_step = 0.01
    sample_size = 100
    success_history_15_7 = []
    success_history_7_4 = []
    BER_history = []

    BER = 0
    while BER <= Max_BER:
        success_count = 0
        for attempt in range(sample_size):
            data = []
            for i in range(7):
                data.append(random.randint(0, 1))

            encoded_data = bch15_7.encode_bch(data)
            errors = introduce_error(encoded_data, BER)

            try:
                decoded_data = bch15_7.decode_bch(encoded_data)[0].tolist()[:len(data)]
            except AttributeError:
                continue

            if decoded_data == data:
                success_count += 1

        try:
            success_rate = success_count / sample_size
        except ZeroDivisionError:
            success_rate = 1.0
        success_history_15_7.append(success_rate)
        BER_history.append(BER)
        print(f"Success rate: {success_rate}")
        BER += BER_step

    BER = 0
    while BER <= Max_BER:
        success_count = 0
        for attempt in range(sample_size):
            data = []
            for i in range(7):
                data.append(random.randint(0, 1))

            encoded_data = bch7_4.encode_bch(data)
            errors = introduce_error(encoded_data, BER)

            try:
                decoded_data = bch7_4.decode_bch(encoded_data)[0].tolist()[:len(data)]
            except AttributeError:
                continue

            if decoded_data == data:
                success_count += 1

        try:
            success_rate = success_count / sample_size
        except ZeroDivisionError:
            success_rate = 1.0
        success_history_7_4.append(success_rate)
        print(f"Success rate: {success_rate}")
        BER += BER_step
    print(success_history_15_7)

    # Plotting
    plt.figure(figsize=(10, 6))  # Increase figure size for readability

    # Plot the BCH(15,7) results
    plt.plot(BER_history, success_history_15_7, color='blue', linestyle='-', linewidth=2, label='BCH(15,7), t=2')

    # Plot the BCH(7,4) results
    plt.plot(BER_history, success_history_7_4, color='red', linestyle='-', linewidth=2, label='BCH(7,4), t=1')

    # Add titles and labels
    plt.title("Success Rate vs. BER for various BCH Codes", fontsize=14, fontweight='bold')
    plt.xlabel("Bit Error Rate (BER)", fontsize=12)
    plt.ylabel("Success Rate", fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5)  # Add dashed grid lines
    plt.legend(loc="upper right", prop={'size': 15})  # Add a legend

    # Show the final plot
    plt.show()
