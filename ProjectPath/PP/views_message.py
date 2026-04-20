from PP.models import CompteEtudiant
from PP.models import message
from PP.models import contact

from django.shortcuts import render
from django.shortcuts import redirect

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


def message_student(request, user_id):
    user = CompteEtudiant.objects.get(id = user_id)
    message_de_etudiant = contact.objects.filter(email = user.adresse_mail)
    nbr_message_de_etudiant =contact.objects.filter(email = user.adresse_mail).count()
    
    message_de_admin = message.objects.filter(receveur= user)
    nbr_message_de_admin = message.objects.filter(receveur= user).count()

    message_non_lu = message.objects.filter(vu = False)
    nbr_message_non_lu = message.objects.filter(vu = False).count()
  
    for m in message_non_lu:
        m.vu = True
        m.save()
        

    return render(request, "Student/Message/message.html", {"user_id": user_id, "message_admin": message_de_admin,
                                                            "message_etudiant": message_de_etudiant, 
                                                            "nbr_admin":nbr_message_de_admin, 
                                                            "nbr_etudiant":nbr_message_de_etudiant,
                                                            "nbr_message_non_vu": nbr_message_non_lu})

