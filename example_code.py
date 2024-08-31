import subprocess
import datetime


class powerTOP:
    def __init__(self, time=10, iteration=0, latest=True):
        self.time = time
        self.iteration = iteration
        self.latest = latest

    # Run the PowerTOP command
    # If time is updated with run_powertop command
    def run_powertop(self, time):
        # If runs with iteration it will automatically save the csv file based on timestamp
        # We can assign the path as the latest report to analyze
        self.time = time
        if self.iteration != 0:
            command = (
                f"sudo powertop --csv=report.csv --time={self.time} -i {self.iteration}"
            )
        # If there is no iteration save as @report-currenttime.csv
        else:
            # take the current time
            ct = str(datetime.datetime.now())
            ct = ct.replace(" ", "-")
            path = "report-" + ct + ".csv"
            print(f"path:{path}")
            command = f"sudo powertop --csv={path} --time={self.time}"
        subprocess.run(command, shell=True)
