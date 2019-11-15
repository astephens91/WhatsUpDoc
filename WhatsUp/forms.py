from django import forms
from WhatsUp.models import Ticket

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class AddTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'ticket_status', 
            'assigned_user'
        ]