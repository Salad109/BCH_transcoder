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


def introduce_error(input_data, ber=0.1):
    errors = input_data.copy()
    for i in range(len(errors)):
        if random.random() <= ber:  # Flip the bit with probability = BER
            errors[i] ^= 1
    return errors


if __name__ == "__main__":
    import bch127_8
    import bch31_6
    import bch15_5
    import bch15_7
    import bch15_11
    import bch7_4
    import numpy as np
    import time
    import csv

    # Simulation parameters
    MAX_BER = 1.0  # Maximum bit error rate to test for(assuming it won't be terminated first by early stopping)
    BER_STEP = 0.075  # BER step value
    SAMPLE_SIZE = 150  # How many randomized messages to send per BER value
    PATIENCE = 3  # Stop after this many epochs' success rate is smaller or equal to threshold
    THRESHOLD = 0.075 # Stop if success rate is smaller or equal to this value

    if MAX_BER <= 0 or BER_STEP <= 0 or SAMPLE_SIZE <= 0 or PATIENCE <= 0 or THRESHOLD < 0:
        raise ValueError("Simulation parameters must be positive.")


    def run_simulation(k, bch_code=None, max_ber=1.0, ber_step=0.05, sample_size=100, patience_count=5,
                       patience_threshold=0.0):
        """
        Simulates performance for BCH codes or a baseline scenario.

        Args:
            k (int): Length of the input data (message size).
            bch_code (object or None): BCH code object with encode_bch and decode_bch methods. If None, runs baseline.
            max_ber (float): Maximum Bit Error Rate to test.
            ber_step (float): Incremental step for BER.
            sample_size (int): Number of samples per BER to test.
            patience_count (int): Number of consecutive BERs with low success rates to trigger early stopping.
            patience_threshold (float): Minimum success rate to prevent early stopping.

        Returns:
            success_history (list of float): Success rates for each BER step.
            ber_history (list of float): Tested BER values.
        """
        if sample_size <= 0:
            raise ValueError("sample_size must be positive.")
        if ber_step <= 0 or max_ber <= 0:
            raise ValueError("ber_step and max_ber must be positive.")

        success_history = []
        ber_history = []
        current_step = 0
        ber = 0.0

        while round(ber, 10) <= max_ber:
            start_time = time.perf_counter()
            success_count = 0

            for _ in range(sample_size):
                # Generate random data
                data = np.random.randint(2, size=k)

                if bch_code is not None:
                    # BCH code scenario
                    encoded_data = bch_code.encode(data)  # Encode data
                    error_data = introduce_error(encoded_data, ber)  # Introduce random errors
                    decoded_data = bch_code.decode(error_data)  # Decode received data

                    # Validate decoding
                    if decoded_data[0] is not None and np.array_equal(decoded_data[0][:len(data)], data):
                        success_count += 1
                else:
                    # Baseline scenario
                    error_data = introduce_error(data, ber)  # Introduce random errors

                    # Validate: success if no bit-flip occurred
                    if np.array_equal(error_data, data):
                        success_count += 1

            # Calculate success rate
            success_rate = success_count / sample_size
            success_history.append(success_rate)
            ber_history.append(ber)
            current_step += 1
            epoch_time = time.perf_counter() - start_time

            # Print progress
            if bch_code is not None:
                print(
                    f"Code: BCH({bch_code.n},{bch_code.k}) | BER: {ber:.3f} | Step: {current_step:4d} "
                    f"| Success Rate: {success_rate:.4f} | Time: {epoch_time:.3f}s"
                )
            else:
                print(
                    f"Code: No encoding (k={k}) | BER: {ber:.3f} | Step: {current_step:4d} "
                    f"| Success Rate: {success_rate:.4f} | Time: {epoch_time:.3f}s"
                )

            # Early stopping condition
            if len(success_history) >= patience_count and all(
                    rate <= patience_threshold for rate in success_history[-patience_count:]):
                print("Early stopping triggered!")
                break

            ber += ber_step

        return success_history, ber_history


    # Running simulations
    bch127_8 = bch127_8.BCH127_8()
    bch31_6 = bch31_6.BCH31_6()
    bch15_5 = bch15_5.BCH15_5()
    bch15_7 = bch15_7.BCH15_7()
    bch15_11 = bch15_11.BCH15_11()
    bch7_4 = bch7_4.BCH7_4()

    print("Commencing simulation with the following parameters:")
    print(f"Max BER: {MAX_BER}")
    print(f"BER step: {BER_STEP}")
    print(f"Sample size: {SAMPLE_SIZE}")
    print(f"Patience: {PATIENCE}")
    print(f"Patience threshold: {THRESHOLD}")
    print("The simulation may take several minutes to complete. Please be patient.")

    simulation_start_time = time.perf_counter()

    bch127_8_success_history, bch127_8_ber_history = run_simulation(k=bch127_8.k, bch_code=bch127_8,
                                                                    max_ber=MAX_BER,
                                                                    ber_step=BER_STEP,
                                                                    sample_size=SAMPLE_SIZE,
                                                                    patience_count=PATIENCE,
                                                                    patience_threshold=THRESHOLD)
    bch31_6_success_history, bch31_6_ber_history = run_simulation(k=bch31_6.k, bch_code=bch31_6,
                                                                  max_ber=MAX_BER,
                                                                  ber_step=BER_STEP,
                                                                  sample_size=SAMPLE_SIZE,
                                                                  patience_count=PATIENCE,
                                                                  patience_threshold=THRESHOLD)
    bch15_5_success_history, bch15_5_ber_history = run_simulation(k=bch15_5.k, bch_code=bch15_5,
                                                                  max_ber=MAX_BER,
                                                                  ber_step=BER_STEP,
                                                                  sample_size=SAMPLE_SIZE,
                                                                  patience_count=PATIENCE,
                                                                  patience_threshold=THRESHOLD)
    bch15_7_success_history, bch15_7_ber_history = run_simulation(k=bch15_7.k, bch_code=bch15_7,
                                                                  max_ber=MAX_BER,
                                                                  ber_step=BER_STEP,
                                                                  sample_size=SAMPLE_SIZE,
                                                                  patience_count=PATIENCE,
                                                                  patience_threshold=THRESHOLD)
    bch15_11_success_history, bch15_11_ber_history = run_simulation(k=bch15_11.k, bch_code=bch15_11,
                                                                    max_ber=MAX_BER,
                                                                    ber_step=BER_STEP,
                                                                    sample_size=SAMPLE_SIZE,
                                                                    patience_count=PATIENCE,
                                                                    patience_threshold=THRESHOLD)
    bch7_4_success_history, bch7_4_ber_history = run_simulation(k=bch7_4.k, bch_code=bch7_4,
                                                                max_ber=MAX_BER,
                                                                ber_step=BER_STEP,
                                                                sample_size=SAMPLE_SIZE,
                                                                patience_count=PATIENCE,
                                                                patience_threshold=THRESHOLD)
    baseline_15_success_history, baseline_15_ber_history = run_simulation(k=15,
                                                                          max_ber=MAX_BER,
                                                                          ber_step=BER_STEP,
                                                                          sample_size=SAMPLE_SIZE,
                                                                          patience_count=PATIENCE,
                                                                          patience_threshold=THRESHOLD)
    baseline_7_success_history, baseline_7_ber_history = run_simulation(k=7,
                                                                        max_ber=MAX_BER,
                                                                        ber_step=BER_STEP,
                                                                        sample_size=SAMPLE_SIZE,
                                                                        patience_count=PATIENCE,
                                                                        patience_threshold=THRESHOLD)

    # Determine the maximum length of the success rate lists
    max_length = max(len(bch127_8_success_history), len(bch31_6_success_history), len(bch15_5_success_history),
                     len(bch15_7_success_history), len(bch15_11_success_history), len(bch7_4_success_history),
                     len(baseline_15_success_history), len(baseline_7_success_history))

    BER_history = max([bch127_8_ber_history, bch31_6_ber_history, bch15_5_ber_history, bch15_7_ber_history,
                       bch15_11_ber_history, bch7_4_ber_history, baseline_15_ber_history, baseline_7_ber_history],
                      key=len)


    # Pad shorter lists with zeros
    def pad_list(lst, length):
        return lst + [0] * (length - len(lst))


    bch127_8_success_history = pad_list(bch127_8_success_history, max_length)
    bch31_6_success_history = pad_list(bch31_6_success_history, max_length)
    bch15_5_success_history = pad_list(bch15_5_success_history, max_length)
    bch15_7_success_history = pad_list(bch15_7_success_history, max_length)
    bch15_11_success_history = pad_list(bch15_11_success_history, max_length)
    bch7_4_success_history = pad_list(bch7_4_success_history, max_length)
    baseline_15_success_history = pad_list(baseline_15_success_history, max_length)
    baseline_7_success_history = pad_list(baseline_7_success_history, max_length)


    # Code rate calculations
    def get_code_rate(bch_code, success_history):
        data_ratio = bch_code.k / bch_code.n
        speed_history = []
        for success_rate in success_history:
            speed_history.append(success_rate * data_ratio)
        return speed_history


    bch127_8_rate = get_code_rate(bch127_8, bch127_8_success_history)
    bch31_6_rate = get_code_rate(bch31_6, bch31_6_success_history)
    bch15_5_rate = get_code_rate(bch15_5, bch15_5_success_history)
    bch15_7_rate = get_code_rate(bch15_7, bch15_7_success_history)
    bch15_11_rate = get_code_rate(bch15_11, bch15_11_success_history)
    bch_7_4_rate = get_code_rate(bch7_4, bch7_4_success_history)
    baseline_15_rate = baseline_15_success_history
    baseline_7_rate = baseline_7_success_history

    total_time = time.perf_counter() - simulation_start_time
    print(f"Simulation took {int(total_time // 60)} minutes and {total_time % 60:.2f} seconds")

    # Write the success rate data to a CSV file
    with open('success_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['BER', 'BCH(127,8)', 'BCH(31,6)', 'BCH(15,5)', 'BCH(15,7)', 'BCH(15,11)', 'BCH(7,4)', 'No encoding (k=15)',
             'No encoding (k=7)'])
        for i in range(max_length):
            writer.writerow(
                [BER_history[i], bch127_8_success_history[i], bch31_6_success_history[i], bch15_5_success_history[i],
                 bch15_7_success_history[i], bch15_11_success_history[i], bch7_4_success_history[i],
                 baseline_15_success_history[i], baseline_7_success_history[i]])

    # Write the effective code rate data to a CSV file
    with open('rate_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['BER', 'BCH(127,8)', 'BCH(31,6)', 'BCH(15,5)', 'BCH(15,7)', 'BCH(15,11)', 'BCH(7,4)', 'No encoding (k=15)',
             'No encoding (k=7)'])
        for i in range(max_length):
            writer.writerow(
                [BER_history[i], bch127_8_rate[i], bch31_6_rate[i], bch15_5_rate[i],
                 bch15_7_rate[i], bch15_11_rate[i], bch_7_4_rate[i],
                 baseline_15_rate[i], baseline_7_rate[i]])

    print("Results saved to CSV files. Run plot_results.py to generate plots.")
