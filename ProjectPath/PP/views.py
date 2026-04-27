from django.shortcuts import render
from django.shortcuts import redirect

from PP.models import projet
from PP.form import CreateProject

from PP.models import Besoin
from PP.form import requestNeed

from PP.models import CompteEtudiant

from PP.models import message
from django.contrib.auth.decorators import login_required

#Project CRUD

@login_required
def add_project(request,user_id):
    if request.user.id != user_id:
        return redirect("logout")
    if request.method =="POST":
        form = CreateProject(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home", user_id)
    else:
        form = CreateProject()
    return render(request, "Student/add_project.html", {'form' : form ,"user_id": user_id})

@login_required
def project_details(request, project_id,user_id,user_type):
    if request.user.id != user_id:
        return redirect("logout")
    projett =  projet.objects.get(id = project_id)
    messages = message.objects.filter(project = projett)
    message_nbr = messages.count()
    etudiants = projett.get_participant()
    if user_type == 1:
        projett.statut = "EnAttente"
        projett.save()
        if request.method == "POST":
            return accept_refuse_form(request, projett,user_id)
        return render(request, "Admin/project_details.html", {"p" : projett , "etudiants" : etudiants ,
                                                    "user_id": user_id, "message" : messages,"message_nb":message_nbr ,
                                                    "user_type":user_type})
    elif user_type == 0:
        return render(request, "Student/project_details.html", {"p" : projett ,"user_id": user_id, "message" : messages, 
                                                    "user_type":user_type, "etudiants": etudiants})

@login_required
def accept_refuse_form(request, projett, user_id):
    if request.user.id != user_id:
        return redirect("logout")
    if "accept" in request.POST:
        projett.statut = "Accepte"
        projett.save()

    elif "refuse" in request.POST:
       projett.statut = "Refuse"
       projett.save()
      
    elif "document_manquant" in request.POST:
        projett.statut = "DocumentManquant"
        projett.save()

    thingie_id = projett.id
    return redirect("commentaire",thingie_id,user_id)

@login_required
def modify_project(request,project_id,user_id):
    if request.user.id != user_id:
        return redirect("logout")
    p = projet.objects.get(id= project_id)
    if request.method == "POST":
        form = CreateProject(request.POST, request.FILES, instance = p )
        if form.is_valid():
            p = form.save()
            p.statut = "NonVue"
            p.save()
            return redirect("project_details",project_id, user_id)
    else:
        form = CreateProject(instance=p)
    return render(request,"Student/add_project.html", {"form" : form ,"user_id": user_id})




#Request CRUD

@login_required
def home(request,user_id):
    if request.user.id != user_id:
        return redirect("logout")
    user = CompteEtudiant.objects.get(id = user_id) 
    user_projects = user.projet_set.all()
    user_request = user.besoin_set.all()
    return render(request,"Student/home.html",{"user" : user, "user_projects": user_projects,
                                               "user_request":user_request ,"user_id": user_id})

@login_required
def request_details(request,b_id,user_id,user_type):
    if request.user.id != user_id:
        return redirect("logout")
    b= Besoin.objects.get(id= b_id)
    messages = message.objects.filter(request = b)
    message_nbr = messages.count()
    etudiants = b.participant
    if user_type == 1:
        b.statut = "EnAttente"
        b.save()
        if request.method == "POST":
            accept_refuse_form(request, b)
        return render(request, "Admin/besoin_details.html", {"b" : b , "etudiants" : etudiants ,
                                                    "user_id": user_id, "message" : messages, "messag_nb":message_nbr,
                                                    "user_type":user_type})
    elif user_type == 0:
        return render(request, "Student/project_details.html", {"b" : b ,"user_id": user_id, "message" : messages, 
                                                    "user_type":user_type, "etudiants": etudiants})

@login_required
def add_request(request, user_id):
    if request.user.id != user_id:
        return redirect("logout")
    if request.method == "POST":
        form = requestNeed(request.POST, request.FILES)
        if form.is_valid():
            b = form.save()
            return redirect("request_details",b.id, user_id)
    else:
        form = requestNeed()
    return render(request, "Student/add_besoin.html", {"form" : form ,"user_id": user_id})

@login_required
def modify_request(request, b_id,user_id):
    if request.user.id != user_id:
        return redirect("logout")
    besoin = Besoin.objects.get(id = b_id)
    if request.method == "POST":
        form = requestNeed(request.POST, request.FILES,instance = besoin)
        if form.is_valid():
            b = form.save()
            b.statut = "NonVue"
            b.save()
            return redirect("request_details",b_id, user_id)
    else:
        form = requestNeed(instance= besoin)
    return render(request, "Student/add_besoin.html", {"form" : form,"user_id": user_id})
