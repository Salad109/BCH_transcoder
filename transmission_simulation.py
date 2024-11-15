import random
import time


def flip_random_bits(input_data, error_count=1):
    flipped_data = input_data.copy()
    data_length = len(flipped_data)
    if error_count > data_length:
        raise ValueError("Not enough unique numbers in the specified range.")

    flip_indexes = random.sample(range(0, data_length), error_count)
    for index in flip_indexes:
        flipped_data[index] ^= 1

    return flipped_data


def introduce_error(input_data, ber=0.1):
    errors = input_data.copy()
    for i in range(len(errors)):
        if random.random() <= ber:  # Flip the bit with probability = BER
            errors[i] ^= 1
    return errors


if __name__ == "__main__":
    import bch31_6
    import bch15_7
    import bch7_4
    import matplotlib.pyplot as plt


    def run_simulation(bch_code, max_ber=1.0, ber_step=0.05, sample_size=100, patience_count=5, patience_threshold=0.0):
        n = bch_code.n
        k = bch_code.k
        success_history = []
        ber_history = []
        current_step = 0
        ber = 0.0

        while ber + (0.01 * ber_step) <= max_ber:
            # The (0.01 * ber_step) is to account for floating point precision. Do not remove
            start_time = time.perf_counter()
            success_count = 0
            for attempt in range(sample_size):
                data = []
                for i in range(k):
                    data.append(random.randint(0, 1))

                encoded_data = bch_code.encode_bch(data)
                error_data = introduce_error(encoded_data, ber)

                try:
                    decoded_data = bch_code.decode_bch(error_data)[0].tolist()[:len(data)]
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
            ber += ber_step
            current_step += 1
            total_epoch_time = time.perf_counter() - start_time

            print(
                f"Code: BCH({n},{k})\t| BER: {ber:4.3} | Epoch: {current_step:4} / {int(Max_BER / BER_step):4} | Success rate: {success_rate:5.4} | Time: {total_epoch_time:5.3}s")

            # Early stopping
            if len(success_history) > patience_count and all(
                    rate <= patience_threshold for rate in success_history[-patience_count:]):
                print("Early stopping!")
                break

        return success_history, ber_history


    def run_simulation_baseline(k, max_ber=1.0, ber_step=0.05, sample_size=100, patience_count=5,
                                patience_threshold=0.0):
        success_history = []
        ber_history = []
        current_step = 0
        ber = 0.0

        while ber + (0.01 * ber_step) <= max_ber:
            # The (0.01 * ber_step) is to account for floating point precision. Do not remove
            start_time = time.perf_counter()
            success_count = 0
            for attempt in range(sample_size):
                data = []
                for i in range(k):
                    data.append(random.randint(0, 1))

                error_data = introduce_error(data, ber)

                if error_data == data:
                    success_count += 1

            try:
                success_rate = success_count / sample_size
            except ZeroDivisionError:
                success_rate = 1.0

            success_history.append(success_rate)
            ber_history.append(ber)
            ber += ber_step
            current_step += 1
            total_epoch_time = time.perf_counter() - start_time

            print(
                f"Code: No encoding (k={k})\t| BER: {ber:4.3} | Epoch: {current_step:4} / {int(Max_BER / BER_step):4} | Success rate: {success_rate:5.4} | Time: {total_epoch_time:5.3}s")

            # Early stopping
            if len(success_history) > patience_count and all(
                    rate <= patience_threshold for rate in success_history[-patience_count:]):
                print("Early stopping!")
                break

        return success_history, ber_history


    # Simulation parameters
    Max_BER = 1.0  # Maximum bit error rate to test for(assuming it won't be terminated first by early stopping)
    BER_step = 0.015  # BER step value
    message_sample_size = 1000  # How many randomized messages to send per BER value
    patience = 5  # Stop after this many epochs' success rate is smaller or equal to patience_value
    patience_value = 0.0

    # Running simulations
    simulation_start_time = time.perf_counter()
    bch31_6_success_history, bch31_6_BER_history = run_simulation(bch_code=bch31_6,
                                                                  max_ber=Max_BER,
                                                                  ber_step=BER_step,
                                                                  sample_size=message_sample_size,
                                                                  patience_count=patience,
                                                                  patience_threshold=patience_value)
    bch15_7_success_history, bch15_7_BER_history = run_simulation(bch_code=bch15_7,
                                                                  max_ber=Max_BER,
                                                                  ber_step=BER_step,
                                                                  sample_size=message_sample_size,
                                                                  patience_count=patience,
                                                                  patience_threshold=patience_value)
    bch7_4_success_history, bch7_4_BER_history = run_simulation(bch_code=bch7_4,
                                                                max_ber=Max_BER,
                                                                ber_step=BER_step,
                                                                sample_size=message_sample_size,
                                                                patience_count=patience,
                                                                patience_threshold=patience_value)
    baseline_success_history, baseline_BER_history = run_simulation_baseline(k=7,
                                                                             max_ber=Max_BER,
                                                                             ber_step=BER_step,
                                                                             sample_size=message_sample_size,
                                                                             patience_count=patience,
                                                                             patience_threshold=patience_value)
    total_time = time.perf_counter() - simulation_start_time
    print(f"Simulation took {int(total_time // 60)} minutes and {total_time % 60:.2f} seconds")

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(bch31_6_BER_history, bch31_6_success_history, color='red', linestyle='-', linewidth=2,
             label='BCH(31,6), t=7')
    plt.plot(bch15_7_BER_history, bch15_7_success_history, color='green', linestyle='-', linewidth=2,
             label='BCH(15,7), t=2')
    plt.plot(bch7_4_BER_history, bch7_4_success_history, color='blue', linestyle='-', linewidth=2,
             label='BCH(7,4), t=1')
    plt.plot(baseline_BER_history, baseline_success_history, color='black', linestyle='-', linewidth=2,
             label='No encoding (7,7), t=0')

    plt.title("Success Rate vs. BER for various BCH Codes", fontsize=14, fontweight='bold')
    plt.xlabel("Bit Error Rate (BER)", fontsize=12)
    plt.ylabel("Success Rate", fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(loc="upper right", prop={'size': 15})

    plt.show()
