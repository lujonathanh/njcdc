
###### POLICY PARAMETERS #########

# per ton CO2
FEE = 30

# amount going back to households
REBATE_PORTION = 0.7

# child multiplier
CHILD_MULTIPLIER = 0.5


##########  ENERGY PARAMETERS ****#


###### GASOLINE CHOICES

GASOLINE_CHOICES = (('e10', 'Regular Gasoline'), ('e0', 'Pure Gasoline'), ('diesel', 'Diesel'), ('b20', '20% Biodiesel'))


###### GASOLINE PARAMETERS
e10_ton_co2_per_gallon = 17.6/2204.6
# https://www.eia.gov/tools/faqs/faq.php?id=307&t=11

e0_ton_co2_per_gallon = 19.6/2204.6

diesel_ton_co2_per_gallon = 22.4/2204.6

b20_ton_co2_per_gallon = 17.9/2204.6




## HEATING

######## HEATING CHOICES
HEATING_CHOICES = ( ('gas', 'Natural Gas'), ('fuel', 'Fuel Oil'))

######## HEATING PARAMETERS

natural_gas_ton_co2_per_therm = 0.0053
# Natural Gas CO2/therm: https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references
# 0.0053 metric tons CO2/therm

fuel_oil_ton_co2_per_gallon = 10.16 * 0.001
# Distillate Fuel Oil (Home Heating Fuel) https://www.eia.gov/environment/emissions/co2_vol_mass.php
# 10.16 kg CO2/gallon * 0.001 metric tons/kg


## ELECTRIC

elec_coal_ton_co2_per_kwh = 10045./3412. * 0.0034095 * 26.05 * 11./3 * 0.001
# kwH of Coal per kwH generated is the average heat rate, 10045, divided by 3412
# https://www.eia.gov/electricity/annual/html/epa_08_02.html, accessed 4/1/2018
# 0.0034095 MMBtu/kWh https://www.unitjuggler.com/convert-energy-from-kWh-to-MMBtu.html
# 26.05 kg C/mmbtu Coal https://www.epa.gov/ghgemissions/inventory-us-greenhouse-gas-emissions-and-sinks-1990-2015, Annex 2, Table A40. Year 2015
# 11/3 kg CO2/kg C
# 0.001 ton/kg

elec_oil_ton_co2_per_kwh = 13535./3412. * 0.0034095 * 20.31 * 11./3 * 0.001
# kwH of Oil per kwH generated is the average heat rate, 13535, divided by 3412, which is 1  kwH of electricity
# The heat rate ranges from 9860 to 13535 https://www.eia.gov/electricity/annual/html/epa_08_02.html, accessed 4/1/2018
# 0.0034095 MMBtu/kWh https://www.unitjuggler.com/convert-energy-from-kWh-to-MMBtu.html
# 20.31 C/mmbtu Oil https://www.epa.gov/ghgemissions/inventory-us-greenhouse-gas-emissions-and-sinks-1990-2015, Annex 2, Table A40. Year 2015
# 11/3 kg CO2/kg C
# 0.001 ton/kg

elec_natural_gas_ton_co2_per_kwh = 11214./3412. * 0.0034095 * 14.46 * 11./3 * 0.001
# kwH of Gas per kwH generated is the average heat rate, 11214, divided by 3412
# The heat rate ranges from 7652 to 11214 https://www.eia.gov/electricity/annual/html/epa_08_02.html, accessed 4/1/2018
# 0.0034095 MMBtu/kWh https://www.unitjuggler.com/convert-energy-from-kWh-to-MMBtu.html
# 14.46 C/mmbtu Gas https://www.epa.gov/ghgemissions/inventory-us-greenhouse-gas-emissions-and-sinks-1990-2015, Annex 2, Table A40. Year 2015
# 11/3 kg CO2/kg C
# 0.001 ton/kg

elec_nuclear_ton_co2_per_kwh = 0
elec_clean_ton_co2_per_kwh = 0



## ELECTRIC UTILITY

######## UTILITY CHOICES

