from django import forms
from PP.models import projet
from PP.models import Besoin
from PP.models import CompteEtudiant
from PP.models import CompteAdmin

class CreateProject(forms.ModelForm):
    class Meta:
        model = projet
        exclude =  ('statut',)

class requestNeed(forms.ModelForm):
    class Meta:
        model = Besoin
        exclude =  ('statut',)

class CreateAccount(forms.ModelForm):
    class Meta:
        model = CompteEtudiant
        fields = '__all__'

class authentification_Student(forms.ModelForm):
    class Meta:
        model = CompteEtudiant
        fields= ['matricule', 'mot_de_passe']
    #Je l'ai toujours pas implementé

class CreateAdmin(forms.ModelForm):
    class Meta:
        model = CompteAdmin
        fields = '__all__'

class Authentification_Admin(forms.ModelForm):
    class Meta:
        model= CompteAdmin
        fields = ["adresse_mail", "mot_de_passe"]

class contact_form(forms.Form):
    nom = forms.fields.CharField(max_length=50)
    prenom = forms.fields.CharField(max_length=50)
    email = forms.fields.EmailField()
    objet = forms.fields.CharField(max_length =100)
    message = forms.fields.CharField(max_length= 1000)
