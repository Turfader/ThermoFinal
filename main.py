import csv
from datetime import datetime
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


def get_data_array(path="our_data.csv") -> np.ndarray:
    return np.genfromtxt(path, delimiter=',', skip_header=1, dtype="str")

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
    # unpack_arr_and_filter()
    data_array = get_data_array()
    print(data_array[0])
  
