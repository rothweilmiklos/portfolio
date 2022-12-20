from django import forms

USERNAME_FIELD_ATTRIBUTES = {'placeholder': 'User name', 'class': 'form-control'}
PASSWORD_FIELD_ATTRIBUTES = {'placeholder': 'Password', 'class': 'form-control'}
PASSWORD2_FIELD_ATTRIBUTES = {'placeholder': 'Confirm Password', 'class': 'form-control'}
CASTE_FIELD_ATTRIBUTES = {'class': 'form-control'}
CASTE_CHOICES = [('WIZARD', 'Wizard'), ('ELF', 'Elf'), ('HUMAN', 'Human'), ('DWARF', 'Dwarf')]

EQUIPMENT_NAME_FIELD_ATTRIBUTES = {'placeholder': 'Enter equipment name...', 'class': 'form-control'}
PRICE_FIELD_ATTRIBUTES = {'placeholder': 'Enter equipment price...', 'class': 'form-control'}
DESCRIPTION_FIELD_ATTRIBUTES = {'rows': '5', 'placeholder': 'Enter equipment description...', 'class': 'form-control'}


class EntityRegistrationForm(forms.Form):
    username = forms.CharField(max_length=128, min_length=3, widget=forms.TextInput(attrs=USERNAME_FIELD_ATTRIBUTES))
    password = forms.CharField(max_length=128, min_length=3,
                               widget=forms.PasswordInput(attrs=PASSWORD_FIELD_ATTRIBUTES))
    password2 = forms.CharField(max_length=128, min_length=3,
                                widget=forms.PasswordInput(attrs=PASSWORD2_FIELD_ATTRIBUTES))
    caste = forms.CharField(widget=forms.Select(choices=CASTE_CHOICES, attrs=CASTE_FIELD_ATTRIBUTES))


class EntityLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=USERNAME_FIELD_ATTRIBUTES))
    password = forms.CharField(widget=forms.PasswordInput(attrs=PASSWORD_FIELD_ATTRIBUTES))


class AddEquipmentForm(forms.Form):
    name = forms.CharField(max_length=128, min_length=3, widget=forms.TextInput(attrs=EQUIPMENT_NAME_FIELD_ATTRIBUTES))
    price = forms.CharField(max_length=128, min_length=3, widget=forms.TextInput(attrs=PRICE_FIELD_ATTRIBUTES))
    description = forms.CharField(max_length=1024, widget=forms.Textarea(attrs=DESCRIPTION_FIELD_ATTRIBUTES))
    wielder_caste = forms.CharField(widget=forms.Select(choices=CASTE_CHOICES, attrs=CASTE_FIELD_ATTRIBUTES))
