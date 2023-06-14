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
    j = 0
    while j < 2:
        with EnergyContext(handler=csv_handler) as ctx:
            for i in range(3):
                #first function
                ctx.record(tag='foo')
                foo(5)
                #second function
                ctx.record(tag='bar')
                bar(5)
        csv_handler.save_data()
        time.sleep(2)
        j+=1



#print_changed_content('pyJoules_result.csv')



if __name__=='__main__':
    p2 = Process(target=track_energy)
    p2.start()
    p1 = Process(target=print_changed_content)
    p1.start()
    