from django.forms import ModelForm, DateInput, NumberInput

from apps.home.models import Order


class OrderCreateModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name',
                  'location',
                  'phone',
                  'return_date',
                  'pack',
                  'coat',
                  'pants',
                  'notes']

        widgets = {
            'return_date':  DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'phone':  NumberInput(),
        }


class OrderUpdateModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name',
                  'location',
                  'phone',
                  'return_date',
                  'pack',
                  'coat',
                  'pants',
                  'notes',
                  'done']

        widgets = {
            'return_date':  DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }