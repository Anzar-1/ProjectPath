from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

#Student authentification

from PP.models import CompteEtudiant
from PP.form import CreateAccount
from PP.form import authentification_Student


def create_acount(request):
    if request.method == "POST":
        form = CreateAccount(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("home", user.id)
    else:
        form = CreateAccount()
    return render(request, "Student/create_account.html", {"form": form})

def student_authentification(request):
    if request.method == "POST":
        form = authentification_Student(request.POST)
        if exists_Student(form) == []:
            user_id = CompteEtudiant.objects.get(matricule = form["matricule"].value()).id
            return redirect("home", user_id)
        else:
            messages.error(request, "matricule ou mot de passe incorects.")
            return redirect("authentification")
    else:
        form = authentification_Student()
    return render(request, "Student/authentification.html", {"form": form})

def exists_Student(form):
    matcher = CompteEtudiant.objects.get(matricule = form["matricule"].value()).get_fields()
    unmatched_fields = []
    if matcher is None:
        unmatched_fields.append("matricule")
        return unmatched_fields
        

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
    return render(request, "Student/modify_user_account.html", {"form": form})

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

from PP.form import contact_form
from django.core.mail import send_mail
from ProjectPath.settings import EMAIL_HOST_USER

def contact_us(request,user_id):
    if request.method =="POST":
        form = contact_form(request.POST)
        if form.is_valid():
            send_mail(subject=f'Message from {{form.cleaned_data["adresse_mail"] or "anonyme"}} via ProjectPath Contact us form.',
                     message= form.cleaned_data["message"], from_email=EMAIL_HOST_USER,
                     recipient_list= ["germanotifa1@gmail.com"])

    else:
        form = contact_form()
    return render(request, "Student/contact_us.html", {"form": form})



import json

def seding_mail(request):
    with open("api-key.json") as f: key = json.load(f)["key"] #faudrait que je lui demainde que represente ces fichier
    with open("token.json") as f: token = json.load(f)

    url = "https://api0utmail-test-email.vercel.app/sendHtml"
    payload = {
        "api_key": key,
        "google_token": token,
        "to": "friend@gmail.com",
        "subject": "Python Test",
        "html": "<h1>Hello form Python</h1>"
    }

    r = render(request,url, json=payload)
    print(r.json())

def index(request):
    return render(request, "Student/index.html")