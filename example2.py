import psutil
import pyRAPL
import time

#List last 5 processes.

print(psutil.pids())

for num, process in enumerate(psutil.pids()):
    print(f"{num}. process\n{psutil.Process(process)}\n*************")

print(f"Type of psutil.pids(), {type(psutil.pids())}")
print(f'''Try to get last 5 items of psutil.pids()
        {psutil.pids()[-5:]}
        ''')

## If there is a peak in the Energy Consumption
# List the last 5 processes running on the PC. 
print(f"There is an unexpectional energy consumption in your computer please check following processes.")
for i in psutil.pids()[-5:]:
    p = psutil.Process(i)
    if p.status() != 'idle':
        print(f'''
        Name: {p.name()}
        Status: {p.status()}
        Cpu percent: {p.cpu_percent(interval=1)}
        Cpu percent: {p.cpu_percent(interval=1)}
        CPU Time: {p.cpu_times().user + p.cpu_times().system}
         ''')
    time.sleep(0.1)   




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

