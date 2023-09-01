#First of all, create your virtual environment
#python -m venv cloud_consumption_venv
#source cloud_consumption_venv/bin/activate
#pip install google-cloud-monitoring
#bash > export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
from google.cloud import monitoring_v3
import time
import json
import csv
from datetime import datetime, timedelta

class MetricDataCollector:
    def __init__(self, credentials_path):
        # Load credentials from the JSON file
        with open(credentials_path) as json_file:
            self.credentials = json.load(json_file)
        # Replace ids with your actual project ID and instance_id
        self.project_id = self.credentials['project_id']
        self.instance_id = self.credentials['instance_id']
        self.client = monitoring_v3.MetricServiceClient()
    
    #Function to start metrics collector for 1 week as default.
    def collect_metric_data(self, time_interval_minutes=60 * 24 * 7):
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=time_interval_minutes)
        
        # Convert start and end times to seconds and nanos
        start_seconds = int(start_time.timestamp())
        end_seconds = int(end_time.timestamp())
        start_nanos = int((start_time - datetime.fromtimestamp(start_seconds)).total_seconds() * 10**9)
        end_nanos = int((end_time - datetime.fromtimestamp(end_seconds)).total_seconds() * 10**9)

        # Create TimeInterval and set start and end times
        interval = monitoring_v3.TimeInterval(
            {
                "start_time": {"seconds": start_seconds, "nanos": start_nanos},
                "end_time": {"seconds": end_seconds, "nanos": end_nanos},
            }
        )

        # Create the filter strings for 5 popular metrics.
        cpu_utilization_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{self.instance_id}" AND metric.type="compute.googleapis.com/instance/cpu/utilization"'
        received_bytes_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{self.instance_id}" AND metric.type="compute.googleapis.com/instance/network/received_bytes_count"'
        sent_bytes_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{self.instance_id}" AND metric.type="compute.googleapis.com/instance/network/sent_bytes_count"'
        memory_utilization_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{self.instance_id}" AND metric.type="agent.googleapis.com/memory/percent_used" AND metric.labels.state="used"'
        disk_utilization_filter = f'resource.type="gce_instance" AND resource.labels.instance_id="{self.instance_id}" AND metric.type="agent.googleapis.com/disk/percent_used" AND metric.labels.state = "used" AND metric.labels.device="/dev/sda1" '

        # List of filter strings
        filter_strs = [cpu_utilization_filter, received_bytes_filter, sent_bytes_filter, memory_utilization_filter, disk_utilization_filter]

        #Define human-readable metric names for dictionary keys
        metric_names = {
            cpu_utilization_filter: 'CPU usage(%)',
            received_bytes_filter: 'Received Bytes',
            sent_bytes_filter: 'Sent Bytes',
            memory_utilization_filter: 'Memory Utilization(%)',
            disk_utilization_filter: 'Disk Utilization(%)'
        }
        # Create a dictionary to store metric values for each timestamp
        metric_data = {name: {} for name in metric_names.values()}
        
        # Retrieve responses for different metrics and store data
        for filter_str in filter_strs:
            response = self.client.list_time_series(
                name=f"projects/{self.project_id}",
                filter=filter_str,
                interval=interval,
                view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
            )

            metric_name = metric_names[filter_str]
            
            for series in response:
                for point in series.points:
                    timestamp = point.interval.start_time.timestamp()
                    rounded_timestamp = datetime.fromtimestamp(timestamp).replace(second=0)
                    readable_timestamp = rounded_timestamp.strftime('%Y-%m-%d %H:%M:%S')

                    if metric_name == 'CPU usage(%)':
                        metric_value = point.value.double_value * 100.0
                    elif metric_name == 'Memory Utilization(%)' or metric_name == 'Disk Utilization(%)':
                        metric_value = point.value.double_value
                    else:
                        metric_value = point.value.int64_value

                    metric_data[metric_name][readable_timestamp] = metric_value

        # Create the CSV file and write the header
        csv_filename = 'metric_data.csv'
        fieldnames = ['timestamp', 'CPU usage(%)', 'Sent Bytes', 'Received Bytes', 'Memory Utilization(%)', 'Disk Utilization(%)']

        # Write and Save the csv file.
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            timestamps = sorted(set(timestamp for data in metric_data.values() for timestamp in data.keys()))

            for timestamp in timestamps:
                row = {'timestamp': timestamp}
                for metric_name in metric_data:
                    if timestamp in metric_data[metric_name]:
                        row[metric_name] = metric_data[metric_name][timestamp]
                    else:
                        row[metric_name] = ''
                writer.writerow(row)
                print(row)

        print(f"Metric data saved to {csv_filename}")



'''
memory_utilization_filter = (
    f'resource.type="gce_instance" AND '
    f'resource.labels.instance_id="{instance_id}" AND '
    f'metric.type="agent.googleapis.com/disk/percent_used" AND '
    f'metric.labels.device="/dev/sda1" AND metric.labels.key="used"'
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


