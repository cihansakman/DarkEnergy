from pyJoules.energy_meter import EnergyContext
from pyJoules.handler.csv_handler import CSVHandler
import time
import random
import pandas as pd
from multiprocessing import Process

'''
In this script, we're tracking the energy consumption of different functions for each given seconds and save them into CSV files.
Using multiprocessing we also tracking the CSV files if there are new data or not. If there are new data inputs we're calculating
the total energy consumption of last n seconds.

#Future work
-The main idea is tracking the energy consumption of each 30seconds and detect and kind of unexpected power usage. For i.e
%25 more power used for 30seconds. 
- Then list the most consuming 5 processes by their CPU usage or Memory usage and give a warning to user!
'''


'''

*    Package : correspond to the wall cpu energy consumption
*    core : correpond to the sum of all cpu core energy consumption
*    uncore : correspond to the integrated GPU

'''

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

def return_random_int():
    return random.randint(-9999,99999)

#Calculate efficiency difference
def efficiency_difference(before, after):
    return ((after - before) / before ) * 100

# A function runs forever with 1 second breaks until user types Ctrl + C
def foo(duration):
    try:
        i = 1
        while i<duration:
            print("foo ",i)
            time.sleep(1)
            i+=1

    except KeyboardInterrupt:
        pass    

# Another function 
def bar(duration):
    #Create random integers and make some calculations for in each iteration.
    try:
        i = 1
        while i<duration:
            print("bar ",i)
            a = return_random_int()
            b = return_random_int()
            #print(a, b)
            time.sleep(1)
            #print(f"a: {a}, b: {b}, (a*b*(a**2/b*b**2))**0.5 : {(a*b*(a**2 / (b*b**2)))**0.5}")
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
                print("Print changed content")

                #while True:
                current_data = pd.read_csv(filename, sep=';')  # Read the CSV file

                print(f"previous_data shape: {previous_data.shape[0]}, current_data shape: {current_data.shape[0]}")

                if has_data_changed(current_data, previous_data):
                    # Delete rows with 'tag' column value as 'start'
                    #current_data = current_data[current_data['tag'] != 'start']
                    print(current_data)  # Print the current data if it has changed

                    #Just take the new added part and summarize the energy consumption of last x seconds and see the difference between 
                    #energy consumptions
                    last_df = current_data[~current_data.isin(previous_data)].dropna()
                    print("**************************")
                    print(f'''
                    Summary of last {last_df['duration'].sum():.2f} seconds
                    All cpu core energy consumption: {format_scientific_notation(last_df['core_0'].sum())} kw/h
                    Integrated GPU energy consumption: {format_scientific_notation(last_df['uncore_0'].sum())} kw/h
                    Memory energy consumption: {format_scientific_notation(last_df['dram_0'].sum())} kw/h
                    ''')

                    #Compare the energy consumption difference with last n seconds
                    current_total = last_df['core_0'].sum() + last_df['uncore_0'].sum() + last_df['dram_0'].sum()
                    #previous_total = previous_last_df['core_0'].sum() + previous_last_df['uncore_0'].sum() + previous_last_df['dram_0'].sum()
                    
                    if(previous_total != 0):
                        difference = efficiency_difference(previous_total, current_total)
                        if(difference > 0):
                            print(f"Total Energy consumption increased by {abs(difference):.2f}%")

                        else:
                            print(f"Total Energy consumption decreased by {abs(difference):.2f}%")


                    previous_total = current_total #update previous_total

                previous_data = current_data  # Update the previous data
                time.sleep(2)
        except FileNotFoundError:
            time.sleep(5)
            pass



'''
If you want to know where is the "hot spots" where your python code consume the most energy you can add "breakpoints" 
during the measurement process and tag them to know amount of energy consumed between this breakpoints.
'''
csv_handler = CSVHandler('pyJoules_result.csv')
def track_energy():
    stop_flag = 0
    try:
        j = 0
        while j < 2 and stop_flag == 0:
            with EnergyContext(handler=csv_handler) as ctx:
                for i in range(3):
                    #first function
                    ctx.record(tag='foo')
                    foo(3)
                    #second function
                    ctx.record(tag='bar')
                    bar(3)
            csv_handler.save_data()
            time.sleep(2)
            j+=1
        print("***********\nEnergy Consumption Tracking is OVER!\n***************")
    except KeyboardInterrupt:
        stop_flag = 1
        print("Interrupted")


#print_changed_content('pyJoules_result.csv')

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



def visualize():
    #Style for plot
    plt.style.use('fivethirtyeight')

    # Initialize the figure and axis
    fig, ax = plt.subplots()

    def animate(i):
        #Create a while loop if there is no such a CSV file wait until it is creating...
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
                ax.plot(df['elapsed_time'], df['package_0'])

                # Set labels and title
                ax.set_xlabel('Elapsed Time (seconds)')
                ax.set_ylabel('Energy Consumption (package_0)')
                ax.set_title('Energy Consumption over Time')

                # Format x-axis
                plt.gcf().autofmt_xdate()

                # Adjust layout
                plt.tight_layout()
                plt.show()
                break
            except:
                print("There is no such a CSV file please wait until it is creating...")
                time.sleep(5)


    # Create the animation
    ani = FuncAnimation(fig, animate, interval=1000)

    plt.tight_layout()
    plt.show()


if __name__=='__main__':
   
    p2 = Process(target=track_energy)
    p2.start()
    p1 = Process(target=print_changed_content)
    p1.start()
    visualize()
    
    