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

PERIOD_CHOICES = (('month', 'Per Month'), )

ELEC_CHOICES = ( ('pseg', 'PSE&G'), ('rockland', 'Orange Rockland Electric'),
                 ('jcpl', 'Jersey Central Power & Light'), ('atlantic', 'Atlantic City Electric'))

ELEC_UNIT_CHOICES = (('kWh', 'kWh'),)

HEATING_CHOICES = ( ('gas', 'Natural Gas'), ('fuel', 'Fuel Oil'), ('elec', 'Electricity'))

HEATING_UNIT_CHOICES = (('therm', 'therms'), ('gallon', 'gallons'), ('kWh', 'kWh'))

GASOLINE_CHOICES = (('e10', '10% Ethanol'), ('e0', 'Pure Gasoline'), ('diesel', 'Diesel'), ('b20', '20% Biodiesel'))

GASOLINE_UNIT_CHOICES = (('gallon', 'gallons'), )
# adding the

def get_possible_gasoline_units(gasoline_type):
    if gasoline_type in {'e10', 'e0', 'diesel', 'b20'}:
        return (('gallon', 'gallons'),)
    else:
        raise ValueError("Gasoline type " + str(gasoline_type) + " not allowed.")


def get_possible_elec_units(elec_type):
    if elec_type == 'pseg' or elec_type == 'rockland' or elec_type == 'jcpl' or elec_type == 'atlantic':
        return (('kWh', 'kWh'),)
    else:
        raise ValueError("Elec type " + str(elec_type) + " not allowed.")


def get_possible_heating_units(heating_type):
    if heating_type == 'gas':
        return (('therm', 'therms'),)
    elif heating_type == 'fuel':
        return (('gallon', 'gallons'),)
    elif heating_type == 'elec':
        return (('kWh', 'kWh'),)
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
    if gasoline_type == 'e10':
        if gasoline_unit == 'gallon':
            return 17.6/2204.6
    elif gasoline_type == 'e0':
        if gasoline_unit == 'gallon':
            return 19.6/2204.6
    elif gasoline_type == 'diesel':
        if gasoline_unit == 'gallon':
            return 22.4/2204.6
    elif gasoline_type == 'b20':
        if gasoline_unit == 'gallon':
            return 17.9/2204.6

    raise ValueError("Gasoline Unit " + str(gasoline_unit) + " not allowed for gasoline type " + str(gasoline_type))


def get_elec_co2_conversion(elec_type, elec_unit):
    """
    get return unit + metric tons co2 per conversion
    :param elec_type:  one of the ELEC_CHOICES
    :return: elc_unit (the unit of electricity, e.g. therm),
            elec_co2_conversion (metric tons of CO2/unit)
    """
    if elec_unit == 'kWh':
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
        if elec_type == 'pseg':
            fuel_makeup = {'coal': 0.2184,
                           'gas': 0.2247,
                           'nuclear': 0.3953,
                           'oil': 0.0012,
                           'clean': 0.0004 + 0.0198 + 0.0002 + 0.00 + 0.0005 + 0.0299 + 0.0241 + 0.0851 + 0.0004}


        # Jersey Central Power & Light
        # https://www.firstenergycorp.com/content/dam/customer/billinserts/8285-NJEnvironmentalLabel1116.pdf, accessed 3/31/2018
        # Time Range: June 2015 - May 2016
        elif elec_type == 'jcpl':
            fuel_makeup = {'coal': 0.3286,
                           'gas': 0.2476,
                           'nuclear': 0.3688,
                           'oil': 0.0023,
                           'clean': 0.0171 + 0.0003 + 0.0033 + 0.00 + 0.00 + 0.0009 + 0.0057 + 0.0229 + 0.0025}

        # Atlantic City Electric
        # https://www.atlanticcityelectric.com/SiteCollectionDocuments/ACE%20Environ%20Disclosure%20Bill%202017.pdf, accessed 3/31/2018
        # Time Range:  June 1, 2016 to May 31, 2017
        elif elec_type == 'atlantic':
            fuel_makeup = {'coal': 0.328,
                           'gas': 0.246,
                           'nuclear': 0.325,
                           'oil': 0.002,
                           'clean': 0.00 + 0.003 + 0.00 + 0.00 + 0.01 + 0.031 + 0.03 + 0.023 + 0.002}

        # Rockland Electric
        # https://www.oru.com/_external/orurates/documents/nj/NJElectricityProductLabel.pdf, accessed 3/31/2018
        # Time Range:  January through June 2017
        elif elec_type == 'rockland':
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


