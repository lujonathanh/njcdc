from django import forms
from .models import UserProfile, get_possible_heating_units


class InputForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('adults', 'children', 
                  'gasoline_type', 'gasoline_amt',
                  'heating_type', 'heating_amt', 'heating_unit', 
                  'elec_type', 'elec_amt')

    def clean_heating_unit(self):
        heating_unit = self.cleaned_data["heating_unit"]
        heating_type = self.cleaned_data["heating_type"]
        if not (heating_unit in get_possible_heating_units(heating_type) or heating_unit in [x[0] for x in get_possible_heating_units(heating_type)]) :
            raise forms.ValidationError(" The unit " + str(heating_unit) + " cannot be used with the heating type " + str(heating_type))

        return heating_unit


# Below were from initial attempts to have the forms update dynamically using AJAX.
# We've commented them out to make sure they're not accidentally used.


# class UpdatingInputForm(forms.ModelForm):
#
#     class Meta:
#         model = UserProfile
#         fields = ('adults', 'children', 'gasoline_type', 'gasoline_amt', 'gasoline_unit',
#                   'heating_type', 'heating_amt', 'heating_unit',
#                   'elec_type', 'elec_amt',  'elec_unit')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['gasoline_unit'].queryset = UserProfile.objects.none()
#
#
# class BasicUserForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('adults', 'children')
#
#
# class GasolineForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('gasoline_type', 'gasoline_amt', 'gasoline_unit')
#
#
# class HeatingForm(forms.ModelForm):
#
#     class Meta:
#         model = UserProfile
#         fields = ('heating_type', 'heating_amt', 'heating_unit')
#
# class ElectricityForm(forms.ModelForm):
#
#     class Meta:
#         model = UserProfile
#         fields = ('elec_type', 'elec_amt', 'elec_unit')