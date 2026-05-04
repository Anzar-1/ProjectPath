from PP.models import CompteEtudiant
from PP.models import message

from django.shortcuts import render
from django.shortcuts import redirect



def message_student(request, user_id):
    if request.user.id != user_id:
        return redirect("logout")
    user = CompteEtudiant.objects.get(id = user_id)
    message_de_etudiant = message.objects.filter(emetteur= user)
    nbr_message_de_etudiant =message.objects.filter(emetteur= user).count()
    
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

