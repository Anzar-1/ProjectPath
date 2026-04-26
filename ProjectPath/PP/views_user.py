from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

#Student authentification

from PP.models import CompteEtudiant
from PP.form import CreateAccount
from PP.form import authentification_Student, ModifyStudentAccount

from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import login_required

def logingout(request):
    logout(request)
    return redirect('authentification')

def student_authentification(request):
    if request.method == "POST":
        form = authentification_Student(request.POST)
        form_inscription = CreateAccount(request.POST)
        if form.is_valid() or form_inscription.is_valid():
            if form.is_valid():
                return authentificate_user(request, form)
            if form_inscription.is_valid():
                return sign_up(request, form_inscription)
        else: 
            print(form.errors)
            print(form_inscription.errors)
    else:
        form = authentification_Student()
        form_inscription = CreateAccount()
    return render(request, "Student/authentification.html", {"form": form, "form_inscription": form_inscription})

def authentificate_user(request,form):
    user_name = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(request,username =user_name, password =password)

    if user is not None :
        login(request, user)
        user_id = user.id
        return redirect("home", user_id)
    else:
        messages.error(request, "Nom d'utilisateur ou mot de passe incorects.")
        return 

def sign_up(request, form):
    user = form.save()
    login(request, user)
    user_id = user.id
    return redirect("home", user_id)

@login_required
def user_details(request, user_id):
    user = CompteEtudiant.objects.get(id = user_id)
    return render(request, "Student/user.html", {"user": user, "user_id": user_id})

@login_required
def modify_user_account(request, user_id):
    user = CompteEtudiant.objects.get(id = user_id)
    if request.method == "POST":
        form = ModifyStudentAccount(request.POST, instance = user)
        if form.is_valid():
            user = form.save()
            return redirect("user_details", user.id)
    else:
        form = ModifyStudentAccount(instance= user)
    return render(request, "Student/modify_user_account.html", {"form": form, "user": user})
#ça change pas le mot de passe.


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