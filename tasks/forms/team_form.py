"""Team Related Forms for the app."""
from django import forms
from tasks.models import Team


class CreateTeamForm(forms.ModelForm):
    class Meta:
        """Form options."""

        model = Team
        fields = ['name']


class JoinTeamForm(forms.Form):
    invitation_code = forms.CharField(label='Invitation Code')


class AddUserToTeamForm(forms.Form):
    """Form for adding User to a team"""
    username = forms.CharField(label='Username')
