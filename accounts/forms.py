from django import forms
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
    UsernameField,
)
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.db.models import fields
from django.forms import models, widgets
from accounts.models import *

from django.forms.widgets import (
    DateInput,
    CheckboxSelectMultiple,
    Select,
    SelectMultiple,
    TextInput,
)
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission

User = get_user_model()


class loginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        label=("Remember Me"), initial=False, required=False
    )


class createUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Please enter username."})
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter full name."}),
        label="Full Name",
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Please enter date of birth."}
        ),
        label="Date of Birth",
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Please enter email."})
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter contact number."}),
        label="Contact Number",
    )


    class Meta:
        model = Account
        fields = (
            "username",
            "name",
            "dob",
            "email",
            "contact_number",
            "role",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override the 'role' field choices
        self.fields['role'].choices = [
            ('Admin', 'Admin'),
            ('User', 'User'),
        ]

class viewUserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter username.",
                   "disabled": "disabled"}
        )
    )
    
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter full name.",
                   "disabled": "disabled"}
        ),
        label="Full Name",
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "Please enter date of birth.",
                "disabled": "disabled",
            }
        ),
        label="Date of Birth",
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter email.", "disabled": "disabled"}
        )
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Please enter contact number.",
                "disabled": "disabled",
            }
        ),
        label="Contact Number",
    )

    class Meta:
        model = Account
        fields = (
            "username",
            "dob",
            "name",
            "email",
            "contact_number",
        )


class editUserForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Please enter username."})
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter full name."}),
        label="Full Name",
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Please enter date of birth."}
        ),
        label="Date of Birth",
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Please enter email."})
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter contact number."}),
        label="Contact Number",
    )
    password = None

    class Meta:
        model = Account
        fields = (
            "username",
            "dob",
            "name",
            "email",
            "contact_number",
            "role",

        )


class AdminUserChangeForm(forms.ModelForm):

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )    

            
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

class AdmineditUserForm(AdminUserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Please enter username."})
    )
    
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter full name."}),
        label="Full Name",
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Please enter date of birth."}
        ),
        label="Date of Birth",
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Please enter email."})
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter contact number."}),
        label="Contact Number",
    )



    class Meta:
        model = Account
        fields = (
            "username",
            "dob",
            "name",
            "email",
            "contact_number",
            "role",
        )

