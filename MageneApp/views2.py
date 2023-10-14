from MageneApp.forms import LoginForm,RegisterForm,ResetPwd,ProfilePlus,UserPlus
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from MageneApp.models import METIERS,FAM,STAT_PATRO,STAT_LIEUX,STAT_AGEMAR,STAT_ESPVIE,GENUSERS_PROFIL
from MageneApp import view_func_auth
from django.forms import inlineformset_factory

def profession(request):
    return render(request, "profession.html")

def listemetiers(request):
    listelettre = METIERS.objects.values('LETTRE').order_by('LETTRE').distinct()
    listemetiers = METIERS.objects.all()
    return render(request, "listemetiers.html",{'listelettre': listelettre, 'listemetiers': listemetiers})

def profcamp(request):
    return render(request, "profcamp.html")
def stat(request):
    listePatro=STAT_PATRO.objects.all()
    listeLieux=STAT_LIEUX.objects.all()
    listeAgeMoy=STAT_AGEMAR.objects.all()
    listeEspMoy = STAT_ESPVIE.objects.all()
    return render(request, "stat.html",{'Patro': listePatro, 'Lieux': listeLieux,'Agemar': listeAgeMoy,'Espvie': listeEspMoy})

def adminform(request):
    #---maj des tables stats par admin---
    OkFormSent = ''
    if 'AgeMar' in request.GET:
        objMar=FAM.objects.select_related('INDF').filter(INDF__DATED__isnull=False, DATEM__isnull=False)
        for f in objMar:
               d=f.INDF.CODEI
        OkFormSent = 'Envoyé AgeMar'
    return render(request, "adminform.html", {'Ret': OkFormSent})

def loginPlus(request):
    nxt = request.GET.get("next", None)

    if len(request.POST) > 0:
        form=LoginForm(request.POST)
        url='patro'
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                nxt = request.GET.get("next", None)
                if nxt is not None:
                    url = '?next=' + nxt
                    return redirect(nxt)
                else:
                    return redirect(url)
            else:
                return render(request, "registration/loginPlus.html", {'form': form,'msg': 'User ou mot de passe incorrect'})
        else:
            return render(request, "registration/loginPlus.html", {'form': form})
    else:
        form = LoginForm()
        return render(request, "registration/loginPlus.html", {'form': form})

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        formProfil = ProfilePlus()
        return render(request, 'registration/register.html', {'form': form,'formProfil': formProfil})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        formProfil = ProfilePlus(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            if formProfil.is_valid():
                profil = formProfil.save(commit=False)
                profil.user_id=user.id
                profil.save()
            login(request, user)
            return redirect('/loginPlus')
        else:
            return render(request, 'registration/register.html', {'form': form})

def resetpwd(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        email=request.POST['email']
        view_func_auth.prepare_mail(email,request)
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})

def pwdcomplete(request):
    return render(request, 'registration/password_reset_complete.html')

def profil(request):
    current_user = request.user
    if current_user.is_active:
        if len(request.GET)>0:
            current_profil = GENUSERS_PROFIL.objects.get(user_id=current_user.id)
            if 'Change' in request.GET:
                formProfil=ProfilePlus(request.GET,instance=current_profil)
                formUser = UserPlus(request.GET,instance=current_user)
                if formUser.is_valid():
                    formUser.save()
                if formProfil.is_valid():
                    formProfil.save()

                return render(request, 'registration/profil.html', {"form": formUser, "form2": formProfil})
            else:
                if 'Del' in request.GET:
                    return redirect('/confirmation')
        else:
            current_profil = GENUSERS_PROFIL.objects.get(user_id=current_user.id)
            formProfil = ProfilePlus(instance=current_profil)
            formUser = UserPlus( instance=current_user)
            return render(request, 'registration/profil.html', {"form": formUser, "form2": formProfil})
    else:
        return redirect('/loginPlus')


@login_required(login_url='loginPlus')
def cousacc(request):
    return render(request, "cousacc.html", {})

def confirm_deletion(request):
    if request.method == 'POST':
        user=request.user
        user.delete()
        return redirect('/index')
    else:
        return render(request, 'registration/deletionConfirm.html')