ELEC_CHOICES = ( ('pseg', 'PSE&G'), ('rockland', 'Orange Rockland Electric'),
                 ('jcpl', 'Jersey Central Power & Light'), ('atlantic', 'Atlantic City Electric'))


######## UTILITY PARAMETERS


### YOU MUST DEFINE A DICTIONARY WITH the relative proportions of:
#  'coal', 'gas', 'nuclear', 'oil', 'clean'
# These must add up to 1. (Don't worry, if you made a mistake, the model will throw you an error)

pseg_fuel_makeup = {'coal': 0.2184,
                           'gas': 0.2247,
                           'nuclear': 0.3953,
                           'oil': 0.0012,
                           'clean': 0.0004 + 0.0198 + 0.0002 + 0.00 + 0.0005 + 0.0299 + 0.0241 + 0.0851 + 0.0004}
# PSE&G
# https://www.pseg.com/info/environment/envirolabel.jsp, accessed 3/31/2018
# Time Range: June 1, 2016 - May 31, 2017

jcpl_fuel_makeup = {'coal': 0.3286,
                           'gas': 0.2476,
                           'nuclear': 0.3688,
                           'oil': 0.0023,
                           'clean': 0.0171 + 0.0003 + 0.0033 + 0.00 + 0.00 + 0.0009 + 0.0057 + 0.0229 + 0.0025}
# Jersey Central Power & Light
# https://www.firstenergycorp.com/content/dam/customer/billinserts/8285-NJEnvironmentalLabel1116.pdf, accessed 3/31/2018
# Time Range: June 2015 - May 2016


atlantic_fuel_makeup = {'coal': 0.328,
                           'gas': 0.246,
                           'nuclear': 0.325,
                           'oil': 0.002,
                           'clean': 0.00 + 0.003 + 0.00 + 0.00 + 0.01 + 0.031 + 0.03 + 0.023 + 0.002}
# Atlantic City Electric
# https://www.atlanticcityelectric.com/SiteCollectionDocuments/ACE%20Environ%20Disclosure%20Bill%202017.pdf, accessed 3/31/2018
# Time Range:  June 1, 2016 to May 31, 2017


rockland_fuel_makeup = {'coal': 0.263,
                           'gas': 0.274,
                           'nuclear': 0.364,
                           'oil': 0.002,
                           'clean': 0.055 + 0.028 + 0.005 + 0.006 + 0.003}
# Rockland Electric
# https://www.oru.com/_external/orurates/documents/nj/NJElectricityProductLabel.pdf, accessed 3/31/2018
# Time Range:  January through June 2017






###### STATE-SPECIFIC PARAMETERS #########

# NOTE THAT THE ENERGY PARAMETERS MAY BE STATE-SPECIFIC AS WELL


# NJ Stats
# For 2017: https://www.census.gov/data/tables/2017/demo/popest/state-total.html
# Adult population from: https://www.census.gov/data/tables/2017/demo/popest/state-detail.html
# Accessed 04-07-2018

TOTALPOPULATION = 9005644
ADULT_POPULATION = 7026626
UNDER18_POPULATION = TOTALPOPULATION - ADULT_POPULATION

# In tons per year, 2015
# U.S. Energy Information Administration | Energy-Related Carbon Dioxide Emissions by State, 2000-2015
# https://www.eia.gov/environment/emissions/state/analysis/pdf/stateanalysis.pdf Accessed 4/7/2018

ANNUALEMISSIONS = 111.9 * 10**6


########## INPUT DEFAULTS

DEFAULT_ADULTS = 1
DEFAULT_CHILDREN = 0

DEFAULT_GASOLINE_AMT = 70.0
DEFAULT_GASOLINE_TYPE = 'e10'
DEFAULT_GASOLINE_UNIT_CHOICE = ('gallon', 'gallons')

DEFAULT_HEATING_AMT = 164.0
DEFAULT_HEATING_TYPE = 'gas'
DEFAULT_HEATING_UNIT_CHOICE = ('therm', 'therms')

DEFAULT_ELEC_AMT = 900.0
DEFAULT_ELEC_TYPE = 'pseg'
DEFAULT_ELEC_UNIT_CHOICE = ('kWh', 'kWh')
