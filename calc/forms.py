from django import forms
from .models import UserProfile


class InputForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('adults', 'children', 
                  'gasoline_type', 'gasoline_amt', 'gasoline_unit', 'gasoline_input',
                  'heating_type', 'heating_amt', 'heating_unit', 'heating_input',
                  'elec_type', 'elec_amt', 'elec_unit', 'elec_input',)


class UpdatingInputForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('adults', 'children', 'gasoline_type', 'gasoline_amt', 'gasoline_unit',
                  'heating_type', 'heating_amt', 'heating_unit',
                  'elec_type', 'elec_amt',  'elec_unit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gasoline_unit'].queryset = UserProfile.objects.none()


class BasicUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('adults', 'children')


class GasolineForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gasoline_type', 'gasoline_amt', 'gasoline_unit')


class HeatingForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('heating_type', 'heating_amt', 'heating_unit')

class ElectricityForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('elec_type', 'elec_amt', 'elec_unit')