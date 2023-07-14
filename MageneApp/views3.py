import os
from django.utils.timezone import localtime
from django.shortcuts import render,redirect
from MageneApp.models import ACTES
from django.conf import settings
from .forms import UploadImageForm,MariageForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return redirect('patro')
    else:
        form = UploadImageForm()
    return render(request, 'upload.html', {'form': form})

def enractes(request):
    msg=''
    Nom1=""
    UserName= request.user
    dated=localtime().date().strftime('%Y-%m-%d')
    if request.method == 'POST':
        form = MariageForm(request.POST, request.FILES)
        Type = request.POST['TYPE']
        try:
            Nom1 = request.POST['NOM1']
        except Exception as e:
            print(e)

        if form.is_valid() :
            msg="Form Validé"
            Nom1 = request.POST['NOM1']
            Type = ""

            # file is saved
            form.save()
        else:

            if Nom1!="":
               msg="pas ok"
         #   return redirect('patro')
    else:
        form = MariageForm()
        Type=""
    return render(request, 'enractes.html', {'Type': Type,'form': form,'Msg': msg,'DateJ': dated,'UserName': UserName})

def TabActes(request):
    listNom1=list(ACTES.objects.filter(NOM1__isnull=False).values_list('NOM1',flat=True))
    listNom2=list(ACTES.objects.filter(NOM2__isnull=False).values_list('NOM2',flat=True))
    listNom3=sorted(set(listNom1+listNom2))
    Nom1=""
    try:
        Nom1 = request.POST['NomFiltre']
    except Exception as e:
        print(e)
    if Nom1 != "":
        ActesFilter=ACTES.objects.filter(NOM1__exact=Nom1).values() | ACTES.objects.filter(NOM2__exact=Nom1).values()
    else:
        ActesFilter =ACTES.objects.all().values()


    return render(request, 'tabActes.html', {'listeNoms': listNom3,'AffichNom':Nom1,'Actes':ActesFilter})

def affActes(request):
    path=settings.MEDIA_ROOT
    im_list=os.listdir(path + '/img/actes')
    pathImg= request.GET['pathImg']
    return render(request,'AfficheActes.html', {'im':  pathImg})


def celebre(request):
    return render(request, 'celebre.html')

def merci(request):
    return render(request, 'merci.html')

def gedDownload(request):
    return render(request, 'gedDownload.html')