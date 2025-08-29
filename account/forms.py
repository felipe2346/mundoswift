from django import forms

from .models import Shipment, LiveUpdate


class DateInput(forms.DateInput):
	input_type = 'date'


class ShipmentCreateForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'
        exclude = ['date_created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make tracking_number readonly (disabled) only during creation
        if not self.instance.pk:  # Means it's a "create" form
            self.fields['tracking_number'].disabled = True
            self.fields['tracking_number'].required = False  # Avoid validation error

        self.fields['content'].widget = forms.Textarea(attrs={'rows': 1, 'cols': 15})

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class LiveUpdateCreateForm(forms.ModelForm):

    class Meta:
        model = LiveUpdate
        fields = '__all__'
        # exclude = ['created_on', 'shipment']
        exclude = ['created_on', 'shipment', 'latitude','longitude']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['content'].widget = forms.Textarea(attrs={'rows':1, 'cols':15})
        # self.fields['shipping_date'].widget = DateInput()
        # self.fields['delivery_date'].widget = DateInput()

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})