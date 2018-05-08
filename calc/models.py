from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.

#################         VALIDATORS          #################

def validate_nonnegative(value):
    if value < 0:
        raise ValidationError(_('%(value)s is a negative number'),
            params={'value': value},
        )

def validate_0to1(value):
    if value < 0:
        raise ValidationError(_('%(value)s is a negative number'),
                    params={'value': value},
                )
    if value > 1:
        raise ValidationError(_('%(value)s is a negative number'),
                    params={'value': value},
                )

def validate_leq20(value):
    if value > 20:
        raise ValidationError(_('%(value)s is greater than 20'),
                              params={'value': value},
                              )

# per ton CO2
FEE = 30

# amount going back to households
REBATE_PORTION = 0.7

# child multiplier
CHILD_MULTIPLIER = 0.5


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


PERIOD_CHOICES = (('month', 'Per Month'), )

ELEC_CHOICES = ( ('pseg', 'PSE&G'), ('rockland', 'Orange Rockland Electric'),
                 ('jcpl', 'Jersey Central Power & Light'), ('atlantic', 'Atlantic City Electric'))

ELEC_UNIT_CHOICES = (('kWh', 'kWh'),)

DEFAULT_ELEC_UNIT_CHOICE = ('kWh', 'kWh')

HEATING_CHOICES = ( ('gas', 'Natural Gas'), ('fuel', 'Fuel Oil'))

HEATING_UNIT_CHOICES = (('therm', 'therms'), ('gallon', 'gallons'))

GASOLINE_CHOICES = (('e10', 'Regular Gasoline'), ('e0', 'Pure Gasoline'), ('diesel', 'Diesel'), ('b20', '20% Biodiesel'))

GASOLINE_UNIT_CHOICES = (('gallon', 'gallons'), )

DEFAULT_GASOLINE_UNIT_CHOICE = ('gallon', 'gallons')


def get_possible_gasoline_units(gasoline_type):
    if gasoline_type in {'e10', 'e0', 'diesel', 'b20'} or gasoline_type in GASOLINE_CHOICES:
        return (('gallon', 'gallons'),)
    else:
        raise ValueError("Gasoline type " + str(gasoline_type) + " not allowed.")


def get_possible_elec_units(elec_type):
    if elec_type == 'pseg' or elec_type == 'rockland' or elec_type == 'jcpl' or elec_type == 'atlantic' or elec_type in ELEC_CHOICES:
        return (('kWh', 'kWh'),)
    else:
        raise ValueError("Elec type " + str(elec_type) + " not allowed.")


def get_possible_heating_units(heating_type):
    if heating_type == 'gas' or heating_type == ('gas', 'Natural Gas')\
        or heating_type == "('gas', 'Natural Gas')":
        return (('therm', 'therms'),)
    elif heating_type == 'fuel' or heating_type == ('fuel', 'Fuel Oil')\
        or heating_type == "('fuel', 'Fuel Oil')":
        return (('gallon', 'gallons'),)
    else:
        raise ValueError("Heating type " + str(heating_type) + " not allowed.")


def get_gasoline_co2_conversion(gasoline_type, gasoline_unit):
    """
    get return unit + metric tons co2 per conversion
    :param gasoline_type:  one of the gasoline_CHOICES
    :return: gasoline_unit (the unit of gasoline method, e.g. therm),
            gasoline_co2_conversion (metric tons of CO2/unit)
    """
    #
    # if gasoline_type not in GASOLINE_CHOICES:
    #     raise ValueError("Gasoline type " + str(gasoline_type) + " is not valid!")

    # gallon of gas to metric tons of CO2
    # https://www.eia.gov/tools/faqs/faq.php?id=307&t=11
    # 'e10': 17.6/2204.6, 'e0': 19.6/2204.6, 'diesel': 22.4/2204.6, 'biodiesel': 17.9/2204.6
    if gasoline_type == 'e10' or gasoline_type == ('e10', 'Regular Gasoline')\
        or gasoline_type == "('e10', 'Regular Gasoline')":
        if gasoline_unit == 'gallon' or gasoline_unit == ('gallon', 'gallons')\
         or gasoline_unit == "('gallon', 'gallons')":
            return 17.6/2204.6
    elif gasoline_type == 'e0' or gasoline_type == ('e0', 'Pure Gasoline')\
        or gasoline_type == "('e0', 'Pure Gasoline')":
        if gasoline_unit == 'gallon' or gasoline_unit == ('gallon', 'gallons')\
         or gasoline_unit == "('gallon', 'gallons')":
            return 19.6/2204.6
    elif gasoline_type == 'diesel' or gasoline_type == ('diesel', 'Diesel')\
        or gasoline_type == "('diesel', 'Diesel')":
        if gasoline_unit == 'gallon' or gasoline_unit == ('gallon', 'gallons')\
         or gasoline_unit == "('gallon', 'gallons')":
            return 22.4/2204.6
    elif gasoline_type == 'b20' or gasoline_type == ('b20', '20% Biodiesel')\
        or gasoline_type == "('b20', '20% Biodiesel')":
        if gasoline_unit == 'gallon' or gasoline_unit == ('gallon', 'gallons')\
         or gasoline_unit == "('gallon', 'gallons')":
            return 17.9/2204.6

    raise ValueError("Gasoline Unit " + str(gasoline_unit) + " not allowed for gasoline type " + str(gasoline_type))


