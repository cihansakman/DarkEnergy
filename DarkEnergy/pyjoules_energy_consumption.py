from pyJoules.energy_meter import EnergyContext
from pyJoules.handler.csv_handler import CSVHandler
import time
import os
import pandas as pd
import json
from multiprocessing import Process
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Classes
from powerTop import powerTOP
from socket_client import BackgroundSocketIO  # Import the BackgroundSocketIO class from the background_socketio.py file


'''
In this script, we're tracking the energy consumption of different functions for each given seconds and save them into CSV files.
Using multiprocessing we also tracking the CSV files if there are new data or not. If there are new data inputs we're calculating
the total energy consumption of last n seconds.

#Future work
-The main idea is tracking the energy consumption of each 30seconds and detect any kind of unexpected power usage. For i.e
50% more power used for last 30seconds. 
- Then list the most consuming 10 processes by their CPU usage or Memory usage and give a warning to user! (Gathered from PowerTop)
    - PowerTOP and psutils can be used for these purpose
'''

'''

*    Package : correspond to the wall cpu energy consumption
*    core : correpond to the sum of all cpu core energy consumption
*    uncore : correspond to the integrated GPU energy consumption

'''


#remove the reports before starting
directory = "./"

# Get a list of all files in the directory
files = os.listdir(directory)

# Iterate over the files
try:
    for file in files:
        # Check if the file starts with "report-" and has a ".csv" extension
        if file.startswith("report-") and file.endswith(".csv"):
            # Create the file path
            file_path = os.path.join(directory, file)
            # Remove the file
            os.remove(file_path)
    os.remove('./pyJoules_result.csv')
except:
    pass


#Global powertop instance
#Runs for 30secs and writes report with current timestamp.
#It takes extra 4secs to write the report
#Defualt time is 10secs but we can give the updated time using run_powertop() function
powertop_instance = powerTOP(iteration=0, latest=False)
#Target csv file to store pyJoules energy measurements
csv_handler = CSVHandler('pyJoules_result.csv')

# Convert mikroJ to kW
def mikroJ_to_kw_hour(mJ):
    return mJ * 2.7777777777778E-13

#Format scientific notation into more readible format.
def format_scientific_notation(number):
    formatted = "{:.2e}".format(number)
    coefficient, exponent = formatted.split("e")
    coefficient = float(coefficient)
    exponent = int(exponent)
    return f"{coefficient}x10^-{exponent}"

#Calculate efficiency difference in percentages
def efficiency_difference(before, after):
    return ((after - before) / before ) * 100

# A function with 1 second breaks until user types Ctrl + C
def foo(duration):
    try:
        i = 1
        while i<duration+1:
            if(i%5==0):
                print('foo', i)
            time.sleep(1)
            i+=1
    except KeyboardInterrupt:
        pass    

# Livestream of the CSV file.
# Function to check if the data has changed
def has_data_changed(current_data, previous_data):
    # Compare the current data with the previous data
    return not current_data.shape[0] == previous_data.shape[0]

#Get the tab titles based on OSids from ChromeExtension's processes JSON file.
#Keeps the titles as key-value pairs of OSid: Tab Title
def get_tab_titles(osids, json_file_path='data_from_socket.json'):
    try:
        with open(json_file_path) as f:
            data = json.load(f)
            processes = data.get('processes', {})
            
            tab_titles = {}
            for process in processes.values():
                os_process_id = process.get('osProcessId')
                if os_process_id in osids:
                    tasks = process.get('tasks', [])
                    for task in tasks:
                        title = task.get('title')
                        if title:
                            tab_titles[os_process_id] = title
            
            return tab_titles
    except:
        print(f"Most probably there is no filed called {json_file_path}")


# Function to print the content if it has changed
#   - When pyJoules calculates the new 'n' time period of power usage, it will update the csv file.
def print_changed_content(filename='pyJoules_result.csv'):
    while True:
        try:
            previous_data = pd.DataFrame()  # Variable to store previous data
            previous_total = 0 # Keep the last n seconds data
            while True:
                current_data = pd.read_csv(filename, sep=';')  # Read the CSV file

                #New data enters
                if has_data_changed(current_data, previous_data):
                    #Just take the new added part and summarize the energy consumption of last n seconds and see the difference between energy consumptions
                    last_df = current_data[~current_data.isin(previous_data)].dropna()
                    print(f'''
********************************************************************************************************
                    Summary of last {last_df['duration'].sum():.2f} seconds
                    All cpu core energy consumption: {format_scientific_notation(last_df['core_0'].sum())} kw/h
                    Integrated GPU energy consumption: {format_scientific_notation(last_df['uncore_0'].sum())} kw/h
                    Memory energy consumption: {format_scientific_notation(last_df['dram_0'].sum())} kw/h
********************************************************************************************************
                    ''')

                    #Compare the energy consumption difference with last n seconds
                    current_total = last_df['core_0'].sum() + last_df['uncore_0'].sum() + last_df['dram_0'].sum()
                    #previous_total = previous_last_df['core_0'].sum() + previous_last_df['uncore_0'].sum() + previous_last_df['dram_0'].sum()
                    
                    #If there is previous data
                    if(previous_total != 0):
                        #calculate the efficiency
                        difference = efficiency_difference(previous_total, current_total)
                        if(difference > 0):
                            print(f"Total Energy consumption increased by {abs(difference):.2f}% compared to last {last_df['duration'].sum():.2f} seconds")
                        else:
                            print(f"Total Energy consumption decreased by {abs(difference):.2f}% compared to last {last_df['duration'].sum():.2f} seconds")
                    

                        #Get the top 10 processes from PowerTop instance
                        top_10_process = powertop_instance.get_top_process_pids()
                        print(f'TOP 10 PROCESS: {top_10_process}')

                        try:
                            #Print the most energy consuming chrome tabs with their title
                            chrome_tabs = get_tab_titles(top_10_process)
                            print("Most Energy consuming Chrome Tabs Listed Below")
                            for key in top_10_process:
                                if key in chrome_tabs:
                                    print(f'* {key}: {chrome_tabs[key]}')
                        except:
                            pass

                    previous_total = current_total #update previous_total

                previous_data = current_data  # Update the previous data
                time.sleep(2)

        #If there is no such a file as pyJoules_result.csv wait until it created by pyJoules
        except FileNotFoundError:
            time.sleep(5)
            pass

'''
If you want to know where is the "hot spots" where your python code consume the most energy you can add "breakpoints" 
during the measurement process and tag them to know amount of energy consumed between this breakpoints.
'''
def track_energy(n_times, n_seconds):
    stop_flag = 0
    try:
        j = 0
        while j < n_times and stop_flag == 0:
            with EnergyContext(handler=csv_handler) as ctx:
                #first function
                ctx.record(tag='foo')
                foo(n_seconds)
            csv_handler.save_data()
            j+=1
            print(f'{j*n_seconds} seconds...')
        print("***********\nEnergy Consumption Tracking is OVER!\n***************")

    except KeyboardInterrupt:
        stop_flag = 1
        print("Interrupted")

'''
There is a little problem with visualization. Due to we get timestamp, the elapsed time calculating by the
timeline when the function called. If we didn't clear the pyJoules_result.csv file and run it 5 mins later it will show the
figure as it was working for 300 seconds. 

Temporary solution: Remove pyJoules_result.csv file in each run
'''
def visualize():
    try:
        #Style for plot
        plt.style.use('fivethirtyeight')

        # Initialize the figure and axis
        fig, ax = plt.subplots()

        def animate(i):
            #Create a while loop if there is no such CSV file and wait until it is created...
            while True:
                try:
                    # Read the CSV file with ';' delimiter
                    df = pd.read_csv('pyJoules_result.csv', delimiter=';')
                    #Do not get the rows with start tag.
                    df = df[df['tag'] != 'start']

                    # Convert the timestamp column to datetime format
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

                    # Calculate the elapsed time since the earliest timestamp
                    df['elapsed_time'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()

                    # Clear the plot
                    ax.clear()

                    # Plot the data
                    '''
                    Package_0 refers to the energy consumption of the entire package, which typically includes
                    the CPU cores, integrated GPU, and other components on the chip. It represents the total power
                    consumed by the processor package.

                    In order to calculate total energy consumption we should sum them up with DRAM energy consumtpion
                    '''
                    ax.plot(df['elapsed_time'], (mikroJ_to_kw_hour(df['package_0'])+mikroJ_to_kw_hour(df['dram_0'])))

                    # Set labels and title
                    ax.set_xlabel('Elapsed Time (seconds)')
                    ax.set_ylabel('Power Consumption (kw/h)')
                    ax.set_title('Power Consumption over Time')

                    # Format x-axis
                    plt.gcf().autofmt_xdate()

                    # Adjust layout
                    plt.tight_layout()
                    plt.show()
                    break
                except:
                    print("There is no such a CSV file please wait until it's created...")
                    time.sleep(5)


        # Create the animation
        ani = FuncAnimation(fig, animate, interval=1000)
        
        #plt.tight_layout()
        plt.show()
        # Save the plot as an image file
        plt.savefig('energy_consumption_plot.png')
    except KeyboardInterrupt:
        # Save the plot as an image file
        plt.savefig('energy_consumption_plot.png')

#Function to run power_top. The object will be assigned globally
def run_powertop(n_times, n_seconds):
    for i in range(n_times):
        #Run the powertop and collect some info about power usage
        powertop_instance.run_powertop(n_seconds)


def main():
    # Create an instance of the BackgroundSocketIO class
    background_socketio = BackgroundSocketIO()

    # Start the background thread
    background_socketio.start()

    # Create and start the processes
    p1 = Process(target=run_powertop, args=(12, 20))
    p1.start()
    p2 = Process(target=visualize)
    p2.start()
    p3 = Process(target=track_energy, args=(12, 20))
    p3.start()
    p4 = Process(target=print_changed_content)
    p4.start()

    # Wait for the other processes to finish
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    # Wait for the background thread to finish (optional)
    background_socketio.join()


#Multiprocessing
if __name__=='__main__':
    main()


   
       
    