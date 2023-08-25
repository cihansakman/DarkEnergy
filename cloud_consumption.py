#First of all, create your virtual environment
#python -m venv cloud_consumption_venv
#source cloud_consumption_venv/bin/activate
#pip install google-cloud-monitoring
#bash > export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
from google.cloud import monitoring_v3
import time 
from datetime import datetime
import json
import csv

# Load credentials from the JSON file
with open('cloud_credentials.json') as json_file:
    credentials = json.load(json_file)


# Replace 'your-project-id' with your actual project ID
project_id = credentials['project_id']
client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

#VM instance id
instance_id = credentials['instance_id']


# Create TimeInterval and set start and end times
interval = monitoring_v3.TimeInterval()


from datetime import datetime, timedelta
# Calculate the start and end times for the last n minutes
end_time = datetime.now()
start_time = end_time - timedelta(minutes=30)

# Print the starting time
print("Starting time:", start_time.strftime('%B %d, %Y %H:%M:%S'))


# Convert start and end times to seconds and nanos
start_seconds = int(start_time.timestamp())
end_seconds = int(end_time.timestamp())
start_nanos = int((start_time - datetime.fromtimestamp(start_seconds)).total_seconds() * 10**9)
end_nanos = int((end_time - datetime.fromtimestamp(end_seconds)).total_seconds() * 10**9)

# Create the TimeInterval
interval = monitoring_v3.TimeInterval(
    {
        "start_time": {"seconds": start_seconds, "nanos": start_nanos},
        "end_time": {"seconds": end_seconds, "nanos": end_nanos},
    }
)

# Create the filter strings for CPU utilization, received bytes, and sent bytes metrics
cpu_utilization_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{instance_id}" AND metric.type="compute.googleapis.com/instance/cpu/utilization"'
received_bytes_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{instance_id}" AND metric.type="compute.googleapis.com/instance/network/received_bytes_count"'
sent_bytes_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{instance_id}" AND metric.type="compute.googleapis.com/instance/network/sent_bytes_count"'
memory_utilization_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{instance_id}" AND metric.type="agent.googleapis.com/memory/percent_used" AND metric.labels.state="used"'


# List of filter strings
filter_strs = [cpu_utilization_filter, received_bytes_filter, sent_bytes_filter, memory_utilization_filter]

# Define human-readable metric names for dictionary keys
metric_names = {
    cpu_utilization_filter: 'CPU usage(%)',
    received_bytes_filter: 'Received Bytes',
    sent_bytes_filter: 'Sent Bytes',
    memory_utilization_filter: 'Memory Utilization(%)'
}

# Create a dictionary to store metric values for each timestamp
metric_data = {name: {} for name in metric_names.values()}

# Retrieve responses for different metrics and store data
for filter_str in filter_strs:
    response = client.list_time_series(
        name=f"projects/{project_id}",
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    )
    
    metric_name = metric_names[filter_str]  # Use the human-readable name
    
    for series in response:
        for point in series.points:
            timestamp = point.interval.start_time.timestamp()
            rounded_timestamp = datetime.fromtimestamp(timestamp).replace(second=0)
            readable_timestamp = rounded_timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            if metric_name == 'CPU usage(%)':
                metric_value = point.value.double_value * 100.0
            elif metric_name == 'Memory Utilization(%)':
                metric_value = point.value.double_value 
            else:
                metric_value = point.value.int64_value

            metric_data[metric_name][readable_timestamp] = metric_value

# Create the CSV file and write the header
csv_filename = 'metric_data.csv'
fieldnames = ['timestamp', 'CPU usage(%)', 'Sent Bytes', 'Received Bytes', 'Memory Utilization(%)']

with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through the timestamps and write data to CSV
    # Sort timestamps in ascending order
    timestamps = sorted(set(timestamp for data in metric_data.values() for timestamp in data.keys()))

    # Iterate through the sorted timestamps and write data to CSV
    for timestamp in timestamps:
        row = {'timestamp': timestamp}
        for metric_name in metric_data:
            if timestamp in metric_data[metric_name]:
                row[metric_name] = metric_data[metric_name][timestamp]
            else:
                row[metric_name] = ''  # Fill with empty string if value is missing
        writer.writerow(row)
        print(row)

print(f"Metric data saved to {csv_filename}")




'''
# Create the filter string for memory utilization metric
memory_utilization_filter = (
    f'resource.type="gce_instance" AND '
    f'resource.labels.instance_id="{instance_id}" AND '
    f'metric.type="agent.googleapis.com/memory/percent_used" AND '
    f'metric.labels.state="used"'
)
# Retrieve memory utilization metric data
response = client.list_time_series(
    name=f"projects/{project_id}",
    filter=memory_utilization_filter,
    interval=interval,
    view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
)

# Process and print memory utilization data
for series in response:
    for point in series.points:
        timestamp = point.interval.start_time.timestamp()
        readable_timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        memory_utilization = point.value.double_value # Convert to percentage

        print(f"Timestamp: {readable_timestamp}, Memory Utilization: {memory_utilization:.2f}%")
'''


#print(f"******************\n{response}\n***************")


