from pyJoules.energy_meter import EnergyContext
from pyJoules.handler.csv_handler import CSVHandler
import time
import random
import pandas as pd
from multiprocessing import Process
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from powerTop import powerTOP

'''
In this script, we're tracking the energy consumption of different functions for each given seconds and save them into CSV files.
Using multiprocessing we also tracking the CSV files if there are new data or not. If there are new data inputs we're calculating
the total energy consumption of last n seconds.

#Future work
-The main idea is tracking the energy consumption of each 30seconds and detect and kind of unexpected power usage. For i.e
50% more power used for 30seconds. 
- Then list the most consuming 5 processes by their CPU usage or Memory usage and give a warning to user!
    - PowerTOP and psutils can be used for these purpose
'''

'''

*    Package : correspond to the wall cpu energy consumption
*    core : correpond to the sum of all cpu core energy consumption
*    uncore : correspond to the integrated GPU energy consumption

'''
#Global powertop instance
#Runs for 30secs and writes report with current timestamp.
#It takes extra 4secs to write the report
powertop_instance = powerTOP(time=8, iteration=0, latest=False)
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

# Another function 
def bar(duration):
    #Create random integers and make some calculations for in each iteration.
    try:
        i = 0
        while i<duration:
            print("bar ",i)
            time.sleep(1)
            i+=1
    except KeyboardInterrupt:
        pass 

# Livestream of the CSV file.
# Function to check if the data has changed
def has_data_changed(current_data, previous_data):
    # Compare the current data with the previous data
    return not current_data.shape[0] == previous_data.shape[0]

# Function to print the content if it has changed
def print_changed_content(filename='pyJoules_result.csv'):
    while True:
        try:
            previous_data = pd.DataFrame()  # Variable to store previous data
            previous_total = 0 # Keep the last n seconds data
            while True:
                
                current_data = pd.read_csv(filename, sep=';')  # Read the CSV file
                
                #New data enters
                if has_data_changed(current_data, previous_data):

                    #Just take the new added part and summarize the energy consumption of last x seconds and see the difference between 
                    #energy consumptions
                    last_df = current_data[~current_data.isin(previous_data)].dropna()
                    print
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
                            top_10_process = powertop_instance.get_top_process_pids()
                            print(f'TOP 10 PROCESS: {top_10_process}')

                        else:
                            print(f"Total Energy consumption decreased by {abs(difference):.2f}% compared to last {last_df['duration'].sum():.2f} seconds")
                            top_10_process = powertop_instance.get_top_process_pids()
                            print(f'TOP 10 PROCESS: {top_10_process}')

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
def track_energy(n_times):
    stop_flag = 0
    try:
        j = 0
        while j < n_times and stop_flag == 0:
            with EnergyContext(handler=csv_handler) as ctx:
                #first function
                ctx.record(tag='foo')
                foo(10)
                #second function
                #ctx.record(tag='bar')
                #bar(5)
            csv_handler.save_data()
            j+=1
            print(f'{j*10} seconds...')
        print("***********\nEnergy Consumption Tracking is OVER!\n***************")

    except KeyboardInterrupt:
        stop_flag = 1
        print("Interrupted")

'''
There is a little problem with visualization. Due to we get timestamp, the elapsed time calculating by the
timeline when the function called. If we didn't clear the pyJoules_result.csv file and run it 5 mins later it will show the
figure as it was working for 300 seconds. 
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
def run_powertop(n_times):

    for i in range(n_times):
        #Run the powertop and collect some info about power usage
        powertop_instance.run_powertop()
#Multiprocessing
if __name__=='__main__':

    p4 = Process(target=run_powertop, args=(12,))
    p4.start()
    p2 = Process(target=track_energy, args=(12,))
    p2.start()
    p1 = Process(target=print_changed_content)
    p1.start()
    p3 = Process(target=visualize)
    p3.start()

   
       
    