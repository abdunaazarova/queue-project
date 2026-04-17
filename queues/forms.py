from django import forms
from .models import Queue, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'location', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'input-field', 'placeholder': 'e.g. AIIMS Delhi', 'autocomplete': 'off'}
        )
        self.fields['category'].widget.attrs.update({'class': 'input-field'})
        self.fields['location'].widget.attrs.update(
            {'class': 'input-field', 'placeholder': 'e.g. Ansari Nagar, New Delhi - 110029', 'autocomplete': 'off'}
        )
        self.fields['description'].widget.attrs.update(
            {'class': 'input-field', 'placeholder': 'Short service details for users...', 'rows': 4}
        )


class QueueConfigForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['service', 'estimated_wait_minutes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].widget.attrs.update({'class': 'input-field'})
        self.fields['estimated_wait_minutes'].widget.attrs.update(
            {'class': 'input-field', 'placeholder': 'e.g. 25', 'min': 1}
        )
