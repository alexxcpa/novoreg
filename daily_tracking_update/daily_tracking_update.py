import os.path
import requests
import datetime as dt
import pandas as pd
import time

from get_affise_charge_data import get_affise_charge_data
from add_affmen_data_in_sheets import add_affmen_data_in_sheets

def main():

    add_affmen_data_in_sheets(get_affise_charge_data())

if __name__ == "__main__":
  main()