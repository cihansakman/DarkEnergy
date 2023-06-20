
import csv
import pandas as pd
import subprocess


#Class for executing powerTop commands.
class powerTOP:
    def __init__(self,path):
        self.path = path

    #Run the PowerTOP command
    def run_powertop(self):
        command = f"sudo powertop --csv={self.path} --time=10"
        subprocess.run(command, shell=True)

    #Extract the Top 10 Power Consumers part as a list
    def extract_top_power_consumers(self):
        dataset = []
        pattern = "*  *  *   Top 10 Power Consumers   *  *  *"
        end_pattern = "____________________________________________________________________"
        found_pattern = False

        with open(self.path, newline='') as csvfile:
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
            pids_list.append(pid[1])
        return pids_list