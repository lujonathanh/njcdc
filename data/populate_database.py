# a file that contains various code snippets for populating the database

# to populate your local database:
# run python manage.py shell, then copy this script into your shell

import pandas as pd

from zipcode_data.models import Zipcode

data = pd.read_table("data/zip_code_data_nj.txt", dtype=str)

# column names
cols =  ['ZipCode', 'Population', 'PersonsPerHousehold', 'AverageHouseValue',
       'IncomePerHousehold', 'electricity (kWh)', 'Nat. Gas (cu.ft.)',
       'FUELOIL (gallons)', 'Vehicle miles traveled', 'Transport (tCO2e/yr)',
       'Housing (tCO2e/yr)', 'Food (tCO2e/yr)', 'Goods (tCO2e/yr)',
       'Services (tCO2e/yr)', 'Total Household Carbon Footprint (tCO2e/yr)',
       'HouseholdsPerZipCode', 'Total Zip Code Carbon Footprint (tCO2e/yr)']

for i in range(len(data.index)):
    z = Zipcode(zipcode=int(data[cols[0]][i].replace(',', '')),
                population=int(data[cols[1]][i].replace(',', '')),
                persons_per_household=data[cols[2]][i].replace(',', ''),
                average_house_value=data[cols[3]][i].replace(',', ''),
                income_per_household=data[cols[4]][i].replace(',', ''),
                electricity=data[cols[5]][i].replace(',', ''),
                nat_gas=data[cols[6]][i].replace(',', ''),
                fuel_oil=data[cols[7]][i].replace(',', ''),
                vehic_miles_traveled=data[cols[8]][i].replace(',', ''),
                transport=data[cols[9]][i].replace(',', ''),
                housing=data[cols[10]][i].replace(',', ''),
                food=data[cols[11]][i].replace(',', ''),
                goods=data[cols[12]][i].replace(',', ''),
                services=data[cols[13]][i].replace(',', ''),
                total_household_footprint=data[cols[14]][i].replace(',', ''),
                households_per_zipcode=int(data[cols[15]][i].replace(',', '')),
                total_zipcode_footprint=data[cols[16]][i].replace(',', ''),
                )
    z.save()