def get_elec_co2_conversion(elec_type, elec_unit):
    """
    get return unit + metric tons co2 per conversion
    :param elec_type:  one of the ELEC_CHOICES
    :return: elc_unit (the unit of electricity, e.g. therm),
            elec_co2_conversion (metric tons of CO2/unit)
    """
    if elec_unit == 'kWh' or elec_unit == ('kWh', 'kWh') or elec_unit == "('kWh', 'kWh')":
        # tons of CO2 per elec_unit
        fuel_co2_conversions = {
            'coal': 10045./3412. * 0.0034095 * 26.05 * 11./3 * 0.001,
            # kwH of Coal per kwH generated is the average heat rate, 10045, divided by 3412
            # https://www.eia.gov/electricity/annual/html/epa_08_02.html, accessed 4/1/2018
            # 0.0034095 MMBtu/kWh https://www.unitjuggler.com/convert-energy-from-kWh-to-MMBtu.html
            # 26.05 kg C/mmbtu Coal https://www.epa.gov/ghgemissions/inventory-us-greenhouse-gas-emissions-and-sinks-1990-2015, Annex 2, Table A40. Year 2015
            # 11/3 kg CO2/kg C
            # 0.001 ton/kg

            'oil': 13535./3412. * 0.0034095 * 20.31 * 11./3 * 0.001,

            # kwH of Oil per kwH generated is the average heat rate, 13535, divided by 3412, which is 1  kwH of electricity
            # The heat rate ranges from 9860 to 13535 https://www.eia.gov/electricity/annual/html/epa_08_02.html, accessed 4/1/2018
            # 0.0034095 MMBtu/kWh https://www.unitjuggler.com/convert-energy-from-kWh-to-MMBtu.html
            # 20.31 C/mmbtu Oil https://www.epa.gov/ghgemissions/inventory-us-greenhouse-gas-emissions-and-sinks-1990-2015, Annex 2, Table A40. Year 2015
            # 11/3 kg CO2/kg C
            # 0.001 ton/kg

            'gas': 11214./3412. * 0.0034095 * 14.46 * 11./3 * 0.001,

            # kwH of Gas per kwH generated is the average heat rate, 11214, divided by 3412
            # The heat rate ranges from 7652 to 11214 https://www.eia.gov/electricity/annual/html/epa_08_02.html, accessed 4/1/2018
            # 0.0034095 MMBtu/kWh https://www.unitjuggler.com/convert-energy-from-kWh-to-MMBtu.html
            # 14.46 C/mmbtu Gas https://www.epa.gov/ghgemissions/inventory-us-greenhouse-gas-emissions-and-sinks-1990-2015, Annex 2, Table A40. Year 2015
            # 11/3 kg CO2/kg C
            # 0.001 ton/kg
            'nuclear': 0,
            'clean': 0
        }

        # PSE&G
        # https://www.pseg.com/info/environment/envirolabel.jsp, accessed 3/31/2018
        # Time Range: June 1, 2016 - May 31, 2017
        if elec_type == 'pseg' or elec_type == ('pseg', 'PSE&G') or elec_type == "('pseg', 'PSE&G')":
            fuel_makeup = {'coal': 0.2184,
                           'gas': 0.2247,
                           'nuclear': 0.3953,
                           'oil': 0.0012,
                           'clean': 0.0004 + 0.0198 + 0.0002 + 0.00 + 0.0005 + 0.0299 + 0.0241 + 0.0851 + 0.0004}


        # Jersey Central Power & Light
        # https://www.firstenergycorp.com/content/dam/customer/billinserts/8285-NJEnvironmentalLabel1116.pdf, accessed 3/31/2018
        # Time Range: June 2015 - May 2016
        elif elec_type == 'jcpl' or elec_type == ('jcpl', 'Jersey Central Power & Light') or elec_type == "('jcpl', 'Jersey Central Power & Light')":
            fuel_makeup = {'coal': 0.3286,
                           'gas': 0.2476,
                           'nuclear': 0.3688,
                           'oil': 0.0023,
                           'clean': 0.0171 + 0.0003 + 0.0033 + 0.00 + 0.00 + 0.0009 + 0.0057 + 0.0229 + 0.0025}

        # Atlantic City Electric
        # https://www.atlanticcityelectric.com/SiteCollectionDocuments/ACE%20Environ%20Disclosure%20Bill%202017.pdf, accessed 3/31/2018
        # Time Range:  June 1, 2016 to May 31, 2017
        elif elec_type == 'atlantic' or elec_type == ('atlantic', 'Atlantic City Electric') or elec_type == "('atlantic', 'Atlantic City Electric')":
            fuel_makeup = {'coal': 0.328,
                           'gas': 0.246,
                           'nuclear': 0.325,
                           'oil': 0.002,
                           'clean': 0.00 + 0.003 + 0.00 + 0.00 + 0.01 + 0.031 + 0.03 + 0.023 + 0.002}

        # Rockland Electric
        # https://www.oru.com/_external/orurates/documents/nj/NJElectricityProductLabel.pdf, accessed 3/31/2018
        # Time Range:  January through June 2017
        elif elec_type == 'rockland' or elec_type == ('rockland', 'Orange Rockland Electric') or elec_type == "('rockland', 'Orange Rockland Electric')":
            fuel_makeup = {'coal': 0.263,
                           'gas': 0.274,
                           'nuclear': 0.364,
                           'oil': 0.002,
                           'clean': 0.055 + 0.028 + 0.005 + 0.006 + 0.003}

        else:
            raise ValueError("Electric Type " + str(elec_type) + " not in electricity choices")

        if sum(fuel_makeup.values()) != 1: # check that we entered a valid amount
            raise ValueError("Fuel Makeup for %s is wrong in database-- doesn't sum to 1." % elec_type)

        if set(fuel_makeup.keys()) != set(fuel_co2_conversions.keys()): # check we entered the right fuels
            raise ValueError("Provided makeup of fuels")

    else:
        raise ValueError("Elec Unit " + str(elec_unit) + " not allowed for elec type " + str(elec_type))



    elec_co2_conversion = 0
    for fuel in fuel_co2_conversions.keys():
        elec_co2_conversion += fuel_co2_conversions[fuel] * fuel_makeup[fuel]

    return elec_co2_conversion


