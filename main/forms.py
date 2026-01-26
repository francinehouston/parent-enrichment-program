from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Program, Participant, MemberDocument, VendorSubmission


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'description', 'date', 'time', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'phone', 'children_ages']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'children_ages': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name (optional)'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name (optional)'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = MemberDocument
        fields = ['document_type', 'file', 'notes']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes about this document'}),
        }


class VendorSubmissionForm(forms.ModelForm):
    class Meta:
        model = VendorSubmission
        fields = ['service_name', 'business_name', 'contact_name', 'email', 'phone', 'price_list', 'description',
                  'discount_percentage', 'service_price', 'overall_value', 'frequency',
                  'free_service_name', 'free_service_frequency']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the name of your service or sales offering'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your business name (optional)'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(555) 123-4567'}),
            'price_list': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional: Describe your service and how it benefits P.E.P. members'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10.00 for 10%', 'step': '0.01', 'min': '0', 'max': '100'}),
            'service_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 99.99', 'step': '0.01', 'min': '0'}),
            'overall_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 199.99', 'step': '0.01', 'min': '0'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'free_service_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of the free service (if applicable)'}),
            'free_service_frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., "Once per month", "One-time", "Annually"'}),
        }

