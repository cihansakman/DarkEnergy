import psutil
import pyRAPL
import time
import pandas as pd
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

'''
import csv


def extract_top_power_consumers(file_path):
    dataset = []
    pattern = "*  *  *   Top 10 Power Consumers   *  *  *"
    end_pattern = "____________________________________________________________________"
    found_pattern = False

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #Find the pattern
            if row and row[0].strip() == pattern:
                found_pattern = True
                continue
            #If we reach the end of the Top 10 power consumers section break the loop
            if found_pattern and (row and row[0].strip() == end_pattern):
                break 
            #Add the rows into the dataset
            elif found_pattern and len(row) > 0:
                dataset.append(row[0])
            

    return dataset

# Example usage
file_path = 'report.csv'
top_power_consumers = extract_top_power_consumers(file_path)

# Print the top power consumers
for row in top_power_consumers:
    print(row)



# Split the first item into column names
column_names = top_power_consumers[0].split(';')

# Create a DataFrame from the remaining items
df = pd.DataFrame([row.split(';') for row in top_power_consumers[1:]], columns=column_names)

print("DATAFRAME")
print(df)

df_processes = df[df['Category']=='Process']

print("df_process")
print(df_processes)

for ind in df_processes.index:
    s = df_processes['Description'][ind]
    pid = s[s.find("[")+1:s.find("]")].split()
    print(pid[1])
'''


from powerTop import powerTOP
import os

#add all csv files started with report- to a list
#sort them as their names and the biggest one will be the latest report.
powertop_instance = powerTOP(time=10, iteration=1)
#Run the powertop and collect some info about power usage
for i in range(3):
    powertop_instance.run_powertop()
prefixed = [filename for filename in os.listdir('.') if filename.startswith("report-")]



prefixed.sort(reverse=True)

for i in prefixed:
    print(i)


top_10_df = powertop_instance.get_top10_as_df()
print(top_10_df)

top_10_process = powertop_instance.get_top_process_pids()
print(top_10_process)






print(f"There is an unexpectional energy consumption in your computer please check following processes.")
for i in top_10_process:
    p = psutil.Process(i)
    if p.status() != 'idle':
        print(f'''
        Process: {p}
        PID: {p.pid}
        Name: {p.name()}
        Status: {p.status()}
        Cpu percent: {p.cpu_percent(interval=1)}
        Cpu num: {p.cpu_num()}
        CPU Time: {p.cpu_times().user + p.cpu_times().system}

        Memory Info: {p.memory_full_info()}
        Memory Percent: {p.memory_percent()}

        ***********************************
        ***********************************
         ''')
    time.sleep(0.1)   

'''
process = psutil.Process(3464)

for func_name in process.as_dict().keys():
    func = getattr(process, func_name)
    result = func()
    print(f"{func_name}: {result}")
'''
