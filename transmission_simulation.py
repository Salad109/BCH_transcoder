import csv
import numpy as np
import random
import time

import bch127_8
import bch15_11
import bch15_5
import bch15_7
import bch31_6
import bch7_4
import config


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
        if random.random() <= ber:
            errors[i] ^= 1
    return errors


def run_simulation(k, bch_code=None, max_ber=1.0, ber_step=0.05, sample_size=100, patience_count=5,
                   patience_threshold=0.0):
    success_history = []
    ber_history = []
    current_step = 0
    ber = 0.0

    while round(ber, 10) <= max_ber:
        start_time = time.perf_counter()
        success_count = 0

        for _ in range(sample_size):
            data = np.random.randint(2, size=k)

            if bch_code is not None:
                encoded_data = bch_code.encode(data)
                error_data = introduce_error(encoded_data, ber)
                decoded_data = bch_code.decode(error_data)

                if decoded_data[0] is not None and np.array_equal(decoded_data[0][:len(data)], data):
                    success_count += 1
            else:
                error_data = introduce_error(data, ber)
                if np.array_equal(error_data, data):
                    success_count += 1

        success_rate = success_count / sample_size
        success_history.append(success_rate)
        ber_history.append(ber)
        current_step += 1
        epoch_time = time.perf_counter() - start_time

        if bch_code is not None:
            print(
                f"Code: BCH({bch_code.n},{bch_code.k}) | BER: {ber:.3f} | Step: {current_step:4d} | Success Rate: {success_rate:.4f} | Time: {epoch_time:.3f}s")
        else:
            print(
                f"Code: No encoding (k={k}) | BER: {ber:.3f} | Step: {current_step:4d} | Success Rate: {success_rate:.4f} | Time: {epoch_time:.3f}s")

        if len(success_history) >= patience_count and all(
                rate <= patience_threshold for rate in success_history[-patience_count:]):
            print("Early stopping triggered!")
            break

        ber += ber_step

    return success_history, ber_history


if __name__ == "__main__":
    print("Starting BCH simulation...")
    print(f"Max BER: {config.MAX_BER}, Step: {config.BER_STEP}, Samples: {config.SAMPLE_SIZE}")

    simulation_start_time = time.perf_counter()

    # Initialize BCH codes
    bch127_8 = bch127_8.BCH127_8()
    bch31_6 = bch31_6.BCH31_6()
    bch15_5 = bch15_5.BCH15_5()
    bch15_7 = bch15_7.BCH15_7()
    bch15_11 = bch15_11.BCH15_11()
    bch7_4 = bch7_4.BCH7_4()

    # Run simulations
    bch127_8_success, bch127_8_ber = run_simulation(bch127_8.k, bch127_8, config.MAX_BER, config.BER_STEP,
                                                    config.SAMPLE_SIZE, config.PATIENCE, config.THRESHOLD)
    bch31_6_success, bch31_6_ber = run_simulation(bch31_6.k, bch31_6, config.MAX_BER, config.BER_STEP,
                                                  config.SAMPLE_SIZE, config.PATIENCE, config.THRESHOLD)
    bch15_5_success, bch15_5_ber = run_simulation(bch15_5.k, bch15_5, config.MAX_BER, config.BER_STEP,
                                                  config.SAMPLE_SIZE, config.PATIENCE, config.THRESHOLD)
    bch15_7_success, bch15_7_ber = run_simulation(bch15_7.k, bch15_7, config.MAX_BER, config.BER_STEP,
                                                  config.SAMPLE_SIZE, config.PATIENCE, config.THRESHOLD)
    bch15_11_success, bch15_11_ber = run_simulation(bch15_11.k, bch15_11, config.MAX_BER, config.BER_STEP,
                                                    config.SAMPLE_SIZE, config.PATIENCE, config.THRESHOLD)
    bch7_4_success, bch7_4_ber = run_simulation(bch7_4.k, bch7_4, config.MAX_BER, config.BER_STEP, config.SAMPLE_SIZE,
                                                config.PATIENCE, config.THRESHOLD)
    baseline_15_success, baseline_15_ber = run_simulation(15, None, config.MAX_BER, config.BER_STEP, config.SAMPLE_SIZE,
                                                          config.PATIENCE, config.THRESHOLD)
    baseline_7_success, baseline_7_ber = run_simulation(7, None, config.MAX_BER, config.BER_STEP, config.SAMPLE_SIZE,
                                                        config.PATIENCE, config.THRESHOLD)

    # Find longest history
    max_length = max(len(bch127_8_success), len(bch31_6_success), len(bch15_5_success),
                     len(bch15_7_success), len(bch15_11_success), len(bch7_4_success),
                     len(baseline_15_success), len(baseline_7_success))

    BER_history = max([bch127_8_ber, bch31_6_ber, bch15_5_ber, bch15_7_ber,
                       bch15_11_ber, bch7_4_ber, baseline_15_ber, baseline_7_ber], key=len)


    # Pad lists to same length
    def pad_list(lst, length):
        return lst + [0] * (length - len(lst))


    bch127_8_success = pad_list(bch127_8_success, max_length)
    bch31_6_success = pad_list(bch31_6_success, max_length)
    bch15_5_success = pad_list(bch15_5_success, max_length)
    bch15_7_success = pad_list(bch15_7_success, max_length)
    bch15_11_success = pad_list(bch15_11_success, max_length)
    bch7_4_success = pad_list(bch7_4_success, max_length)
    baseline_15_success = pad_list(baseline_15_success, max_length)
    baseline_7_success = pad_list(baseline_7_success, max_length)


    # Calculate code rates
    def get_code_rate(bch_code, success_history):
        data_ratio = bch_code.k / bch_code.n
        return [success_rate * data_ratio for success_rate in success_history]


    bch127_8_rate = get_code_rate(bch127_8, bch127_8_success)
    bch31_6_rate = get_code_rate(bch31_6, bch31_6_success)
    bch15_5_rate = get_code_rate(bch15_5, bch15_5_success)
    bch15_7_rate = get_code_rate(bch15_7, bch15_7_success)
    bch15_11_rate = get_code_rate(bch15_11, bch15_11_success)
    bch7_4_rate = get_code_rate(bch7_4, bch7_4_success)

    total_time = time.perf_counter() - simulation_start_time
    print(f"Simulation took {int(total_time // 60)} minutes and {total_time % 60:.2f} seconds")

    # Save success results
    with open('success_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['BER', 'BCH(127,8)', 'BCH(31,6)', 'BCH(15,5)', 'BCH(15,7)', 'BCH(15,11)', 'BCH(7,4)', 'No encoding (k=15)',
             'No encoding (k=7)'])
        for i in range(max_length):
            writer.writerow([BER_history[i], bch127_8_success[i], bch31_6_success[i], bch15_5_success[i],
                             bch15_7_success[i], bch15_11_success[i], bch7_4_success[i],
                             baseline_15_success[i], baseline_7_success[i]])

    # Save rate results
    with open('rate_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['BER', 'BCH(127,8)', 'BCH(31,6)', 'BCH(15,5)', 'BCH(15,7)', 'BCH(15,11)', 'BCH(7,4)', 'No encoding (k=15)',
             'No encoding (k=7)'])
        for i in range(max_length):
            writer.writerow([BER_history[i], bch127_8_rate[i], bch31_6_rate[i], bch15_5_rate[i],
                             bch15_7_rate[i], bch15_11_rate[i], bch7_4_rate[i],
                             baseline_15_success[i], baseline_7_success[i]])

    print("Results saved! Run plot_results.py to generate plots.")
