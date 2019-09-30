from django import forms
from app1.models import student

class studentform(forms.ModelForm):
    class Meta():
        model=student
        fields=('student_name','student_id','date_of_join')
        