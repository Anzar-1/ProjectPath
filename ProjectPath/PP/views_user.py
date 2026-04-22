from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

#Student authentification

from PP.models import CompteEtudiant
from PP.form import CreateAccount
from PP.form import authentification_Student


def student_authentification(request):
    if request.method == "POST":
        form = authentification_Student(request.POST)
        form_inscription = CreateAccount(request.POST)
        if exists_Student(form) == [] or form_inscription.is_valid():
            if form_inscription.is_valid():
                user = form.save()
                return redirect("home", user.id)
            user_id = CompteEtudiant.objects.get(matricule = form["matricule"].value()).id
            return redirect("home", user_id)
        else:
            messages.error(request, "matricule ou mot de passe incorects.")
            return redirect("authentification")
    else:
        form = authentification_Student()
        form_inscription = CreateAccount()
    return render(request, "Student/authentification.html", {"form": form, "form_inscription": form_inscription})

def exists_Student(form):
    unmatched_fields = [] 
    try:
        matcher = CompteEtudiant.objects.get(matricule = form["matricule"].value()).get_fields() #y a un blem ici
        #ça retourne pas nul quand la matricule n'existe pas. je viens de le remarquer
    except CompteEtudiant.DoesNotExist:
        unmatched_fields.append("matricule")
        return unmatched_fields
    
    matcher = CompteEtudiant.objects.get(matricule = form["matricule"].value()).get_fields()
    if form["mot_de_passe"].value() != matcher[3]:
        unmatched_fields.append("mot_de_passe")

    return unmatched_fields

def user_details(request, user_id):
    user = CompteEtudiant.objects.get(id = user_id)
    return render(request, "Student/user.html", {"user": user, "user_id": user_id})

def modify_user_account(request, user_id):
    user = CompteEtudiant.objects.get(id = user_id)
    if request.method == "POST":
        form = CreateAccount(request.POST, instance = user)
        if form.is_valid():
            user = form.save()
            return redirect("user_details", user.id)
    else:
        form = CreateAccount(instance= user)
    return render(request, "Student/modify_user_account.html", {"form": form, "user": user})

def delete_user(request, user_id):
    user = CompteEtudiant.objecs.get( id =user_id)
    if request.method == "POST":
        user.delete()
        #return redirect("page_d'accueil")
    return render(request, "Student/delete_user.html")


#STAFF authetification

from PP.models import CompteAdmin
from PP.form import CreateAdmin
from PP.form import Authentification_Admin

from PP.models import projet
from PP.models import Besoin

def staff_Dashboard(request, user_id):
    
    project = projet.objects.all()
    project_nbr = project.count()
    prj_enAtt = projet.objects.filter(statut = "EnAttente").count()
    prj_valide = projet.objects.filter(statut = "Accepte").count()
    prj_refuse = projet.objects.filter(statut = "Refuse").count()
    
    besoin = Besoin.objects.all()
    besoin_nbr = besoin.count()
    bs_enAtt = Besoin.objects.filter(statut = "EnAttente").count()
    bs_valide = Besoin.objects.filter(statut = "Accepte").count()
    bs_refuse = Besoin.objects.filter(statut = "Refuse").count()

    return render(request, "Admin/dashboard.html",{"user_id": user_id, "project": project, "besoin": besoin,
                                                    "project_nbr": project_nbr, "prj_enAtt": prj_enAtt, " prj_valide": prj_valide,
                                                    "prj_refuse": prj_refuse ,"besoin_nbr": besoin_nbr, "bs_enAtt":bs_enAtt ,
                                                    "bs_valide":bs_valide, "bs_refuse": bs_refuse })

def create_staff_account(request):
    if request.method == "POST":
        form = CreateAdmin(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("project_list", user.id)
    else:
        form = CreateAdmin()
    return render(request, "Admin/create_account.html", {"form": form})

def staff_authetification(request):
    if request.method == "POST":
        form = Authentification_Admin(request.POST)
        if staff_exists(form) == []:
            user_id = CompteAdmin.objects.get(adresse_mail = form["adresse_mail"].value()).id
            return redirect("project_list", user_id)
        else:
            messages.error(request, "email ou mot de passe incorects.")
            return redirect("authentification")
    else:
        form = Authentification_Admin()
    return render(request, "Admin/authentification.html", {"form": form})
    
def staff_exists(form):    
    matcher = CompteAdmin.objects.get(adresse_mail = form["adresse_mail"].value()).get_fields()
    unmatched_fields = []

    if matcher is None:
        unmatched_fields.append("adresse_mail")
        return unmatched_fields
    
    if form["mot_de_passe"].value() != matcher[2]:
        unmatched_fields.append("mot de passe")

    return unmatched_fields
    
def staff_details(request, user_id):
    user = CompteAdmin.objects.get(id = user_id)
    return render(request, "Admin/user.html", {"user": user}) 
    
def modify_staff_account(request, user_id):
    user = CompteAdmin.objects.get(id = user_id)
    if request.method == "POST":
        form = CreateAdmin(request.POST, instance = user)
        if form.is_valid():
            user = form.save()
            return redirect("staff_details", user.id)
    else:
        form = CreateAdmin(instance= user)
    return render(request, "Admin/modify_account.html", {"form": form}) 

def delete_staff(request, user_id):
    user = CompteAdmin.objecs.get( id =user_id)
    if request.method == "POST":
        user.delete()
        #return redirect("page_d'accueil")
    return render(request, "Admin/delete_account.html")

#Other stuff


def index(request):
    return render(request, "Student/index.html")