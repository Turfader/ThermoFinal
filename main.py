import csv
from subprocess import run
from time import time
import sys
import venv
from os import getcwd, path


# Automatic package imports
# Yes, I know there's a better way to do this. This is a just a quick and dirty solution that I know works
# Create a new virtual environment, given that there isn't one already.
venv_folder = path.join(getcwd(), "subprocess_venv")
if not path.exists(venv_folder):

    start = time()

    print("Creating virtual environment")
    venv.create("subprocess_venv", with_pip=True)

    print("Installing dependencies...")

    # Add pip installation names here for any new package.
    packages = ["numpy", "matplotlib", "DateTime", "CoolProp"]
    for package in packages:
        run([sys.executable, "-m", "pip", "install", package], check=True)
        print(f"Installed package: {package}")

    print(f"Venv creation completed in {round(time()-start, 2)}s")


# Freshly downloaded imports. Yes, I know you're not supposed to do imports anywhere other than the top of a document
import datetime
import numpy as np
from matplotlib import pyplot
# from CoolProp improt ...

# Functions for number 1 & 2
# TODO unpack csv into 2d array

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
    print("Hello, world")
  
