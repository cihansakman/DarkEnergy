# GcpFootprintEstimationConstants from 2021
# https://github.com/cloud-carbon-footprint/cloud-carbon-footprint/blob/trunk/packages/gcp/src/domain/GcpFootprintEstimationConstants.ts


# Other constants
MIN_WATTS_MEDIAN =  0.68 # wH
MAX_WATTS_MEDIAN =  4.11 # wH
#how many watt-hours (Wh) it takes to store a terabyte of data on HDD or SSD 
SSDCOEFFICIENT = 1.2 # watt hours / terabyte hour
HDDCOEFFICIENT = 0.65 # watt hours / terabyte hour
NETWORKING_COEFFICIENT = 0.001 # kWh / Gb
MEMORY_COEFFICIENT = 0.000392 # kWh / Gb
PUE_AVG = 1.1


# Constants related to processor types in wH
MIN_WATTS_BY_COMPUTE_PROCESSOR = {
    "CASCADE_LAKE": 0.64,
    "SKYLAKE": 0.65,
    "BROADWELL": 0.71,
    "HASWELL": 1,
    "COFFEE_LAKE": 1.14,
    "SANDY_BRIDGE": 2.17,
    "IVY_BRIDGE": 3.04,
    "AMD_EPYC_1ST_GEN": 0.82,
    "AMD_EPYC_2ND_GEN": 0.47,
    "AMD_EPYC_3RD_GEN": 0.45,
}

MAX_WATTS_BY_COMPUTE_PROCESSOR = {
    "CASCADE_LAKE": 3.97,
    "SKYLAKE": 4.26,
    "BROADWELL": 3.69,
    "HASWELL": 4.74,
    "COFFEE_LAKE": 5.42,
    "SANDY_BRIDGE": 8.57,
    "IVY_BRIDGE": 8.25,
    "AMD_EPYC_1ST_GEN": 2.55,
    "AMD_EPYC_2ND_GEN": 1.69,
    "AMD_EPYC_3RD_GEN": 2.02,
}

PUE_TRAILING_TWELVE_MONTH = {
    "US_EAST4": 1.08,
    "US_CENTRAL1": 1.11,
    "US_CENTRAL2": 1.11,
    "EUROPE_WEST1": 1.09,
    "EUROPE_WEST4": 1.07,
    "EUROPE_NORTH1": 1.09,
    "ASIA_EAST1": 1.12,
    "ASIA_SOUTHEAST1": 1.13,
}




# Function to calculate min watts, by default return MEDIAN
def getMinWatts(computeProcessor=None):
    if computeProcessor:
        return MIN_WATTS_BY_COMPUTE_PROCESSOR.get(computeProcessor, MIN_WATTS_MEDIAN)
    else:
        return MIN_WATTS_MEDIAN

# Function to calculate max watts, by default return MEDIAN
def getMaxWatts(computeProcessor=None):
    if computeProcessor:
        return MAX_WATTS_BY_COMPUTE_PROCESSOR.get(computeProcessor, MAX_WATTS_MEDIAN)
    else:
        return MAX_WATTS_MEDIAN

# Function to get PUE value by region, by default return AVG
def getPUE(region=None):
    if region:
        return PUE_TRAILING_TWELVE_MONTH.get(region, PUE_AVG)
    else:
        return PUE_AVG
