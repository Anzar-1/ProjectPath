from django import forms
from PP.models import projet
from PP.models import Besoin
from PP.models import CompteEtudiant
from PP.models import CompteAdmin
from PP.models import contact
from PP.models import message

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomFKF(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        nom_complet = obj.last_name + " " + obj.first_name
        return "%s" % nom_complet

class CreateProject(forms.ModelForm):
    class Meta:
        model = projet
        exclude =  ('statut',)
    participants = CustomFKF(
        queryset = CompteEtudiant.objects.all()
     )

class requestNeed(forms.ModelForm):
    class Meta:
        model = Besoin
        exclude =  ('statut',)
    participant = CustomFKF(
        queryset = CompteEtudiant.objects.all()
    )

class CreateAccount(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'matricule', 'first_name' ,'last_name', 'email','niveau_etude' ,'telephone']

class authentification_Student(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class ModifyStudentAccount(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'matricule', 'first_name' ,'last_name', 'email','niveau_etude' ,'telephone']

class CreateAdmin(forms.ModelForm):
    class Meta:
        model = CompteAdmin
        fields = '__all__'

class Authentification_Admin(forms.ModelForm):
    class Meta:
        model= CompteAdmin
        fields = ["adresse_mail", "mot_de_passe"]

class contact_form(forms.ModelForm):
    class Meta:
        model = contact
        exclude =('vu',)

class message_form(forms.ModelForm):
    class Meta:
        model = message
        exclude = ('vu',)