import psutil
import pyRAPL
import time

#List last 5 processes.

#print(psutil.pids())


#for num, process in enumerate(psutil.pids()):
#    print(f"{num}. process\n{psutil.Process(process)}\n*************")

#print(f"Type of psutil.pids(), {type(psutil.pids())}")
#print(f'''Try to get last 5 items of psutil.pids()
#        {psutil.pids()[-5:]}
#        ''')

## If there is a peak in the Energy Consumption
# List the last 5 processes running on the PC. 

'''
print(f"There is an unexpectional energy consumption in your computer please check following processes.")
for i in psutil.pids()[-10:]:
    p = psutil.Process(i)
    if p.status() != 'idle':
        print(f'
        Name: {p.name()}
        Status: {p.status()}
        Cpu percent: {p.cpu_percent(interval=1)}
        Cpu num: {p.cpu_num()}
        CPU Time: {p.cpu_times().user + p.cpu_times().system}

        Memory Info: {p.memory_full_info()}
        Memory Percent: {p.memory_percent()}
         ')
    time.sleep(0.1)   
'''


'''
# Track energy consumption and save it for each 10secs

#Start energy tracking
pyRAPL.setup()

#create a csv path to save results
csv_output = pyRAPL.outputs.CSVOutput('example_results.csv')

#Create the decorater
@pyRAPL.measureit(output=csv_output)
def foo():
    #Run for 5 secs.
    print("Started")
    time.sleep(5)
    print("Ended")

for i in range(5):
    foo()
    csv_output.save()
'''

#Print the process information with desired sorted format
'''
import psutil

# Get a list of running processes
processes = []
for process in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_times']):
    processes.append(process)

# Sort the processes by CPU usage in descending order
sorted_processes = sorted(processes, key=lambda process: process.info['cpu_times'].user + process.info['cpu_times'].system, reverse=True)

# Print the sorted processes
for process in sorted_processes:
    print(f"PID: {process.info['pid']}, Name: {process.info['name']}, Memory Percent: {process.info['memory_percent']}%, CPUT Time: {process.info['cpu_times'].user + process.info['cpu_times'].system}")


'''


import subprocess
import csv

# Run PowerTOP command and capture the output
command = "sudo powertop --csv=report.csv"
subprocess.run(command, shell=True)


# Read the report.csv file
with open('report.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Sort the data based on the "Usage" column in descending order
sorted_data = sorted(data, key=lambda x: float(x['Usage']), reverse=True)

# Select the top 10 power consumers
top_consumers = sorted_data[:10]

# Define the field names for the new CSV file
fieldnames = ['Usage', 'Events/s', 'Category', 'Description']

# Write the top consumers to a new CSV file
with open('top_consumers.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(top_consumers)

print("Top 10 power consumers saved to top_consumers.csv")

