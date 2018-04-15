from django import forms
from .models import UserProfile


class InputForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('adults', 'children', 'gasoline_type', 'gasoline_amt', 'gasoline_unit',
                  'heating_type', 'heating_amt', 'heating_unit',
                  'elec_type', 'elec_amt',  'elec_unit')