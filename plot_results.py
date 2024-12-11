import csv
import matplotlib.pyplot as plt


def read_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row
        data = list(reader)
    return headers, data


# Read success rate data
success_headers, success_data = read_csv('success_results.csv')
BER_history = [float(row[0]) for row in success_data]
bch127_8_success_history = [float(row[1]) for row in success_data]
bch31_6_success_history = [float(row[2]) for row in success_data]
bch15_5_success_history = [float(row[3]) for row in success_data]
bch15_7_success_history = [float(row[4]) for row in success_data]
bch15_11_success_history = [float(row[5]) for row in success_data]
bch7_4_success_history = [float(row[6]) for row in success_data]
baseline_15_success_history = [float(row[7]) for row in success_data]
baseline_7_success_history = [float(row[8]) for row in success_data]

# Read effective code rate data
rate_headers, rate_data = read_csv('rate_results.csv')
bch127_8_rate = [float(row[1]) for row in rate_data]
bch31_6_rate = [float(row[2]) for row in rate_data]
bch15_5_rate = [float(row[3]) for row in rate_data]
bch15_7_rate = [float(row[4]) for row in rate_data]
bch15_11_rate = [float(row[5]) for row in rate_data]
bch_7_4_rate = [float(row[6]) for row in rate_data]
baseline_15_rate = [float(row[7]) for row in rate_data]
baseline_7_rate = [float(row[8]) for row in rate_data]

# Plotting Success Rate vs BER
plt.figure(figsize=(10, 6))
plt.plot(BER_history, bch127_8_success_history, color='purple', linestyle='-', linewidth=2,
         label='BCH(127,8), t=31')
plt.plot(BER_history, bch31_6_success_history, color='red', linestyle='-', linewidth=2,
         label='BCH(31,6), t=7')
plt.plot(BER_history, bch15_5_success_history, color='green', linestyle='-', linewidth=2,
         label='BCH(15,5), t=3')
plt.plot(BER_history, bch15_7_success_history, color='green', linestyle='--', linewidth=2,
         label='BCH(15,7), t=2')
plt.plot(BER_history, bch15_11_success_history, color='green', linestyle=':', linewidth=2,
         label='BCH(15,11), t=1')
plt.plot(BER_history, bch7_4_success_history, color='blue', linestyle='-', linewidth=2,
         label='BCH(7,4), t=1')
plt.plot(BER_history, baseline_15_success_history, color='black', linestyle='--', linewidth=2,
         label='No encoding(k=15), t=0')
plt.plot(BER_history, baseline_7_success_history, color='black', linestyle=':', linewidth=2,
         label='No encoding(k=7), t=0')

plt.title("Success Rate vs. BER for various BCH Codes", fontsize=20, fontweight='bold')
plt.xlabel("Bit Error Rate (BER)", fontsize=12)
plt.ylabel("Success Rate", fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(loc="upper right", prop={'size': 15})
plt.tight_layout()

plt.savefig('success_plot_all.svg', format='svg')
plt.show()

# Plotting code rate
plt.figure(figsize=(10, 6))
plt.plot(BER_history, bch127_8_rate, color='purple', linestyle='-', linewidth=2,
         label='BCH(127,8), t=31')
plt.plot(BER_history, bch31_6_rate, color='red', linestyle='-', linewidth=2,
         label='BCH(31,6), t=7')
plt.plot(BER_history, bch15_5_rate, color='green', linestyle='-', linewidth=2,
         label='BCH(15,5), t=3')
plt.plot(BER_history, bch15_7_rate, color='green', linestyle='--', linewidth=2,
         label='BCH(15,7), t=2')
plt.plot(BER_history, bch15_11_rate, color='green', linestyle=':', linewidth=2,
         label='BCH(15,11), t=1')
plt.plot(BER_history, bch_7_4_rate, color='blue', linestyle='-', linewidth=2,
         label='BCH(7,4), t=1')
plt.plot(BER_history, baseline_15_rate, color='black', linestyle='--', linewidth=2,
         label='No encoding(k=15), t=0')
plt.plot(BER_history, baseline_7_rate, color='black', linestyle=':', linewidth=2,
         label='No encoding(k=7), t=0')

plt.title("Effective code rate vs. BER for various BCH Codes", fontsize=20, fontweight='bold')
plt.xlabel("Bit Error Rate (BER)", fontsize=12)
plt.ylabel("Effective code rate", fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(loc="upper right", prop={'size': 15})
plt.tight_layout()

plt.savefig('rate_plot_all.svg', format='svg')
plt.show()

# Plotting BCH(15,x) success rates standalone
plt.figure(figsize=(10, 6))
plt.plot(BER_history, bch15_5_success_history, color='green', linestyle='-', linewidth=2,
         label='BCH(15,5), t=3')
plt.plot(BER_history, bch15_7_success_history, color='green', linestyle='--', linewidth=2,
         label='BCH(15,7), t=2')
plt.plot(BER_history, bch15_11_success_history, color='green', linestyle=':', linewidth=2,
         label='BCH(15,11), t=1')
plt.plot(BER_history, baseline_15_success_history, color='black', linestyle='--', linewidth=2,
         label='No encoding(k=15), t=0')

plt.title("Success Rate vs. BER for BCH(15,x) codes", fontsize=20, fontweight='bold')
plt.xlabel("Bit Error Rate (BER)", fontsize=12)
plt.ylabel("Success Rate", fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(loc="upper right", prop={'size': 15})
plt.tight_layout()

plt.savefig('success_plot_bch15.svg', format='svg')
plt.show()

# Plotting BCH(15,x) code rate standalone
plt.figure(figsize=(10, 6))
plt.plot(BER_history, bch15_5_rate, color='green', linestyle='-', linewidth=2,
         label='BCH(15,5), t=3')
plt.plot(BER_history, bch15_7_rate, color='green', linestyle='--', linewidth=2,
         label='BCH(15,7), t=2')
plt.plot(BER_history, bch15_11_rate, color='green', linestyle=':', linewidth=2,
         label='BCH(15,11), t=1')
plt.plot(BER_history, baseline_15_rate, color='black', linestyle='--', linewidth=2,
         label='No encoding(k=15), t=0')

plt.title("Effective code rate vs. BER for BCH(15,x) codes", fontsize=20, fontweight='bold')
plt.xlabel("Bit Error Rate (BER)", fontsize=12)
plt.ylabel("Effective code rate", fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(loc="upper right", prop={'size': 15})
plt.tight_layout()

plt.savefig('rate_plot_bch15.svg', format='svg')
plt.show()
