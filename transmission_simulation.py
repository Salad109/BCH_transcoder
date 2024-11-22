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
    import matplotlib.pyplot as plt
    import numpy as np
    import time


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
                    encoded_data = bch_code.encode_bch(data)  # Encode data
                    error_data = introduce_error(encoded_data, ber)  # Introduce random errors
                    decoded_data = bch_code.decode_bch(error_data)  # Decode received data

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


    # Simulation parameters
    MAX_BER = 1.0  # Maximum bit error rate to test for(assuming it won't be terminated first by early stopping)
    BER_STEP = 0.05  # BER step value
    SAMPLE_SIZE = 250  # How many randomized messages to send per BER value
    PATIENCE = 3  # Stop after this many epochs' success rate is smaller or equal to threshold
    THRESHOLD = 0.005

    # Running simulations
    simulation_start_time = time.perf_counter()

    bch127_8_success_history, bch127_8_BER_history = run_simulation(k=bch127_8.k, bch_code=bch127_8,
                                                                    max_ber=MAX_BER,
                                                                    ber_step=BER_STEP,
                                                                    sample_size=SAMPLE_SIZE,
                                                                    patience_count=PATIENCE,
                                                                    patience_threshold=THRESHOLD)
    bch31_6_success_history, bch31_6_BER_history = run_simulation(k=bch31_6.k, bch_code=bch31_6,
                                                                  max_ber=MAX_BER,
                                                                  ber_step=BER_STEP,
                                                                  sample_size=SAMPLE_SIZE,
                                                                  patience_count=PATIENCE,
                                                                  patience_threshold=THRESHOLD)
    bch15_5_success_history, bch15_5_BER_history = run_simulation(k=bch15_5.k, bch_code=bch15_5,
                                                                  max_ber=MAX_BER,
                                                                  ber_step=BER_STEP,
                                                                  sample_size=SAMPLE_SIZE,
                                                                  patience_count=PATIENCE,
                                                                  patience_threshold=THRESHOLD)
    bch15_7_success_history, bch15_7_BER_history = run_simulation(k=bch15_7.k, bch_code=bch15_7,
                                                                  max_ber=MAX_BER,
                                                                  ber_step=BER_STEP,
                                                                  sample_size=SAMPLE_SIZE,
                                                                  patience_count=PATIENCE,
                                                                  patience_threshold=THRESHOLD)
    bch15_11_success_history, bch15_11_BER_history = run_simulation(k=bch15_11.k, bch_code=bch15_11,
                                                                    max_ber=MAX_BER,
                                                                    ber_step=BER_STEP,
                                                                    sample_size=SAMPLE_SIZE,
                                                                    patience_count=PATIENCE,
                                                                    patience_threshold=THRESHOLD)
    bch7_4_success_history, bch7_4_BER_history = run_simulation(k=bch7_4.k, bch_code=bch7_4,
                                                                max_ber=MAX_BER,
                                                                ber_step=BER_STEP,
                                                                sample_size=SAMPLE_SIZE,
                                                                patience_count=PATIENCE,
                                                                patience_threshold=THRESHOLD)
    baseline_15_success_history, baseline_15_BER_history = run_simulation(k=15,
                                                                        max_ber=MAX_BER,
                                                                        ber_step=BER_STEP,
                                                                        sample_size=SAMPLE_SIZE,
                                                                        patience_count=PATIENCE,
                                                                        patience_threshold=THRESHOLD)
    baseline_7_success_history, baseline_7_BER_history = run_simulation(k=7,
                                                                        max_ber=MAX_BER,
                                                                        ber_step=BER_STEP,
                                                                        sample_size=SAMPLE_SIZE,
                                                                        patience_count=PATIENCE,
                                                                        patience_threshold=THRESHOLD)


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

    # Plotting Success Rate vs BER
    plt.figure(figsize=(10, 6))
    plt.plot(bch127_8_BER_history, bch127_8_success_history, color='purple', linestyle='-', linewidth=2,
             label='BCH(127,8), t=31')
    plt.plot(bch31_6_BER_history, bch31_6_success_history, color='red', linestyle='-', linewidth=2,
             label='BCH(31,6), t=7')
    plt.plot(bch15_5_BER_history, bch15_5_success_history, color='green', linestyle='-', linewidth=2,
             label='BCH(15,5), t=3')
    plt.plot(bch15_7_BER_history, bch15_7_success_history, color='green', linestyle='--', linewidth=2,
             label='BCH(15,7), t=2')
    plt.plot(bch15_11_BER_history, bch15_11_success_history, color='green', linestyle=':', linewidth=2,
             label='BCH(15,11), t=1')
    plt.plot(bch7_4_BER_history, bch7_4_success_history, color='blue', linestyle='-', linewidth=2,
             label='BCH(7,4), t=1')
    plt.plot(baseline_15_BER_history, baseline_15_success_history, color='black', linestyle='--', linewidth=2,
             label='No encoding(k=15), t=0')
    plt.plot(baseline_7_BER_history, baseline_7_success_history, color='black', linestyle=':', linewidth=2,
             label='No encoding(k=7), t=0')

    plt.title("Success Rate vs. BER for various BCH Codes", fontsize=20, fontweight='bold')
    plt.xlabel("Bit Error Rate (BER)", fontsize=12)
    plt.ylabel("Success Rate", fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(loc="upper right", prop={'size': 15})
    plt.tight_layout()

    text = f"BER step: {BER_STEP}\nMessages per step per code: {SAMPLE_SIZE}"
    plt.annotate(text, (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')

    plt.savefig('success_plot_all.svg', format='svg')
    plt.show()

    # Plotting code rate
    plt.figure(figsize=(10, 6))
    plt.plot(bch127_8_BER_history, bch127_8_rate, color='purple', linestyle='-', linewidth=2,
             label='BCH(127,8), t=31')
    plt.plot(bch31_6_BER_history, bch31_6_rate, color='red', linestyle='-', linewidth=2,
             label='BCH(31,6), t=7')
    plt.plot(bch15_5_BER_history, bch15_5_rate, color='green', linestyle='-', linewidth=2,
             label='BCH(15,5), t=3')
    plt.plot(bch15_7_BER_history, bch15_7_rate, color='green', linestyle='--', linewidth=2,
             label='BCH(15,7), t=2')
    plt.plot(bch15_11_BER_history, bch15_11_rate, color='green', linestyle=':', linewidth=2,
             label='BCH(15,11), t=1')
    plt.plot(bch7_4_BER_history, bch_7_4_rate, color='blue', linestyle='-', linewidth=2,
             label='BCH(7,4), t=1')
    plt.plot(baseline_15_BER_history, baseline_15_rate, color='black', linestyle='--', linewidth=2,
             label='No encoding(k=15), t=0')
    plt.plot(baseline_7_BER_history, baseline_7_rate, color='black', linestyle=':', linewidth=2,
             label='No encoding(k=7), t=0')

    plt.title("Effective code rate vs. BER for various BCH Codes", fontsize=20, fontweight='bold')
    plt.xlabel("Bit Error Rate (BER)", fontsize=12)
    plt.ylabel("Effective code rate", fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(loc="upper right", prop={'size': 15})
    plt.tight_layout()

    text = f"BER step: {BER_STEP}\nMessages per step per code: {SAMPLE_SIZE}"
    plt.annotate(text, (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')

    plt.savefig('rate_plot_all.svg', format='svg')
    plt.show()

    # Plotting BCH(15,x) success rates standalone
    plt.figure(figsize=(10, 6))
    plt.plot(bch15_5_BER_history, bch15_5_success_history, color='green', linestyle='-', linewidth=2,
             label='BCH(15,5), t=3')
    plt.plot(bch15_7_BER_history, bch15_7_success_history, color='green', linestyle='--', linewidth=2,
             label='BCH(15,7), t=2')
    plt.plot(bch15_11_BER_history, bch15_11_success_history, color='green', linestyle=':', linewidth=2,
             label='BCH(15,11), t=1')
    plt.plot(baseline_15_BER_history, baseline_15_success_history, color='black', linestyle='--', linewidth=2,
             label='No encoding(k=15), t=0')

    plt.title("Success Rate vs. BER for BCH(15,x) codes", fontsize=20, fontweight='bold')
    plt.xlabel("Bit Error Rate (BER)", fontsize=12)
    plt.ylabel("Success Rate", fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(loc="upper right", prop={'size': 15})
    plt.tight_layout()

    text = f"BER step: {BER_STEP}\nMessages per step per code: {SAMPLE_SIZE}"
    plt.annotate(text, (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')

    plt.savefig('success_plot_bch15.svg', format='svg')
    plt.show()

    # Plotting BCH(15,x) code rate standalone
    plt.figure(figsize=(10, 6))
    plt.plot(bch15_5_BER_history, bch15_5_rate, color='green', linestyle='-', linewidth=2,
             label='BCH(15,5), t=3')
    plt.plot(bch15_7_BER_history, bch15_7_rate, color='green', linestyle='--', linewidth=2,
             label='BCH(15,7), t=2')
    plt.plot(bch15_11_BER_history, bch15_11_rate, color='green', linestyle=':', linewidth=2,
             label='BCH(15,11), t=1')
    plt.plot(baseline_15_BER_history, baseline_15_rate, color='black', linestyle='--', linewidth=2,
             label='No encoding(k=15), t=0')

    plt.title("Effective code rate vs. BER for BCH(15,x) codes", fontsize=20, fontweight='bold')
    plt.xlabel("Bit Error Rate (BER)", fontsize=12)
    plt.ylabel("Effective code rate", fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(loc="upper right", prop={'size': 15})
    plt.tight_layout()

    text = f"BER step: {BER_STEP}\nMessages per step per code: {SAMPLE_SIZE}"
    plt.annotate(text, (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')

    plt.savefig('rate_plot_bch15.svg', format='svg')
    plt.show()
