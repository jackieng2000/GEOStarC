# events/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import EventAdmin, EventUser

User = get_user_model()

# events/forms.py - Add this at the top with other imports
from .models import Event, EventAdmin, EventUser

# Add this form class to your forms.py
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['EventName', 'Type', 'Distance', 'Elevation', 'Description']
        widgets = {
            'EventName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event name'}),
            'Type': forms.Select(attrs={'class': 'form-control'}),
            'Distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Distance in km'}),
            'Elevation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Elevation in meters'}),
            'Description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Event description'}),
        }
        labels = {
            'EventName': 'Event Name',
            'Type': 'Event Type', 
            'Distance': 'Distance (km)',
            'Elevation': 'Elevation (m)',
            'Description': 'Description',
        }

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = EventAdmin
        fields = ['UserId', 'Role']
    
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
        # Filter users who are not already admins
        if self.event:
            existing_admins = EventAdmin.objects.filter(EventId=self.event).values_list('UserId', flat=True)
            existing_admins = list(existing_admins) + [self.event.AdminUser.id]
            self.fields['UserId'].queryset = User.objects.exclude(id__in=existing_admins)
        
        self.fields['UserId'].label = "Select User"
        self.fields['Role'].required = False
        
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class EventUserForm(forms.ModelForm):
    Completed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = EventUser
        fields = ['UserId', 'StartTimestamp', 'EndTimestamp', 'DistanceCompleted', 'Notes']
        widgets = {
            'StartTimestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'EndTimestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'Notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
        # Filter users who are not already enrolled
        if self.event and not self.instance.pk:
            existing_users = EventUser.objects.filter(EventId=self.event).values_list('UserId', flat=True)
            self.fields['UserId'].queryset = User.objects.exclude(id__in=existing_users)
        else:
            self.fields['UserId'].queryset = User.objects.all()
        
        self.fields['UserId'].label = "Select User"
        
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if field_name not in ['Completed']:
                field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('StartTimestamp')
        end_time = cleaned_data.get('EndTimestamp')
        
        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError("Start time cannot be after end time.")
        
        return cleaned_data