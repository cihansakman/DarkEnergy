import pyRAPL
import time


pyRAPL.setup() 


'''
If you want to handle data with different output than the standard one, you can configure the decorator with an Output instance
from the pyRAPL.outputs module.

As an example if you want to write the recorded energy consumption in a csv file
'''
'''
csv_output = pyRAPL.outputs.CSVOutput('result.csv')
@pyRAPL.measureit(output = csv_output)
def foo():
    for i in range(10):
        time.sleep(0.5)
        print(f"Let's sleep for {i}th time")



for _ in range(10):
    foo()

csv_output.save()
'''



###################################

# Measure the energy consumption of a piece of code

#To measure the energy consumed by the machine during the execution of a given piece of code, run the following code:

def mikroJ_to_kw_hour(mJ):
    return mJ * 2.7777777777778E-13

csv_output_of_code = pyRAPL.outputs.CSVOutput('result_of_code.csv')
measure = pyRAPL.Measurement('bar')
measure.begin()

try:
    i = 1
    while True:
        print(i)
        time.sleep(1)
        i+=1

except KeyboardInterrupt:
    pass

measure.end()
result = measure.result
print(f'PKG:{mikroJ_to_kw_hour(result.pkg[0])} kW*h, DRAM:{mikroJ_to_kw_hour(result.dram[0])} kW*h')
measure.export(csv_output_of_code)
print("\nSuccesfully saved!")
