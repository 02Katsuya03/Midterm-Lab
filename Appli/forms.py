from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import School, Profile, LostItem, FoundItem
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class RegistrationUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    middle_name = forms.CharField(max_length=30, required=False, label='Middle Name (Optional)')
    last_name = forms.CharField(max_length=30, label='Last Name')
    email = forms.EmailField(max_length=254, label='Email')
    sex = forms.ChoiceField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], label='Gender')
    phone_number = forms.CharField(max_length=15, label='Phone Number')
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=True, label='School')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'middle_name', 'last_name', 'email', 'sex', 'phone_number', 'school', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'password-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'password-input'})
        }

    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class LoginUserForm(AuthenticationForm):
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=True)
    role = forms.ChoiceField(choices=[('User', 'User')], required=True, widget=forms.HiddenInput())  
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['school'].choices = [(school.id, school.Name) for school in School.objects.all()]
        
        self.fields['role'].initial = 'User'

    def clean_role(self):
        
        role = self.cleaned_data['role']
        return role.capitalize()  
    
class LoginAdminForm(AuthenticationForm):
    school = forms.ChoiceField(choices=[], required=True)
    role = forms.ChoiceField(choices=[('Admin', 'Admin')], required=True, widget=forms.HiddenInput())  
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].choices = [(school.id, school.Name) for school in School.objects.all()]
        self.fields['role'].initial = 'Admin'

    def clean_role(self):
        role = self.cleaned_data['role']
        return role.capitalize()  
    
class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['item_name', 'description', 'category', 'date_lost', 
                  'location_lost', 'contact_information', 'lost_by', 'school', 'photo']
        widgets = {
            'date_lost': forms.DateInput(attrs={
                'type': 'text',  
                'class': 'form-control',  
                'id': 'datePicker',  
            }),
        }

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['item_name', 'description', 'category', 'date_found', 
                  'location_found', 'contact_information', 'found_by', 'school', 'photo']
        widgets = {
            'date_found': forms.DateInput(attrs={
                'type': 'text',  
                'class': 'form-control',  
                'id': 'datePicker',  
            }),
        }