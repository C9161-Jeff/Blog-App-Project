from dataclasses import field
import imp
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        field = ("username", "email")

    def clean_email(self):#email customize validation yapılacak/ clean_...(ne custom edeceksen)
        email = self.cleaned_data["email"]#self(form doldurulduğunda oluşan instance)/doldurulan formdakı emali al
        if User.objects.filter(email=email).exists():#kontrol et kullancının girdiği başka bir user varsa
            raise forms.ValidationError("Please use another Email, that one already taken")#hata yükselt(raise ile)
        return email#yoksa normal email döndür    