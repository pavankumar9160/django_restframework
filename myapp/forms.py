
from django import forms

from .models import *


class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields=["first_name",'last_name','email']