def get_heating_co2_conversion(heating_type, heating_unit):
    """
    get return unit + metric tons co2 per conversion
    :param heating_type:  one of the HEATING_CHOICES
    :return: heating_unit (the unit of heating method, e.g. therm),
            heating_co2_conversion (metric tons of CO2/unit)
    """

    # Natural Gas CO2/therm: https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references
    # 0.0053 metric tons CO2/therm
    if heating_type == 'gas' or heating_type == ('gas', 'Natural Gas')\
        or heating_type == "('gas', 'Natural Gas')":
        if heating_unit == 'therm' or heating_unit == ('therm', 'therms')\
            or heating_unit == "('therm', 'therms')":
            heating_co2_conversion = 0.0053
        else:
            raise ValueError("Heating Unit " + str(heating_unit) + " not allowed for heating type " + str(heating_type))

    # Distillate Fuel Oil (Home Heating Fuel) https://www.eia.gov/environment/emissions/co2_vol_mass.php
    # 10.16 kg CO2/gallon * 0.001 metric tons/kg
    elif heating_type == 'fuel' or heating_type == ('fuel', 'Fuel Oil')\
        or heating_type == "('fuel', 'Fuel Oil')":
        if heating_unit == 'gallon' or heating_unit == ('gallon', 'gallons')\
            or heating_unit == "('gallon', 'gallons')":
            heating_co2_conversion = 10.16 * 0.001
        else:
            raise ValueError("Heating Unit " + str(heating_unit) + " not allowed for heating type " + str(heating_type))
    else:
        raise ValueError("Heating type " + str(heating_type) + " not in heating choices")

    return heating_co2_conversion

def get_gasoline_co2(gasoline_type, gasoline_amt, gasoline_unit):
    """
    Return tons CO2 of this.
    """
    gasoline_co2_conversion = get_gasoline_co2_conversion(gasoline_type, gasoline_unit)
    return gasoline_amt * gasoline_co2_conversion

def get_elec_co2(elec_type, elec_amt, elec_unit):
    """
    Return tons CO2 of this.
    """
    elec_co2_conversion = get_elec_co2_conversion(elec_type, elec_unit)
    return elec_amt * elec_co2_conversion

def get_heating_co2(heating_type, heating_amt, heating_unit):
    """
    Return tons CO2 of this.
    """
    heating_co2_conversion = get_heating_co2_conversion(heating_type, heating_unit)
    return heating_amt * heating_co2_conversion


def get_benefit_per_adult(emissions, fee, rebate_portion, adult_population, child_population, child_multiplier):
    """
    :param emissions: Total CO2 Emissions (tons)
    :param fee: Fee per ton CO2 ($)
    :param rebate_portion: % of total revenue to be returned to households
    :param adult_population: # adults in state
    :param child_population: # children in state
    :param child_multiplier: portion of adult revenue a child should get
    :return: benefit_per_adult
    """
    if (emissions < 0):
        raise ValueError("Can't have negative emissions amount: " + str(emissions))
    if (fee < 0):
        raise ValueError("Can't have negative fee amount: " + str(fee))
    if (rebate_portion < 0 or rebate_portion > 1):
        raise ValueError("Rebate amount " + str(rebate_portion) + " Must be between 0 and 1")
    if (adult_population < 0):
        raise ValueError("Can't have negative adults: " + str(adult_population))
    if (child_population < 0):
        raise ValueError("Can't have negative children: " + str(child_population))
    if (child_multiplier < 0 or child_multiplier > 1):
        raise ValueError("Child multiplier " + str(child_multiplier) + " Must be between 0 and 1")

    total_revenue = emissions * fee
    total_rebate = total_revenue * rebate_portion
    total_adults = adult_population + child_population * child_multiplier

    benefit_per_adult = total_rebate * 1.0 / total_adults

    return benefit_per_adult



def get_benefit_for_household(emissions, fee, rebate_portion, adult_population, child_population, child_multiplier, household_adults,
                              household_children):
    """
    :param emissions: Total CO2 Emissions (tons)
    :param fee: Fee per ton CO2 ($)
    :param rebate_portion: % of total revenue to be returned to households
    :param adult_population: # adults in state
    :param child_population: # children in state
    :param child_multiplier: portion of adult revenue a child should get
    :param household_adults: # in household
    :param household_children: # in household
    :return: benefit_for_household, benefit_per_adult
    """
    if (child_multiplier < 0 or child_multiplier > 1):
        raise ValueError("Child multiplier " + str(child_multiplier) + " Must be between 0 and 1")
    if (household_adults < 0):
        raise ValueError("Can't have negative adults: " + str(household_adults))
    if (household_children < 0):
        raise ValueError("Can't have negative children: " + str(household_children))

    benefit_per_adult = get_benefit_per_adult(emissions=emissions, fee=fee, rebate_portion=rebate_portion,
                                              adult_population=adult_population, child_population=child_population,
                                              child_multiplier=child_multiplier)

    total_household_adults = household_adults + child_multiplier * household_children

    benefit_for_household = benefit_per_adult * total_household_adults

    return benefit_for_household, benefit_per_adult



