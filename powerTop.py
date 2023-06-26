
import csv
import pandas as pd
import subprocess
import os

#Side not
'''
If we don't want to use iterations we can call the powertop without iteration
but gives the .csv file name according to timestamp

import datetime;
 
# ct stores current time
ct = datetime.datetime.now()
-> 2020-07-15 14:30:26.159446
'''

#Class for executing powerTop commands.
class powerTOP:
    def __init__(self, time, iteration=0):
        self.time = time
        self.iteration = iteration

    #Run the PowerTOP command
    def run_powertop(self):
        #If runs with iteration it will automatically save the csv file based on timestamp
        #We can assign the path as the latest report to analyze
        if(self.iteration!=0):
            command = f"sudo powertop --csv=report.csv --time={self.time} -i {self.iteration}"
        #If there is no iteration save as @report.csv
        else:
            command = f"sudo powertop --csv=report.csv --time={self.time}"
        subprocess.run(command, shell=True)

    #Extract the Top 10 Power Consumers part as a list
    def extract_top_power_consumers(self):
        dataset = []
        pattern = "*  *  *   Top 10 Power Consumers   *  *  *"
        end_pattern = "____________________________________________________________________"
        found_pattern = False

        #Find the latest report if there is iteration
        if(self.iteration != 0):
            reports = [filename for filename in os.listdir('.') if filename.startswith("report-")]
            reports.sort(reverse=True)
            path = reports[0]
        else:
            path = 'report.csv'
        with open(path, newline='') as csvfile:
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

    #Convert the Top 10 Power Consumer list into a DataFrame
    def get_top10_as_df(self):
        top_power_consumers = self.extract_top_power_consumers()

        # Split the first item into column names
        column_names = top_power_consumers[0].split(';')

        # Create a DataFrame from the remaining items
        df = pd.DataFrame([row.split(';') for row in top_power_consumers[1:]], columns=column_names)
        return df
    #Get the most consumer processes' PIDs as a list
    def get_top_process_pids(self):
        df = self.get_top10_as_df()
        df_processes = df[df['Category']=='Process']

        pids_list = []
        for ind in df_processes.index:
            s = df_processes['Description'][ind]
            pid = s[s.find("[")+1:s.find("]")].split()
            pids_list.append(int(pid[1]))
        return pids_list