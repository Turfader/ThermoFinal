import csv
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import openpyxl
import os
import pint
from copy import deepcopy

np.seterr(divide='ignore', invalid='ignore')

# keep for conversion
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
ureg.formatter.default_format = '.3f'


# Functions for number 1 & 2

def convert_header(header):
    replacements = {
        "(°F)": "(°C)",
        "(gpm)": "(lpm)",
        "(SCFH)": "(cmh)",
        "(MBTU/H)": "(kW)",
        "(lbs/min)": "(kg/min)"
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

                row[5] = round((row[5] * ureg.gallon / ureg.minute).to(
                    flow_unit).magnitude, 3)  # Convert from gpm to L/min or gpm

                row[6] = round((row[6] * ureg.ft**3 / ureg.hour).to(
                    gas_flow_unit).magnitude, 3)  # Convert from SCFH to m³/h or SCFH

                # Write the converted row to the CSV
                writer.writerow(row)


def get_data_array(path="our_data_usc.csv") -> np.ndarray:
    return np.genfromtxt(path, delimiter=',', skip_header=1, dtype="str")


def make_csv(arr, unit="usc"):
    array = deepcopy(arr)
    header = ["Date", "PHWR Temp (°F)", "SHWS Temp (°F)",
              "SHWR Temp (°F)", "Common Temp (°F)", "SHWS Flow (gpm)",
              "Gas Flow (SCFH)", "Sec HTR (MBTU/H)", "Pri HTR (MBTU/H)",
              "Efficiency η", "Pri MFR (lbs/min)", "Bypass MFR (lbs/min)",
              "Percent thru Bypass (%)", "Percent thru Sec (%)"]

    if unit == "si":
        temp_unit = ureg.degC  # Celsius
        flow_unit = ureg.liters / ureg.minute  # Liters per minute
        gas_flow_unit = ureg.meter**3 / ureg.hour  # Cubic meters per hour
        sec_htr_unit = ureg.kW  # kW
        pri_htr_unit = ureg.kW  # kW
        mfr_unit = ureg.kg / ureg.minute  # kg/min
    else:
        # Default is US Customary units (usc)
        temp_unit = ureg.degF  # Fahrenheit
        flow_unit = ureg.gallon / ureg.minute  # Gallons per minute
        gas_flow_unit = ureg.ft**3 / ureg.hour  # Standard cubic feet per hour
        sec_htr_unit = ureg.MBTU * 1e-3 / ureg.hour  # MBTU/h
        pri_htr_unit = ureg.MBTU * 1e-3 / ureg.hour  # MBTU/h
        mfr_unit = ureg.lbs / ureg.minute  # lbs/min

    if unit == "si":
        header = convert_header(header)
        for row in array:
            row[1] = round(Q_(float(row[1]), ureg.degF).to(temp_unit).magnitude, 3)  # Convert from °F to target temp unit (°C or °F)
            row[2] = round(Q_(float(row[2]), ureg.degF).to(temp_unit).magnitude, 3)
            row[3] = round(Q_(float(row[3]), ureg.degF).to(temp_unit).magnitude, 3)
            row[4] = round(Q_(float(row[4]), ureg.degF).to(temp_unit).magnitude, 3)

            row[5] = round((float(row[5]) * ureg.gallon / ureg.minute).to(
                flow_unit).magnitude, 3)  # Convert from gpm to L/min or gpm

            row[6] = round((float(row[6]) * ureg.ft ** 3 / ureg.hour).to(
                gas_flow_unit).magnitude, 3)  # Convert from SCFH to m³/h or SCFH

            row[7] = round(Q_(float(row[7]), ureg.MBTU * 1e-3 / ureg.hour).to(sec_htr_unit).magnitude, 3)
            row[8] = round(Q_(float(row[8]), ureg.MBTU * 1e-3 / ureg.hour).to(pri_htr_unit).magnitude, 3)

            row[10] = round(Q_(float(row[10]), ureg.lbs / ureg.minute).to(mfr_unit).magnitude, 3)
            row[11] = round(Q_(float(row[11]), ureg.lbs / ureg.minute).to(mfr_unit).magnitude, 3)

    with open(f"final_{unit}.csv", mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write the headers
        writer.writerow(header)

        # Write the rows of the 2D array
        for row in array:
            writer.writerow(row)


# heat transfer rate function
def heat_transfer_rate(temp1, temp2, flow, fluid="water", unit="usc"):
    if fluid == "water":
        cp = 1e-3  # cp_usc MBTU / lb F for water using 1e3 for M
        if unit =="si":
            cp = 4.186  # kJ / Kg K for water
    elif fluid == "gas":
        cp = 1150e-3  # MBTU / SCF for natural gas
        if unit == "si":
            cp = 42.8e3  # kJ / m**3

    if fluid == "water":
        return flow * (temp1 - temp2) * cp
    return flow * cp


# adds calculated heat transfer rate of second loop to array
def add_sec_loop_htr(array, fluid="water", unit="usc") -> np.ndarray:
    htr_values = [
        heat_transfer_rate(
            float(row[2]), float(row[3]), float(row[5].astype(float)*60*8.33), fluid=fluid, unit=unit
        )
        for row in array
    ]
    htr_column = np.array(htr_values).reshape(-1, 1)
    return np.hstack((array, htr_column))


# adds calculated htr of primary loop to array
def add_gas_primary_htr(array, fluid="gas", unit="usc") -> np.ndarray:
    htr_values = [
        heat_transfer_rate(
            float(row[2]), float(row[1]), float(row[6]), fluid=fluid, unit=unit
        )
        for row in array
    ]
    htr_column = np.array(htr_values).reshape(-1, 1)
    return np.hstack((array, htr_column))


def plot_ht_t(x_axis, y_axis, title, unit="usc"):
    plt.title(f"{title} Heat Transfer Rate vs. Date and Time")
    plt.ylabel(f"Heat Transfer Rate {'(KW)' if unit =='si' else '(MBTU/hour)'}")
    plt.xlabel("Date and Time")
    #plt.legend()
    plt.grid(True)
    plt.plot([datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in x_axis],
             [float(value) for value in y_axis],
             color="red")  # change to plt.plot() for a line plot instead
    plt.show()  # uncomment this if you want to see the graph
    plt.savefig(f"{title} vs datetime")  # uncomment to save


def plot_eff_t(x_axis, y_axis):
    plt.title(f"Efficiency vs. Date and Time")
    plt.ylabel(f"Thermal Efficiency")
    plt.xlabel("Date and Time")
    # plt.legend()
    plt.grid(True)
    plt.plot([datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in x_axis],
             [float(value) for value in y_axis],
             color="red")  # change to plt.plot() for a line plot instead
    plt.show()  # uncomment this if you want to see the graph
    plt.savefig(f"efficiency vs datetime")  # uncomment to save


def mfr_primary(array, unit="usc"):
    cp = 1  # cp_usc BTU / lb F for water using 1e3 for M
    if unit == "si":
        cp = 4.186  # kJ / Kg K for water
    mfr = [
        float(row[8])/(cp*(float(row[2])-float(row[1])))*1e3/60  # pounds of water per minute
        for row in array
    ]
    htr_column = np.array(mfr).reshape(-1, 1)
    return np.hstack((array, htr_column))


def plot_bpp_t(x_axis, y_axis):
    plt.title(f"Bypass Pipe Percent Flow vs. Date and Time")
    plt.ylabel(f"Percent Flow")
    plt.xlabel("Date and Time")
    # plt.legend()
    plt.grid(True)
    plt.plot([datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in x_axis],
             [float(value) for value in y_axis],
             color="red")  # change to plt.plot() for a line plot instead
    plt.show()  # uncomment this if you want to see the graph
    plt.savefig(f"bpp vs datetime")  # uncomment to save


def plot_spp_t(x_axis, y_axis):
    plt.title(f"Secondary Pipe Percent Flow vs. Date and Time")
    plt.ylabel(f"Percent Flow")
    plt.xlabel("Date and Time")
    # plt.legend()
    plt.grid(True)
    plt.plot([datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in x_axis],
             [float(value) for value in y_axis],
             color="red")  # change to plt.plot() for a line plot instead
    plt.show()  # uncomment this if you want to see the graph
    plt.savefig(f"spp vs datetime")  # uncomment to save


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

    data_array = add_sec_loop_htr(data_array)

    plot_ht_t(data_array[:, 0], data_array[:, 7], "Q")
    print(f"Average Q for secondary loop (us customary) = {np.mean(data_array[:, 7].astype(float))} MBTU/hr")

    data_array = add_gas_primary_htr(data_array)

    plot_ht_t(data_array[:, 0], data_array[:, 8], "Q_comb")
    print(f"Average Q for secondary loop (us customary) = {np.mean(data_array[:, 8].astype(float))} MBTU/hr")

    print(f"average efficiency = {np.mean(data_array[:, 7].astype(float))/np.mean(data_array[:, 8].astype(float))}")

    data_array = np.column_stack((data_array, np.nan_to_num(data_array[:, 7].astype(float) / data_array[:, 8].astype(float), nan=0.0)))

    plot_eff_t(data_array[:, 0], data_array[:, 9])

    data_array = mfr_primary(data_array)

    data_array = np.column_stack((data_array, data_array[:, 10].astype(float)-data_array[:, 5].astype(float)*8.33))

    data_array = np.column_stack((data_array, np.nan_to_num(data_array[:, 11].astype(float)/data_array[:, 10].astype(float)*100, nan=0.0, posinf=0, neginf=0)))

    print(f"average percent through bypass {np.mean(data_array[:, 12].astype(float))}%")

    plot_bpp_t(data_array[:, 0], data_array[:, 12])

    data_array = np.column_stack((data_array,
                                  np.nan_to_num(data_array[:, 5].astype(float) / data_array[:, 10].astype(float) * 8.33 *100,
                                                nan=0.0, posinf=0, neginf=0)))

    print(f"average percent to school {np.mean(data_array[:, 13].astype(float))}%")

    plot_spp_t(data_array[:, 0], data_array[:, 13])

    print(data_array[0:10])

    make_csv(data_array)
    make_csv(data_array, "si")
