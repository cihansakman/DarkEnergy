# Computer Energy and Data Consumption Tracker

This repository provides tools for tracking energy consumption and data consumption on a single computer. It utilizes various libraries to monitor and measure the energy usage of the CPU and track data consumption on the system.

## Computer Hardware

### CPU

- Model name: Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz
- CPU family: 6
- Model: 142
- Thread(s) per core: 2
- Core(s) per socket: 4
- Size: 2975MHz
- Capacity: 4200 MHz

### GPU

- Description: VGA compatible controller
- Product: UHD Graphics 620
- Vendor: Intel Corporation
- Version: 07
- Width: 64 bits
- Clock: 33MHz

## Energy Consumption

This repository provides two libraries for tracking energy consumption:

### pyJoules

pyjoules is a Python library that allows you to measure and monitor energy consumption on systems with Intel RAPL (Running Average Power Limit) support. It provides a simple and convenient way to access energy-related information, such as package power and energy consumption.

You can find more information about pyjoules on its [GitHub repository](https://github.com/powerapi-ng/pyJoules/blob/master/README.md#rapl-domain-description).


#### pyJoules-Nvidia GPU

pyJoules uses the nvidia "Nvidia Management Library" technology to measure energy consumption of nvidia devices. The energy measurement API is only available on nvidia GPU with Volta architecture(2018)

#### pyJoules Example output

```
begin timestamp : 1685697444.8609605; tag : foo; duration : 4.584830045700073; package_0 : 11390718.0; dram_0 : 3499747.0; core_0 : 1680782.0; uncore_0 : 138610.0
```

- package_0: This refers to the energy consumption of the entire package, which typically includes the CPU cores, integrated GPU, and other components on the chip. It represents the total power consumed by the processor package.

- dram_0: This represents the energy consumption of the Dynamic Random Access Memory (DRAM), which is the primary memory used by the system. It indicates the power consumed by the memory modules and controllers.

- core_0: This denotes the energy consumption of the CPU cores. It represents the power consumed by the processing units (cores) of the CPU during the execution of your code.

- uncore_0: This refers to the energy consumption of the uncore components. The uncore includes parts of the CPU that are not directly related to the cores, such as the memory controller, cache hierarchy, and other on-chip components. It represents the power consumed by these components.

The output displays the energy measurements for the specified duration. The values for package_0, dram_0, core_0, and uncore_0 are given in joules (J) and indicate the total energy consumed by each component during the execution of the function.

### pyRAPL

pyRAPL is another Python library that enables you to measure and monitor energy consumption on Intel platforms using the RAPL interface. It provides a high-level API to measure energy usage at different levels, such as package, DRAM, and individual cores.

More details about pyRAPL can be found on its [GitHub repository](https://github.com/powerapi-ng/pyRAPL).

## Data Consumption

For tracking data consumption, this repository utilizes the following library:

### psutil

psutil is a cross-platform library for retrieving information on running processes and system utilization, including CPU, memory, disk, and network usage. It provides various functions and methods to monitor network traffic and calculate data consumption.

You can learn more about psutil and its capabilities on its [GitHub repository](https://github.com/giampaolo/psutil).

