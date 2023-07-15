import matplotlib.pyplot as plt

# Gas usage data for transactions
gas_usage = [138186, 0, 21000]  # Update with the actual gas usage data from the samples

# Define the gas usage ranges for the histogram bins
bin_ranges = [0, 50000, 100000, 150000, 200000, 250000]  # Adjust the bin ranges as needed

# Plotting the histogram
plt.figure(figsize=(8, 6))
plt.hist(gas_usage, bins=bin_ranges, edgecolor='black', alpha=0.7)

# Set labels and title
plt.xlabel('Gas Usage')
plt.ylabel('Number of Transactions')
plt.title('Gas Usage Distribution')

# Show the percentage of transactions in each bin
total_transactions = len(gas_usage)
bin_counts, _, _ = plt.hist(gas_usage, bins=bin_ranges, edgecolor='black', alpha=0.7)
for i, count in enumerate(bin_counts):
    percentage = (count / total_transactions) * 100
    plt.text(bin_ranges[i], count, f'{percentage:.1f}%', ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.savefig("gas_usage_dist.png")