def get_heating_co2_conversion(heating_type, heating_unit, elec_type=None):
    """
    get return unit + metric tons co2 per conversion
    :param heating_type:  one of the HEATING_CHOICES
    :return: heating_unit (the unit of heating method, e.g. therm),
            heating_co2_conversion (metric tons of CO2/unit)
    """

    # if heating_type not in HEATING_CHOICES:
    #     raise ValueError("Heating type " + str(heating_type) + " is not valid!")

    # Natural Gas CO2/therm: https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references
    # 0.0053 metric tons CO2/therm
    if heating_type == 'gas':
        if heating_unit == 'therm':
            heating_co2_conversion = 0.0053
        else:
            raise ValueError("Heating Unit " + str(heating_unit) + " not allowed for heating type " + str(heating_type))

    # Distillate Fuel Oil (Home Heating Fuel) https://www.eia.gov/environment/emissions/co2_vol_mass.php
    # 10.16 kg CO2/gallon * 0.001 metric tons/kg
    elif heating_type == 'fuel':
        if heating_unit == 'gallon':
            heating_co2_conversion = 10.16 * 0.001
        else:
            raise ValueError("Heating Unit " + str(heating_unit) + " not allowed for heating type " + str(heating_type))


    # Electricity
    # Simply return CO2 content of electricity
    elif heating_type == 'elec':
        if heating_unit == 'kWh':
            heating_co2_conversion = get_elec_co2_conversion(elec_type, heating_unit) # modified CW 4/12/18
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


#################         MODELS         #################


class UserProfile(models.Model):
    # eventually would be cool to load default from other models...

    fee = models.FloatField(default=30., validators=[validate_nonnegative], help_text="Fee, dollars per ton of CO2.")
    rebate_portion = models.FloatField(default=0.7, validators=[validate_0to1], help_text="Portion of total revenue. The rest goes to sustainableinvestment and relief for vulnerable businesses and communities.")
    period = models.CharField(choices=PERIOD_CHOICES, default='month', max_length=5, help_text="Time range for calculation.")


    adults = models.PositiveIntegerField(default=1, validators=[validate_leq20], help_text="Members of household 18 and older.")
    children = models.PositiveIntegerField(default=0, validators=[validate_leq20], help_text="Members of household under 18.")
    CHILD_MULTIPLIER = 0.5

    ##############    GASOLINE    ##############

    # the fundamental unit: gasoline in gallons per month
    # we set the 200 gall/month based on average across zipcodes in NJ: 198 gall/month, see data/zipcode_data_nj.txt
    gasoline_amt = models.FloatField(default=200.0, validators=[validate_nonnegative])
    gasoline_type = models.CharField(choices=GASOLINE_CHOICES, default='e10', max_length=40)
    gasoline_unit = models.CharField(choices=GASOLINE_UNIT_CHOICES, default=get_possible_gasoline_units('e10')[0],
                                    max_length=40)

    ##############    ELECTRICITY    ##############

    # the fundamental unit: electricity in kWh per month

    elec_amt = models.FloatField(default=1.0, validators=[validate_nonnegative])
    elec_type = models.CharField(choices=ELEC_CHOICES, default='pseg', max_length=40, help_text="Your electric utility provider.")
    elec_unit = models.CharField(choices=ELEC_UNIT_CHOICES, default=get_possible_elec_units('pseg')[0],
                                    max_length=40)

    ##############    HEATING    ##############

    # the fundamental unit: therm for gas, gallons for fuel oil, kWh for elec
    heating_amt = models.FloatField(default=1.0, validators=[validate_nonnegative])
    heating_type = models.CharField(choices=HEATING_CHOICES, default='gas', max_length=40)
    heating_unit = models.CharField(choices=HEATING_UNIT_CHOICES, default=get_possible_heating_units('gas')[0],
                                    max_length=40)



    def calculate_net(self):
        # TODO: update. remember should be monthly. should calculate with child as well
        # TODO: update with the correct units


        # In tons per year, 2015
        # U.S. Energy Information Administration | Energy-Related Carbon Dioxide Emissions by State, 2000-2015
        # https://www.eia.gov/environment/emissions/state/analysis/pdf/stateanalysis.pdf Accessed 4/7/2018
        TOTALEMISSIONS = 111.9 * 10**6
        if self.period == 'month':
            TOTALEMISSIONS /= 12.0
        elif self.period == 'year':
            pass
        else:
            raise ValueError("Period " + str(self.period) + " not allowed.")

        TOTALREVENUE = TOTALEMISSIONS * self.fee

        # For 2017: https://www.census.gov/data/tables/2017/demo/popest/state-total.html
        # Adult population from: https://www.census.gov/data/tables/2017/demo/popest/state-detail.html
        # Accessed 04-07-2018
        TOTALPOPULATION = 9005644
        ADULT_POPULATION = 7026626
        UNDER18_POPULATION = TOTALPOPULATION - ADULT_POPULATION



        REVENUEPERADULT = TOTALREVENUE * 1.0 / (UNDER18_POPULATION * self.CHILD_MULTIPLIER + ADULT_POPULATION)

        self.DIVIDENDPERADULT =  REVENUEPERADULT * self.rebate_portion
        self.benefit = (self.CHILD_MULTIPLIER * self.children + self.adults) * self.DIVIDENDPERADULT


        self.gasoline_co2 = get_gasoline_co2(str(self.gasoline_type), self.gasoline_amt, self.gasoline_unit)

        self.gasoline_cost = self.fee * self.gasoline_co2

        self.elec_co2 = get_elec_co2(self.elec_type, self.elec_amt, self.elec_unit)

        self.elec_cost = self.fee * self.elec_co2

        self.heating_co2 = get_heating_co2(self.heating_type, self.heating_amt, self.heating_unit)

        self.heating_cost = self.fee * self.heating_co2


        self.total_cost = self.gasoline_cost + self.elec_cost + self.heating_cost

        self.net = self.benefit - self.total_cost



