import csv
import matplotlib.pyplot as plt


def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = list(reader)
    return headers, data


# Read data
success_headers, success_data = read_csv('success_results.csv')
rate_headers, rate_data = read_csv('rate_results.csv')

# Parse success data
BER_history = [float(row[0]) for row in success_data]
bch127_8_success = [float(row[1]) for row in success_data]
bch31_6_success = [float(row[2]) for row in success_data]
bch15_5_success = [float(row[3]) for row in success_data]
bch15_7_success = [float(row[4]) for row in success_data]
bch15_11_success = [float(row[5]) for row in success_data]
bch7_4_success = [float(row[6]) for row in success_data]
baseline_15_success = [float(row[7]) for row in success_data]
baseline_7_success = [float(row[8]) for row in success_data]

# Parse rate data
bch127_8_rate = [float(row[1]) for row in rate_data]
bch31_6_rate = [float(row[2]) for row in rate_data]
bch15_5_rate = [float(row[3]) for row in rate_data]
bch15_7_rate = [float(row[4]) for row in rate_data]
bch15_11_rate = [float(row[5]) for row in rate_data]
bch7_4_rate = [float(row[6]) for row in rate_data]
baseline_15_rate = [float(row[7]) for row in rate_data]
baseline_7_rate = [float(row[8]) for row in rate_data]

# Plot 1: Success Rate vs BER (All codes)
plt.figure(figsize=(10, 6))
plt.plot(BER_history, bch127_8_success, 'purple', linewidth=2, label='BCH(127,8), t=31')
plt.plot(BER_history, bch31_6_success, 'red', linewidth=2, label='BCH(31,6), t=7')
plt.plot(BER_history, bch15_5_success, 'green', linewidth=2, label='BCH(15,5), t=3')
plt.plot(BER_history, bch15_7_success, 'green', linestyle='--', linewidth=2, label='BCH(15,7), t=2')
plt.plot(BER_history, bch15_11_success, 'green', linestyle=':', linewidth=2, label='BCH(15,11), t=1')
plt.plot(BER_history, bch7_4_success, 'blue', linewidth=2, label='BCH(7,4), t=1')
plt.plot(BER_history, baseline_15_success, 'black', linestyle='--', linewidth=2, label='No encoding(k=15)')
plt.plot(BER_history, baseline_7_success, 'black', linestyle=':', linewidth=2, label='No encoding(k=7)')

plt.title("Success Rate vs. BER for various BCH Codes", fontsize=20, fontweight='bold')
plt.xlabel("Bit Error Rate (BER)", fontsize=12)
plt.ylabel("Success Rate", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc="upper right", fontsize=10)
plt.tight_layout()
plt.savefig('success_plot_all.svg', format='svg')
print("Saved: success_plot_all.svg")
plt.show()

# Plot 2: Code Rate vs BER (All codes)
plt.figure(figsize=(10, 6))
plt.plot(BER_history, bch127_8_rate, 'purple', linewidth=2, label='BCH(127,8), t=31')
plt.plot(BER_history, bch31_6_rate, 'red', linewidth=2, label='BCH(31,6), t=7')
plt.plot(BER_history, bch15_5_rate, 'green', linewidth=2, label='BCH(15,5), t=3')
plt.plot(BER_history, bch15_7_rate, 'green', linestyle='--', linewidth=2, label='BCH(15,7), t=2')
plt.plot(BER_history, bch15_11_rate, 'green', linestyle=':', linewidth=2, label='BCH(15,11), t=1')
plt.plot(BER_history, bch7_4_rate, 'blue', linewidth=2, label='BCH(7,4), t=1')
plt.plot(BER_history, baseline_15_rate, 'black', linestyle='--', linewidth=2, label='No encoding(k=15)')
plt.plot(BER_history, baseline_7_rate, 'black', linestyle=':', linewidth=2, label='No encoding(k=7)')

plt.title("Effective Code Rate vs. BER for various BCH Codes", fontsize=20, fontweight='bold')
plt.xlabel("Bit Error Rate (BER)", fontsize=12)
plt.ylabel("Effective Code Rate", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc="upper right", fontsize=10)
plt.tight_layout()
plt.savefig('rate_plot_all.svg', format='svg')
print("Saved: rate_plot_all.svg")
plt.show()

# Plot 3: BCH(15,x) Success Rates
plt.figure(figsize=(10, 6))
plt.plot(BER_history, bch15_5_success, 'green', linewidth=2, label='BCH(15,5), t=3')
plt.plot(BER_history, bch15_7_success, 'green', linestyle='--', linewidth=2, label='BCH(15,7), t=2')
plt.plot(BER_history, bch15_11_success, 'green', linestyle=':', linewidth=2, label='BCH(15,11), t=1')
plt.plot(BER_history, baseline_15_success, 'black', linestyle='--', linewidth=2, label='No encoding(k=15)')

plt.title("Success Rate vs. BER for BCH(15,x) codes", fontsize=20, fontweight='bold')
plt.xlabel("Bit Error Rate (BER)", fontsize=12)
plt.ylabel("Success Rate", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc="upper right", fontsize=12)
plt.tight_layout()
plt.savefig('success_plot_bch15.svg', format='svg')
print("Saved: success_plot_bch15.svg")
plt.show()

# Plot 4: BCH(15,x) Code Rates
plt.figure(figsize=(10, 6))
plt.plot(BER_history, bch15_5_rate, 'green', linewidth=2, label='BCH(15,5), t=3')
plt.plot(BER_history, bch15_7_rate, 'green', linestyle='--', linewidth=2, label='BCH(15,7), t=2')
plt.plot(BER_history, bch15_11_rate, 'green', linestyle=':', linewidth=2, label='BCH(15,11), t=1')
plt.plot(BER_history, baseline_15_rate, 'black', linestyle='--', linewidth=2, label='No encoding(k=15)')

plt.title("Effective Code Rate vs. BER for BCH(15,x) codes", fontsize=20, fontweight='bold')
plt.xlabel("Bit Error Rate (BER)", fontsize=12)
plt.ylabel("Effective Code Rate", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc="upper right", fontsize=12)
plt.tight_layout()
plt.savefig('rate_plot_bch15.svg', format='svg')
print("Saved: rate_plot_bch15.svg")
plt.show()

print("All plots generated successfully!")
