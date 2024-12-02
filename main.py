import csv
from datetime import datetime
from idlelib.sidebar import ShellSidebar

import numpy as np
from matplotlib import pyplot
import openpyxl
# from CoolProp import ...


# Functions for number 1 & 2
def unpack_arr_and_filter(start_date=datetime(2024, 4, 26, 0, 0, 0),
                          end_date=datetime(2024, 5, 1, 0, 0, 0),
                          path_in="Temp_Boiler_Plant_Data_ Fall24.xlsx",
                          path_out="our_data.csv") -> None:
    workbook = openpyxl.load_workbook(path_in)

    # Select the active sheet
    sheet = workbook.active

    with open(path_out, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write the header row (first row from the sheet)
        header = [cell.value for cell in sheet[1]]
        writer.writerow(header)

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_date = row[0]

            if start_date <= row_date <= end_date:
                writer.writerow(row)


# TODO add heat transfer rate function

# TODO add calculated heat transfer rate of second loop to array

# TODO graph calculated heat transfer rate vs. date time (secondary loop for one, primary loop for 2)

# Average
# to be used for average value of Q dot for number one and two, efficiency for number 3
def get_mean(array: np.ndarray) -> float:
    return np.mean(array)

# Functions for number 3

# TODO add function to calculate efficiency of boilers

# TODO graph efficiency vs datetime

# Functions for number 4
def mass_balance(SHWS, SHWR, PHWR, Q_SHWS, cp= 1000):

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

# Test values
SHWS = 195.2
SHWR = 172.7
PHWR = 186.6
Q_SHWS = 1329.6879

# Print mass flow rate of primary and bypass
mass_flow_rate_primary, mass_flow_rate_bypass = mass_balance(PHWS, PHWR, SHWS)
print(f"Mass flow rate through the primary loop: {mass_flow_rate_primary:.2f} kg/s")
print(f"Mass flow rate through the bypass pipe: {mass_flow_rate_bypass:.2f} kg/s")

### If you want to work on code, 4 would be a good place to do so
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
    unpack_arr_and_filter()
  
