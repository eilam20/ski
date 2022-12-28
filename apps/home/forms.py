from django.forms import ModelForm, DateInput

from apps.home.models import Order


class OrderCreateModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name',
                  'place',
                  'phone',
                  'return_date',
                  'pack',
                  'coat',
                  'pants',
                  'notes']

        widgets = {
            'return_date':  DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }