from django.db import models
from django.core.exceptions import ValidationError

def Validate_email_adress(value):
    if not value.endswith('@estin.dz'):
        raise ValidationError("L'adresse mail ne fait pas parti du domaine 'ESTIN'.")


class CompteEtudiant(models.Model):
    matricule = models.fields.IntegerField(unique=True)
    nom = models.fields.CharField(max_length = 100)
    prenom = models.fields.CharField(max_length = 100)

    class Niveau(models.TextChoices):
        one = "1CP"
        two = "2CP"
        three = "1CS"
        four = "2CS"
        five = "3CS"

    niveau_etude = models.fields.CharField(max_length = 5 , choices = Niveau.choices, default = "1CP")
    mot_de_passe = models.fields.CharField( max_length = 100 ) #Y a surement un moyen de la rendre invisible au formulaire, jsp si c'est mon boulot pour l'instant.
    adresse_mail = models.fields.EmailField(validators=[Validate_email_adress])
    telephone = models.fields.IntegerField()

    def get_fields(self):
        return([self.matricule, self.nom, self.prenom, self.mot_de_passe, self.adresse_mail, self.telephone])

class CompteAdmin(models.Model):
    nom = models.fields.CharField(max_length = 100)
    prenom = models.fields.CharField(max_length= 100)
    mot_de_passe = models.fields.CharField()
    adresse_mail = models.fields.EmailField(validators=[Validate_email_adress])
    telephone = models.fields.IntegerField()

    def get_fields(self):
        return([self.nom, self.prenom, self.mot_de_passe, self.adresse_mail, self.telephone])

class Statut(models.TextChoices):
    NON_VUE = "NonVue"
    EN_ATTENTE = "EnAttente"
    ACCEPTE = "Accepte"
    REFUSE = "Refuse"
    DOCUMENT_MAQUANT = "DocumentManquant"

class Besoin(models.Model):
    typeDeBesoin = models.fields.CharField(max_length = 100) #si ça se trouve tu dois choisir parmi une liste
    description = models.fields.CharField(max_length = 1000)
    participants = models.ManyToManyField(CompteEtudiant)
    statut = models.fields.CharField(max_length = 16, choices = Statut.choices, default = "NonVue")

class projet(models.Model):
    nom_projet= models.fields.CharField(max_length=100)
    description = models.fields.CharField(max_length=1000)
    participants = models.ManyToManyField(CompteEtudiant)
    file_path = models.FileField(upload_to="files/", null = False,verbose_name="")
    statut = models.fields.CharField(max_length = 16, choices = Statut.choices, default = "NonVue")

    def get_participant(self):
        return self.participants.all()

class message(models.Model):
    objet = models.fields.CharField(max_length=200)
    contenu = models.fields.CharField(max_length=1500)
    emetteur = models.ForeignKey(CompteAdmin, on_delete= models.SET_NULL, null= True)
    receveur = models.ManyToManyField(CompteEtudiant)
    project = models.ForeignKey(projet, on_delete = models.CASCADE)