#################         MODELS         #################


class UserProfile(models.Model):
    # eventually would be cool to load default from other models...

    fee = models.FloatField(default=FEE, validators=[validate_nonnegative], help_text="Fee, dollars per ton of CO2.")
    rebate_portion = models.FloatField(default=REBATE_PORTION, validators=[validate_0to1], help_text="Portion of total revenue. The rest goes to sustainableinvestment and relief for vulnerable businesses and communities.")
    period = models.CharField(choices=PERIOD_CHOICES, default='month', max_length=5, help_text="Time range for calculation.")


    adults = models.PositiveIntegerField(default=1, validators=[validate_leq20], help_text="Members of household 18 and older.")
    children = models.PositiveIntegerField(default=0, validators=[validate_leq20], help_text="Members of household under 18.")

    ##############    GASOLINE    ##############

    # the fundamental unit: gasoline in gallons per month
    # we set the 200 gall/month based on average across zipcodes in NJ: 198 gall/month, see data/zipcode_data_nj.txt
    gasoline_amt = models.FloatField(default=70.0, validators=[validate_nonnegative])
    gasoline_type = models.CharField(choices=GASOLINE_CHOICES, default='e10', max_length=40)
    gasoline_unit = models.CharField(choices=GASOLINE_UNIT_CHOICES, default=DEFAULT_GASOLINE_UNIT_CHOICE,
                                    max_length=40)

    ##############    HEATING    ##############

    # the fundamental unit: therm for gas, gallons for fuel oil, kWh for elec
    heating_amt = models.FloatField(default=164.0, validators=[validate_nonnegative])
    heating_type = models.CharField(choices=HEATING_CHOICES, default='gas', max_length=40)
    heating_unit = models.CharField(choices=HEATING_UNIT_CHOICES, default=get_possible_heating_units('gas')[0],
                                    max_length=40)

    ##############    ELECTRICITY    ##############

    # the fundamental unit: electricity in kWh per month

    elec_amt = models.FloatField(default=900.0, validators=[validate_nonnegative])
    elec_type = models.CharField(choices=ELEC_CHOICES, default='pseg', max_length=40, help_text="Your electric utility provider.")
    elec_unit = models.CharField(choices=ELEC_UNIT_CHOICES, default=DEFAULT_ELEC_UNIT_CHOICE,
                                    max_length=40)



    def calculate_net(self):
        # TODO: update. remember should be monthly. should calculate with child as well
        # TODO: update with the correct units


        if self.period == 'month':
            EMISSIONSPERPERIOD = ANNUALEMISSIONS / 12.0
        elif self.period == 'year':
            EMISSIONSPERPERIOD = ANNUALEMISSIONS
        else:
            raise ValueError("Period " + str(self.period) + " not allowed.")

        self.benefit, BENEFITPERADULT = get_benefit_for_household(emissions=EMISSIONSPERPERIOD,
                                                                   fee=self.fee,
                                                                   rebate_portion=self.rebate_portion,
                                                                   adult_population=ADULT_POPULATION,
                                                                   child_population=UNDER18_POPULATION,
                                                                   child_multiplier=CHILD_MULTIPLIER,
                                                                   household_adults=self.adults,
                                                                   household_children=self.children)

        self.benefit = int(round(self.benefit))

        self.gasoline_co2 = get_gasoline_co2(str(self.gasoline_type), self.gasoline_amt, self.gasoline_unit)

        self.gasoline_cost = int(round(self.fee * self.gasoline_co2))

        self.elec_co2 = get_elec_co2(self.elec_type, self.elec_amt, self.elec_unit)

        self.elec_cost = int(round(self.fee * self.elec_co2))

        self.heating_co2 = get_heating_co2(self.heating_type, self.heating_amt, self.heating_unit)

        self.heating_cost = int(round(self.fee * self.heating_co2))


        self.total_cost = int(round(self.gasoline_cost + self.elec_cost + self.heating_cost))
        self.total_cost_minus = -1*self.total_cost

        self.net = int(self.benefit - self.total_cost)

