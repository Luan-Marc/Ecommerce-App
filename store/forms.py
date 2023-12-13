from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'number', 'street', 'city', 'state', 'postal_code', 'card_number', 'card_expiration', 'card_cvv', 'number_house', 'card_name', 'email']
        labels = {
            'email' : 'Email',
            'card_name' : 'Nome Cartão',
            'number_house' : 'Número',
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'number': 'Número',
            'street': 'Rua',
            'city': 'Cidade',
            'state': 'Estado',
            'postal_code': 'Código Postal',
            'card_number': 'Número do Cartão',
            'card_expiration': 'Validade do Cartão',
            'card_cvv': 'CVV/CVC',
        }
        placeholders = {
            'email' : 'Digite Email',
            'card_name' : 'Nome do cartão',
            'number_house' : ' Número',
            'first_name': 'Digite seu primeiro nome',
            'last_name': 'Digite seu sobrenome',
            'number': 'Digite seu número',
            'street': 'Digite sua rua',
            'city': 'Digite sua cidade',
            'state': 'Digite seu estado',
            'postal_code': 'Digite seu código postal',
            'card_number': 'Digite o número do seu cartão',
            'card_expiration': 'MM/AAAA',
            'card_cvv': 'Digite o código de segurança',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': placeholders['first_name']}),
            'last_name': forms.TextInput(attrs={'placeholder': placeholders['last_name']}),
            'number': forms.TextInput(attrs={'placeholder': placeholders['number']}),
            'street': forms.TextInput(attrs={'placeholder': placeholders['street']}),
            'city': forms.TextInput(attrs={'placeholder': placeholders['city']}),
            'state': forms.TextInput(attrs={'placeholder': placeholders['state']}),
            'postal_code': forms.TextInput(attrs={'placeholder': placeholders['postal_code']}),
            'card_number': forms.TextInput(attrs={'placeholder': placeholders['card_number']}),
            'card_expiration': forms.TextInput(attrs={'placeholder': placeholders['card_expiration']}),
            'card_cvv': forms.TextInput(attrs={'placeholder': placeholders['card_cvv']}),
            'number_house': forms.TextInput(attrs={'placeholder': placeholders['number_house']}),
            'card_name': forms.TextInput(attrs={'placeholder': placeholders['card_name']}),
            'email': forms.TextInput(attrs={'placeholder': placeholders['email']}),

        }

