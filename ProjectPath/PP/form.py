from django import forms
from PP.models import projet
from PP.models import Besoin
from PP.models import CompteEtudiant
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
        exclude =  ('statut','participants',)

class requestNeed(forms.ModelForm):
    class Meta:
        model = Besoin
        exclude =  ('statut',"participant")

    def clean_projet_concerne(self):
        project = self.cleaned_data.get('projet_concerne')

        if not projet.objects.filter(nom_projet=project).exists():
            raise forms.ValidationError("Ce projet n'existe pas.")

        return projet

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
        fields = ['username','matricule', 'first_name' ,'last_name', 'email' ,'niveau_etude' ,'telephone']

class ModifyAdminAccount(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'matricule', 'first_name' ,'last_name', 'email','niveau_etude' ,'telephone']

class message_form(forms.ModelForm):
    class Meta:
        model = message
        exclude = ('vu','emetteur', 'receveur', "project", "request")

