import csv
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import openpyxl
import os
import pint
# from CoolProp import ...

# keep for conversion
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
ureg.formatter.default_format = '.3f'


# Functions for number 1 & 2

def convert_header(header):
    replacements = {
        "(°F)": "(°C)",
        "(gpm)": "(lpm)",
        "(SCFH)": "(cmh)"
    }
    converted_header = []
    for item in header:
        for old_unit, new_unit in replacements.items():
            if old_unit in item:
                item = item.replace(old_unit, new_unit)
        converted_header.append(item)
    return converted_header

def unpack_arr_and_filter(start_date=datetime(2024, 4, 26, 0, 0, 0),
                          end_date=datetime(2024, 5, 1, 0, 0, 0),
                          path_in="Temp_Boiler_Plant_Data_ Fall24.xlsx",
                          path_out="our_data_usc.csv", unit="usc") -> None:

    workbook = openpyxl.load_workbook(path_in)

    # Select the active sheet
    sheet = workbook.active

    if unit == "si":
        temp_unit = ureg.degC  # Celsius
        flow_unit = ureg.liters / ureg.minute  # Liters per minute
        gas_flow_unit = ureg.meter**3 / ureg.hour  # Cubic meters per hour
        path_out = "our_data_si.csv"
    else:
        # Default is US Customary units (usc)
        temp_unit = ureg.degF  # Fahrenheit
        flow_unit = ureg.gallon / ureg.minute  # Gallons per minute
        gas_flow_unit = ureg.ft**3 / ureg.hour  # Standard cubic feet per hour

    with open(path_out, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write the header row (first row from the sheet)
        header = [cell.value for cell in sheet[1]]
        if unit == "si":
            header = convert_header(header)
        writer.writerow(header)



        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_date = row[0]

            if start_date <= row_date <= end_date:
                # Convert the values to the appropriate units using Pint
                row = list(row)

                # Convert temperature columns (PHWR Temp, SHWS Temp, SHWR Temp, Common Temp)
                row[1] = round(Q_(row[1], ureg.degF).to(temp_unit).magnitude, 3)  # Convert from °F to target temp unit (°C or °F)
                row[2] = round(Q_(row[2], ureg.degF).to(temp_unit).magnitude, 3)
                row[3] = round(Q_(row[3], ureg.degF).to(temp_unit).magnitude, 3)
                row[4] = round(Q_(row[4], ureg.degF).to(temp_unit).magnitude, 3)

                # Convert SHWS Flow (gpm) to the desired flow unit (L/min or gpm)
                row[5] = round((row[5] * ureg.gallon / ureg.minute).to(
                    flow_unit).magnitude, 3)  # Convert from gpm to L/min or gpm

                # Convert Gas Flow (SCFH) to the desired gas flow unit (m³/h or SCFH)
                row[6] = round((row[6] * ureg.ft**3 / ureg.hour).to(
                    gas_flow_unit).magnitude, 3)  # Convert from SCFH to m³/h or SCFH

                # Write the converted row to the CSV
                writer.writerow(row)


def get_data_array(path="our_data_usc.csv") -> np.ndarray:
    return np.genfromtxt(path, delimiter=',', skip_header=1, dtype="str")


# TODO add heat transfer rate function
def heat_transfer_rate(temp1, temp2, flow, cp=1000, unit="usc"):
    if unit =="si":
        cp=4.186
    pass


# TODO add calculated heat transfer rate of second loop to array
def add_sec_loop_htr(array, unit="usc"):
    for i in len(array):
        if i == 0:
            array[i][7].append("Secondary pipe heat transfer rate")
        array[i][7].append(heat_transfer_rate(array[i][2], array[i][3], array[i][5], unit=unit))


# TODO graph calculated heat transfer rate vs. date time (secondary loop for one, primary loop for 2)
def plot(x_axis, y_axis):
    plt.title(f"{x_axis[0]} vs. {y_axis[0]}")
    plt.xlabel(x_axis[0])
    plt.ylabel(y_axis[0])
    plt.legend()
    plt.grid(True)
    plt.scatter(x_axis[1::], y_axis[1::], color="red")  # change to plt.plot() for a line plot instead
    # plt.show()  # uncomment this if you want to see the graph
    # plt.savefig(f"{x_axis[0]} vs {y_axis[0]}.png")  # uncomment to save

# Average
# to be used for average value of Q dot for number one and two, efficiency for number 3
def get_mean(array: np.ndarray) -> float:
    return np.mean(array)

# Functions for number 3

# TODO add function to calculate efficiency of boilers

# TODO graph efficiency vs datetime

# Functions for number 4
def mass_balance(SHWS, SHWR, PHWR, Q_SHWS, cp= 1000, unit="usc"):
    if unit == "si":
        cp = 4184  # J/(Kg K)

     #Calculate mass flow rate of water through bypass

     #Parameters:
     #SHWS (float): Primary Hot Water Supply Temperature (F)
     #SHWR (float): Primary Hot Water Return Temperature (F)
     #PHWR (float): Primary Hot Water Return Temperature (F)
     #Q_SHWS (float): Secondary Hot Water Supply Flowrate (MBTU/hr)
     #cp (float): Specific heat capacity of water (MBTU/lb F) {default 1000)

    #Returns:
    #float: Mass flow rate through bypass pipe (lb/hr)


    # Calculate difference in temperature of primary loop
    delta_T_primary = PHWR - SHWS

    # Calculate difference in temperature of secondary loop
    delta_T_secondary = SHWR - SHWS

    #Calculate mass flow rate through primary loop
    m_primary = Q_SHWS / (cp * delta_T_primary)

    # Calculate mass flow rate through secondary pipe
    m_secondary = Q_SHWS / (cp * delta_T_secondary)

    #Calculate mass flow rate through bypass pipe
    m_bypass = m_primary - Q_SHWS

    return m_primary, m_bypass


# TODO add function for mass balance

# TODO add function for energy balance

# TODO add function that calls mass and energy balance and gets mass flow rate

# Functions for number 5
# TODO add function to calc water mass flow rate through primary loop. Use functions from 4 with numbers from 5

# Functions for number 6
# TODO Using data from 4 and 5, function to calc water percent flowing through common pipe. Mass through bypass divided by mass through primary

# TODO graph percent vs datetime

# Functions for number 7
# TODO mass flow rate through campus

# TODO mass flow rate through campus divided by mass flowrate through primary loop (from 5)

# TODO plot percent vs datetime

# TODO get average value of percent of h2o to campus


if __name__ == "__main__":
    if not os.path.exists("our_data_usc.csv"):
        try:
            unpack_arr_and_filter()
        except FileNotFoundError:
            print("Make sure you have 'Temp_Boiler_Plant_Data_ Fall24.xlsx' in the same directory as main.py")
    if not os.path.exists("our_data_si.csv"):
        try:
            unpack_arr_and_filter(unit="si")
        except FileNotFoundError:
            print("Make sure you have 'Temp_Boiler_Plant_Data_ Fall24.xlsx' in the same directory as main.py")
    data_array = get_data_array()
    print(data_array[0])
    '''
    # Test values
    SHWS = 195.2
    SHWR = 172.7
    PHWR = 186.6
    Q_SHWS = 1329.6879

    # Print mass flow rate of primary and bypass
    mass_flow_rate_primary, mass_flow_rate_bypass = mass_balance(PHWS, PHWR, SHWS)
    print(f"Mass flow rate through the primary loop: {mass_flow_rate_primary:.2f} kg/s")
    print(f"Mass flow rate through the bypass pipe: {mass_flow_rate_bypass:.2f} kg/s")
    '''