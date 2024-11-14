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

    # ======================
    # Simulation parameters
    Max_BER = 0.8
    BER_step = 0.01
    sample_size = 100

    # ======================

    def run_simulation(bch_code, max_ber, ber_step, sample_size):
        n = bch_code.n
        k = bch_code.k
        success_history = []
        ber_history = []
        current_step = 1
        ber = 0.0

        while ber + (0.01 * ber_step) <= max_ber:
            # The (0.01 * ber_step) is to account for floating point precision. Do not remove
            success_count = 0
            for attempt in range(sample_size):
                data = []
                for i in range(k):
                    data.append(random.randint(0, 1))

                encoded_data = bch_code.encode_bch(data)
                errors = introduce_error(encoded_data, ber)

                try:
                    decoded_data = bch_code.decode_bch(encoded_data)[0].tolist()[:len(data)]
                except AttributeError:
                    continue

                if decoded_data == data:
                    success_count += 1

            try:
                success_rate = success_count / sample_size
            except ZeroDivisionError:
                success_rate = 1.0
            success_history.append(success_rate)
            ber_history.append(ber)
            print(
                f"Code: BCH({n},{k})\t| BER: {ber:4.3} | Pass: {current_step} / {int(Max_BER / BER_step):4} | Success rate: {success_rate:.3}")
            ber += ber_step
            current_step += 1

        return success_history, ber_history


    # Running simulations
    bch15_7_success_history, bch15_7_BER_history = run_simulation(bch15_7, Max_BER, BER_step, sample_size)
    bch7_4_success_history, bch7_4_BER_history = run_simulation(bch7_4, Max_BER, BER_step, sample_size)

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(bch15_7_BER_history, bch15_7_success_history, color='blue', linestyle='-', linewidth=2,
             label='BCH(15,7), t=2')
    plt.plot(bch7_4_BER_history, bch7_4_success_history, color='red', linestyle='-', linewidth=2, label='BCH(7,4), t=1')

    plt.title("Success Rate vs. BER for various BCH Codes", fontsize=14, fontweight='bold')
    plt.xlabel("Bit Error Rate (BER)", fontsize=12)
    plt.xscale("log")
    plt.ylabel("Success Rate", fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(loc="upper right", prop={'size': 15})

    plt.show()
