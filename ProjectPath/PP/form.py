from django import forms
from PP.models import projet
from PP.models import Besoin
from PP.models import CompteEtudiant
from PP.models import CompteAdmin
from PP.models import contact

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        nom_complet = obj.nom + " " + obj.prenom
        return "%s" % nom_complet

class CustomFKF(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        nom_complet = obj.nom + " " + obj.prenom
        return "%s" % nom_complet

class CreateProject(forms.ModelForm):
    class Meta:
        model = projet
        exclude =  ('statut',)
    participants = CustomMMCF(
        queryset = CompteEtudiant.objects.all()
    )

class requestNeed(forms.ModelForm):
    class Meta:
        model = Besoin
        exclude =  ('statut',)
    participant = CustomFKF(
        queryset = CompteEtudiant.objects.all()
    )

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
    class Meta:
        model = contact
        exclude =('vu',)
