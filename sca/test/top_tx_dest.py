import matplotlib.pyplot as plt

# Transaction data with recipient addresses
transactions = [
    {"to": "0x95ba4cf87d6723ad9c0db21737d862be80e93911"},
    {"to": "0x1234567890abcdef"},
    {"to": "0x95ba4cf87d6723ad9c0db21737d862be80e93911"},
    {"to": "0xabcdef1234567890"},
    {"to": "0x95ba4cf87d6723ad9c0db21737d862be80e93911"},
]  # Update with the actual transaction data and recipient addresses

# Count the frequency of recipient addresses
recipient_counts = {}
for transaction in transactions:
    recipient = transaction["to"]
    if recipient in recipient_counts:
        recipient_counts[recipient] += 1
    else:
        recipient_counts[recipient] = 1

# Sort the recipient addresses by frequency
top_recipients = sorted(recipient_counts.items(), key=lambda x: x[1], reverse=True)[:5]  # Change 5 to the desired number of top recipients

# Extract the addresses and frequencies
addresses = [recipient[0] for recipient in top_recipients]
frequencies = [recipient[1] for recipient in top_recipients]

# Plotting the bar chart
plt.figure(figsize=(10, 6))
plt.bar(addresses, frequencies)

# Set labels and title
plt.xlabel('Recipient Address')
plt.ylabel('Frequency')
plt.title('Top Transaction Recipients')

# Rotate x-axis tick labels for better readability if needed
plt.xticks(rotation='vertical')

# Show the plot
plt.tight_layout()
plt.savefig('top_tx_dest.png', dpi=300)
