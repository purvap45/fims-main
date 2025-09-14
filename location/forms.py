from django import forms
from django.forms import ModelForm
from family.models import State, City, statusChoice

class StateForm(ModelForm):
    class Meta:
        model = State
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state_name'].required = False
        self.fields['status'].required = False
        self.fields['status'].choices = [
            (statusChoice.ACTIVE, 'Active'),
            (statusChoice.INACTIVE, 'Inactive'),
        ]

    def clean(self):
        super().clean()
        # state name
        state_name = self.cleaned_data.get('state_name')
        if not state_name: 
            self.add_error('state_name','State is required.')
        elif State.objects.exclude(status=statusChoice.DELETE).filter(state_name=state_name).exclude(pk=self.instance.pk).exists():
            self.add_error('state_name','State already exists.')

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_name'].required = False
        self.fields['state'].required = False
        self.fields['status'].required = False
        self.fields['state'].queryset = State.objects.filter(status=statusChoice.ACTIVE)
        self.fields['status'].choices = [
            (statusChoice.ACTIVE, 'Active'),
            (statusChoice.INACTIVE, 'Inactive'),
        ]

    def clean(self):
        super().clean()
        # state name
        state = self.cleaned_data.get('state')
        if not state:
            self.add_error('state','State is required to add City.')
        # city name
        city_name = self.cleaned_data.get('city_name')
        if not city_name: 
            self.add_error('city_name','City is required.')
        elif City.objects.exclude(status=statusChoice.DELETE).filter(city_name=city_name).exclude(pk=self.instance.pk).exists():
            self.add_error('city_name','City already exists.')
        