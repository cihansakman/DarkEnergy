from pyJoules.energy_meter import EnergyContext
from pyJoules.handler.csv_handler import CSVHandler
import time
import random
import pandas as pd

def return_random_int():
    return random.randint(-9999,99999)

# A function runs forever with 1 second breaks until user types Ctrl + C
def foo():
    try:
        i = 1
        while i<5:
            print("foo ",i)
            time.sleep(1)
            i+=1

    except KeyboardInterrupt:
        pass    

# Another function 
def bar():
    #Create random integers and make some calculations for in each iteration.
    try:
        i = 1
        while i<5:
            print("bar ",i)
            a = return_random_int()
            b = return_random_int()
            print(a, b)
            time.sleep(1)
            print(f"a: {a}, b: {b}, (a*b*(a**2/b*b**2))**0.5 : {(a*b*(a**2 / (b*b**2)))**0.5}")
            i+=1
            print("**********************\n**********************")

    except KeyboardInterrupt:
        pass 

# Livestream of the CSV file.
# Function to check if the data has changed
def has_data_changed(current_data, previous_data):
    # Compare the current data with the previous data
    return not current_data.equals(previous_data)

# Function to print the content if it has changed
def print_changed_content(filename):
    previous_data = pd.DataFrame()  # Variable to store previous data

    #while True:
    current_data = pd.read_csv(filename, sep=';')  # Read the CSV file

    if has_data_changed(current_data, previous_data):
        # Delete rows with 'tag' column value as 'start'
        current_data = current_data[current_data['tag'] != 'start']
        print(current_data)  # Print the current data if it has changed

    previous_data = current_data  # Update the previous data



'''
If you want to know where is the "hot spots" where your python code consume the most energy you can add "breakpoints" 
during the measurement process and tag them to know amount of energy consumed between this breakpoints.
'''
csv_handler = CSVHandler('pyJoules_result.csv')
with EnergyContext(handler=csv_handler) as ctx:
    for i in range(3):
        #first function
        ctx.record(tag='foo')
        foo()
        #second function
        ctx.record(tag='bar')
        bar()
csv_handler.save_data()
print_changed_content('pyJoules_result.csv')



