from django.db import models
from django.core.exceptions import ValidationError

def Validate_email_adress(value):
    if not value.endswith('@estin.dz'):
        raise ValidationError("L'adresse mail ne fait pas parti du domaine 'ESTIN'.")

def Validate_matricule(value):
    if value >= 1000000000000 or value <= 99999999999:
        raise ValidationError("La matricule doit contenir 12 chiffres.")

def Validate_telephone(value):
    if value >=1000000000 or value <= 99999999:
        raise ValidationError("Le numero de telephone doit contenir au moins 9 chiffre (sans compte le 0)")

def Validate_fichier(value):
    if not value.endswith(".pdf"):
        raise ValidationError("Le fichier dois être un PDF.")

class CompteEtudiant(models.Model):
    matricule = models.fields.IntegerField(unique=True, validators= [Validate_matricule])
    nom = models.fields.CharField(max_length = 100)
    prenom = models.fields.CharField(max_length = 100)

    class Niveau(models.TextChoices):
        one = "1CP", "1CP"
        two = "2CP", "2CP"
        three = "1CS" , "1CS"
        four = "2CS" , "2CS"
        five = "3CS", "3CS"

    niveau_etude = models.fields.CharField(max_length = 5 , choices = Niveau.choices, default = "1CP")
    mot_de_passe = models.fields.CharField( max_length = 100 ) #Y a surement un moyen de la rendre invisible au formulaire, jsp si c'est mon boulot pour l'instant.
    adresse_mail = models.fields.EmailField(validators=[Validate_email_adress])
    telephone = models.fields.IntegerField(validators=[Validate_telephone])

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

    projet_concerne = models.fields.CharField(max_length=20)
    class TypeDeBesoin(models.TextChoices):
        Materiel = "MATERIEL"
        Budget = "BUDGET"
        Encadrement = "ENCADREMENT"
        Laboratoire = "LABORATOIRE"
        Support_Technique = "SUPPORT TECHNIQUE"
        Formation = "FORMATION"
        Networking = "NETWORKING"


    typeDeBesoin = models.fields.CharField(max_length = 20 , choices = TypeDeBesoin.choices, default = "MATERIEL") #si ça se trouve tu dois choisir parmi une liste
    description = models.fields.CharField(max_length = 1000)
    participant = models.ForeignKey(CompteEtudiant, on_delete = models.CASCADE)
    justification = models.fields.CharField(max_length=1000)
    file_path = models.FileField(upload_to="files/", null = True ,blank = True ,verbose_name="", validators=[Validate_fichier])
    statut = models.fields.CharField(max_length = 16, choices = Statut.choices, default = "NonVue")

class projet(models.Model):
    nom_projet= models.fields.CharField(max_length=100)
    description = models.fields.CharField(max_length=1000)
    participants = models.ManyToManyField(CompteEtudiant)
    probleme_resolu = models.fields.CharField(max_length=200)

    class Domaine(models.TextChoices):
        Technologie_et_sante = "Technologie et sante", "Technologie et sante"
        Technologie_et_finances = "Technologie et finances", "Technologie et finances"
        Technologie_et_Environement = "Technologie et environement", "Technologie et environement"
        E_commerce = "E-commerce", "E-commerce"
        Technologie_et_agriculture = "Technologie et agriculture", "Technologie et agriculture"
        Autre = "Autre", "Autre"

    domaine = models.CharField(max_length=30, choices= Domaine.choices, default="Autre")
    objectif = models.CharField(max_length=200)
    file_path = models.FileField(upload_to="files/", null = False,verbose_name="",validators=[Validate_fichier])
    statut = models.fields.CharField(max_length = 16, choices = Statut.choices, default = "NonVue")

    def get_participant(self):
        return self.participants.all()

class message(models.Model):#Message admin->etudiant
    objet = models.fields.CharField(max_length=200)
    contenu = models.fields.CharField(max_length=1500)
    emetteur = models.ForeignKey(CompteAdmin, on_delete= models.SET_NULL, null= True)
    receveur = models.ManyToManyField(CompteEtudiant)
    project = models.ForeignKey(projet, on_delete = models.CASCADE)
    vu = models.fields.BooleanField(default = False)

class contact(models.Model): #Message etudiant ->admin
    nom = models.fields.CharField(max_length=50)
    prenom = models.fields.CharField(max_length=50)
    email = models.fields.EmailField()
    objet = models.fields.CharField(max_length =100)
    message = models.fields.CharField(max_length= 1000)

