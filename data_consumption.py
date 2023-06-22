import psutil
from pprint import pprint as pp
import time
import matplotlib.pyplot as plt

# Specify the process name to monitor
process_name = "firefox"

# Specify the duration in seconds
duration = 1800  # 0.5 hour

# Get the process ID for the specified process name
process_id = None
for proc in psutil.process_iter(['name', 'pid']):
    if proc.info['name'] == process_name:
        process_id = proc.info['pid']
        break

total_data_mb = 0
time_list = []
data_list = []

if process_id is None:
    print(f"No process found with the name '{process_name}'")
else:
    # Get the initial network stats for the specified process
    process = psutil.Process(process_id)
    print(process)
    # Get the initial network stats
    network_stats = psutil.net_io_counters()

    # Start time for tracking duration
    start_time = time.time()

    # Continuously track data consumption until the duration is reached
    while time.time() - start_time <= duration:
        # Get the updated network stats
        updated_stats = psutil.net_io_counters()
        print(updated_stats)

        # Calculate the data consumption for the specified process
        data_sent = updated_stats.bytes_sent - network_stats.bytes_sent
        data_received = updated_stats.bytes_recv - network_stats.bytes_recv
        total_data = data_sent + data_received
        
        # Convert the data to a human-readable format
        total_data_mb += total_data / (1024 * 1024)

        # Print the data consumption for the specified process
        print(f"Process: {process_name} process id {process_id}")
        print(f"Data Sent: {data_sent / (1024*1024):.2f} MB")
        print(f"Data Received: {data_received / (1024*1024):.2f} MB")
        print(f"Total Data consumption: {total_data_mb:.2f} MB")
        print("")

        # Update the network stats for the next iteration
        network_stats = updated_stats
        
        # Append the data to the lists for plotting
        time_list.append(time.time() - start_time)
        data_list.append(total_data_mb)

        # Plot the data consumption in real-time
        plt.plot(time_list, data_list)
        plt.xlabel('Time (s)')
        plt.ylabel('Total Data Consumption (MB)')
        plt.title('Live Data Consumption')
        plt.grid(True)
        plt.pause(0.1)

        # Sleep for a short interval (e.g., 3 seconds) before checking again
        time.sleep(3)

# Display the final plot
plt.show()