from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from .parameters import *


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
            return e10_ton_co2_per_gallon
    elif gasoline_type == 'e0' or gasoline_type == ('e0', 'Pure Gasoline')\
        or gasoline_type == "('e0', 'Pure Gasoline')":
        if gasoline_unit == 'gallon' or gasoline_unit == ('gallon', 'gallons')\
         or gasoline_unit == "('gallon', 'gallons')":
            return e0_ton_co2_per_gallon
    elif gasoline_type == 'diesel' or gasoline_type == ('diesel', 'Diesel')\
        or gasoline_type == "('diesel', 'Diesel')":
        if gasoline_unit == 'gallon' or gasoline_unit == ('gallon', 'gallons')\
         or gasoline_unit == "('gallon', 'gallons')":
            return diesel_ton_co2_per_gallon
    elif gasoline_type == 'b20' or gasoline_type == ('b20', '20% Biodiesel')\
        or gasoline_type == "('b20', '20% Biodiesel')":
        if gasoline_unit == 'gallon' or gasoline_unit == ('gallon', 'gallons')\
         or gasoline_unit == "('gallon', 'gallons')":
            return b20_ton_co2_per_gallon

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
            'coal': elec_coal_ton_co2_per_kwh,
            'oil': elec_oil_ton_co2_per_kwh,
            'gas': elec_natural_gas_ton_co2_per_kwh,
            'nuclear': elec_nuclear_ton_co2_per_kwh,
            'clean': elec_clean_ton_co2_per_kwh,
        }


        if elec_type == 'pseg' or elec_type == ('pseg', 'PSE&G') or elec_type == "('pseg', 'PSE&G')":
            fuel_makeup = pseg_fuel_makeup
        elif elec_type == 'jcpl' or elec_type == ('jcpl', 'Jersey Central Power & Light') or elec_type == "('jcpl', 'Jersey Central Power & Light')":
            fuel_makeup = jcpl_fuel_makeup

        elif elec_type == 'atlantic' or elec_type == ('atlantic', 'Atlantic City Electric') or elec_type == "('atlantic', 'Atlantic City Electric')":
            fuel_makeup = atlantic_fuel_makeup

        elif elec_type == 'rockland' or elec_type == ('rockland', 'Orange Rockland Electric') or elec_type == "('rockland', 'Orange Rockland Electric')":
            fuel_makeup = rockland_fuel_makeup

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

    if heating_type == 'gas' or heating_type == ('gas', 'Natural Gas')\
        or heating_type == "('gas', 'Natural Gas')":
        if heating_unit == 'therm' or heating_unit == ('therm', 'therms')\
            or heating_unit == "('therm', 'therms')":
            heating_co2_conversion = natural_gas_ton_co2_per_therm
        else:
            raise ValueError("Heating Unit " + str(heating_unit) + " not allowed for heating type " + str(heating_type))

    elif heating_type == 'fuel' or heating_type == ('fuel', 'Fuel Oil')\
        or heating_type == "('fuel', 'Fuel Oil')":
        if heating_unit == 'gallon' or heating_unit == ('gallon', 'gallons')\
            or heating_unit == "('gallon', 'gallons')":
            heating_co2_conversion = fuel_oil_ton_co2_per_gallon
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


    adults = models.PositiveIntegerField(default=DEFAULT_ADULTS, validators=[validate_leq20], help_text="Members of household 18 and older.")
    children = models.PositiveIntegerField(default=DEFAULT_CHILDREN, validators=[validate_leq20], help_text="Members of household under 18.")

    ##############    GASOLINE    ##############

    # the fundamental unit: gasoline in gallons per month
    # we set the 200 gall/month based on average across zipcodes in NJ: 198 gall/month, see data/zipcode_data_nj.txt
    gasoline_amt = models.FloatField(default=DEFAULT_GASOLINE_AMT, validators=[validate_nonnegative])
    gasoline_type = models.CharField(choices=GASOLINE_CHOICES, default=DEFAULT_GASOLINE_TYPE, max_length=40)
    gasoline_unit = models.CharField(choices=GASOLINE_UNIT_CHOICES, default=DEFAULT_GASOLINE_UNIT_CHOICE,
                                    max_length=40)

    ##############    HEATING    ##############

    # the fundamental unit: therm for gas, gallons for fuel oil, kWh for elec
    heating_amt = models.FloatField(default=DEFAULT_HEATING_AMT, validators=[validate_nonnegative])
    heating_type = models.CharField(choices=HEATING_CHOICES, default=DEFAULT_HEATING_TYPE, max_length=40)
    heating_unit = models.CharField(choices=HEATING_UNIT_CHOICES, default=DEFAULT_HEATING_UNIT_CHOICE,
                                    max_length=40)

    ##############    ELECTRICITY    ##############

    # the fundamental unit: electricity in kWh per month

    elec_amt = models.FloatField(default=DEFAULT_ELEC_AMT, validators=[validate_nonnegative])
    elec_type = models.CharField(choices=ELEC_CHOICES, default=DEFAULT_ELEC_TYPE, max_length=40, help_text="Your electric utility provider.")
    elec_unit = models.CharField(choices=ELEC_UNIT_CHOICES, default=DEFAULT_ELEC_UNIT_CHOICE,
                                    max_length=40)



    def calculate_net(self):

        if self.period == 'month':
            EMISSIONSPERPERIOD = ANNUALEMISSIONS / 12.0
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

