from pyJoules.energy_meter import measure_energy
import psutil
import multiprocessing
import time

# Define the list of process names you want to track
process_names = ["firefox", "python"]

duration_sec = 30  # 30 seconds

def track_energy_consumption(pid):

    @measure_energy
    def inner_track_energy_consumption():
        # Track the energy consumption of the process while the function is running.
        # In that case it will be running for duration_sec seconds
        start_time = time.time()
        while time.time() - start_time < duration_sec:
            pass

    process = psutil.Process(pid)
    process_name = process.name()
    print(f"Tracking energy consumption for process: {process_name} (PID: {pid})")
    energy_consumption = inner_track_energy_consumption()
    return process_name, energy_consumption


def track_energy_consumptions(pid):
    process = psutil.Process(pid)
    process_name = process.name()
    print(f"Tracking energy consumption for process: {process_name} (PID: {pid})")
    energy_consumption = track_energy_consumption(pid)
    return process_name, energy_consumption

if __name__ == "__main__":
    # Get the list of running processes
    running_processes = psutil.process_iter(attrs=["name", "pid"])

    # Filter the processes to track
    processes_to_track = [
        process.info["pid"]
        for process in running_processes
        if process.info["name"] in process_names
    ]

    # Create a multiprocessing Pool
    pool = multiprocessing.Pool()

    # Track energy consumption for each process using parallel processing
    results = []
    try:
        results = pool.map(track_energy_consumptions, processes_to_track)
    except KeyboardInterrupt:
        pool.terminate()

    # Create a dictionary from the results
    energy_consumptions = {
        process_name: energy
        for process_name, energy in results
        if process_name is not None and energy is not None
    }

    # Print the energy consumption results for each process
    print(energy_consumptions)

'''
for process_name, energy_consumption in energy_consumptions.items():
        print(
            f"*************\nEnergy consumption for process {process_name}: {energy_consumption.package_0} Joules\n****************"
        )

'''
    