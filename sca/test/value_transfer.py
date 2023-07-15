import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime

# Value transferred data for transactions
value_transferred = [29655916115773925070530298846711, 574275922094568, 0]  # Update with the actual value transferred data from the samples

# Timestamps for the transactions
timestamps = [1678576055, 1654581151, 1678575455]  # Update with the actual timestamps from the samples

# Convert timestamps to datetime objects
dates = [datetime.fromtimestamp(timestamp) for timestamp in timestamps]

# Plotting the value transferred over time
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(dates, value_transferred, marker='o')

# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Value Transferred')
ax.set_title('Value Transferred over Time')

# Format x-axis tick labels as dates
date_format = DateFormatter('%Y-%m-%d')  # Choose the desired date format
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

# Show the plot
plt.tight_layout()
plt.savefig('value_transfer.png')
