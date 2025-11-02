from django.forms import ModelForm, DateInput, NumberInput
from django import forms

from apps.home.models import Order


class OrderCreateModelForm(ModelForm):
    return_date = forms.DateField(
        required=True,
        label="תאריך החזרה",
        widget=DateInput(
            format='%d/%m/%Y',
            attrs={'class': 'form-control', 'placeholder': 'בחר תאריך', 'type': 'date', }
        ),
        error_messages={'required': 'יש לבחור תאריך החזרה!'}
    )
    class Meta:
        model = Order
        fields = ['name',
                  'location',
                  'phone',
                  'return_date',
                  'pack',
                  'notes']

        widgets = {
            'return_date':  DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'phone':  NumberInput(),
        }


class OrderUpdateModelForm(ModelForm):
    return_date = forms.DateField(
        required=True,
        label="תאריך החזרה",
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'class': 'form-control', 'placeholder': 'בחר תאריך', 'type': 'date'}
        ),
        error_messages={'required': 'יש לבחור תאריך החזרה!'}
    )
    class Meta:
        model = Order
        fields = ['name',
                  'location',
                  'phone',
                  'return_date',
                  'pack',
                  'notes',
                  'done']

        widgets = {
            'return_date':  DateInput(format='%Y-%m-%d', attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }