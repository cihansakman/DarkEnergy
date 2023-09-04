from gcp_cloud_constants import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class MetricAnalyzer:
    def __init__(self, metric_data_file, compute_processor, DISKSPACE, MEMORY, region):
        self.metric_data_file = metric_data_file
        self.compute_processor = compute_processor
        self.DISKSPACE = DISKSPACE
        self.MEMORY = MEMORY
        self.region = region

    #Function to calculate power consumptions based on given metrics in Watts
    def calculate_power_consumption_watts(self, cpu_utilization, memory_utilization, network_traffic, disk_utilization):

        #GET MIN AND MAX PROCESSOR WATTS FROM GCP CONSTANTS
        min_watts = getMinWatts(self.compute_processor)
        max_watts = getMaxWatts(self.compute_processor)
        # Calculate energy usage for CPU and memory
        cpu_energy =((cpu_utilization / 100) * (max_watts - min_watts) + min_watts)
        memory_energy =  (self.MEMORY * (memory_utilization / 100) * MEMORY_COEFFICIENT) * 1000 # kw to W  


        # Calculate energy usage for network and disk
        network_energy = ((network_traffic / (1024 * 1024 * 1024)) * NETWORKING_COEFFICIENT) * 1000  # Convert bytes to W/GB/h
        disk_energy = ((((self.DISKSPACE * disk_utilization) / 100) / 1024) * HDDCOEFFICIENT) # Converts gb to tb / hour

        # Total energy consumption before applying PUE
        total_energy_before_pue = (cpu_energy*60) + (memory_energy*60) + network_energy + (disk_energy*60)

        # Apply PUE for region
        # If region is not found it will return avg PUE for GCP
        pue = getPUE(self.region)
        total_energy = total_energy_before_pue * pue

        return total_energy
    #Function to convert csv into dataframe and process the data
    #Group by the Metricses by hour
    #Calculate power consumption for each hour
    def load_metric_data(self):
        #Read data
        data = pd.read_csv(self.metric_data_file, parse_dates=['timestamp'])
        #Drop NaN values
        dropped_data = data.dropna(inplace=False)
        # Set the timestamp column as index
        dropped_data.set_index('timestamp', inplace=True)

        #Resample the data by hours, calculating the mean for CPU Usage(%), Disk Utilization(%) and Memory Utilization(%), and the sum for Sent Bytes and Received Bytes
        resampled_df = dropped_data.resample('H').agg({
            'CPU usage(%)': 'mean',
            'Memory Utilization(%)': 'mean',
            'Sent Bytes': 'sum',
            'Received Bytes': 'sum',
            'Disk Utilization(%)': 'mean'
        })
        
        #Apply power consumption function and add it as a new column
        resampled_df['PowerConsumption(Wh)'] = resampled_df.apply(
            lambda row: self.calculate_power_consumption_watts(
                row['CPU usage(%)'],
                row['Memory Utilization(%)'],
                row['Sent Bytes'] + row['Received Bytes'],
                row['Disk Utilization(%)']
            ),
            axis=1
        )

        return resampled_df

    def plot_metrics(self, df):
        sns.set_style("whitegrid")
        timestamps = df.index
        cpu_usage = df["CPU usage(%)"]
        memory_utilization = df["Memory Utilization(%)"]
        sent_bytes = df["Sent Bytes"]
        received_bytes = df["Received Bytes"]
        power_consumption = df["PowerConsumption(Wh)"]

        fig, axs = plt.subplots(2, 2, figsize=(15, 10))

        axs[0, 0].plot(timestamps, cpu_usage, label="CPU Usage(%)", color="blue")
        axs[0, 0].set_title("CPU Usage over Time")
        axs[0, 0].set_xlabel("Timestamp")
        axs[0, 0].set_ylabel("CPU Usage(%)")
        axs[0, 0].set_xticklabels(axs[0, 0].get_xticklabels(), rotation=45)  # Rotate x-values by 45 degrees

        axs[0, 1].plot(timestamps, memory_utilization, label="Memory Utilization(%)", color="green")
        axs[0, 1].set_title("Memory Utilization over Time")
        axs[0, 1].set_xlabel("Timestamp")
        axs[0, 1].set_ylabel("Memory Utilization(%)")
        axs[0, 1].set_xticklabels(axs[0, 1].get_xticklabels(), rotation=45)  # Rotate x-values by 45 degrees

        sent_received_sum = sent_bytes + received_bytes
        axs[1, 0].plot(timestamps, sent_bytes, label="Sent Bytes", color="orange")
        axs[1, 0].plot(timestamps, received_bytes, label="Received Bytes", color="red")
        axs[1, 0].plot(timestamps, sent_received_sum, label="Sent+Received Bytes", color="purple", linestyle="--")
        axs[1, 0].set_title("Sent and Received Bytes over Time")
        axs[1, 0].set_xlabel("Timestamp")
        axs[1, 0].set_ylabel("Bytes")
        axs[1, 0].set_xticklabels(axs[1, 0].get_xticklabels(), rotation=45)  # Rotate x-values by 45 degrees
        axs[1, 0].legend()

        axs[1, 1].plot(timestamps, power_consumption, label="Energy Consumption(Wh)", color="brown")
        axs[1, 1].set_title("Energy Consumption over Time")
        axs[1, 1].set_xlabel("Timestamp")
        axs[1, 1].set_ylabel("Energy Consumption(Wh)")
        axs[1, 1].set_xticklabels(axs[1, 1].get_xticklabels(), rotation=45)  # Rotate x-values by 45 degrees

        # Format timestamps without the year
        # Format timestamps as MM-DD without the year
       # Format timestamps as MM-DD without the year
        timestamps = df.index
        
       


        plt.tight_layout()
        plt.show()


