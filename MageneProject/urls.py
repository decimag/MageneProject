"""MageneProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import  include
from django.conf.urls.static import static
from django.contrib.auth import views



from MageneApp import views
from MageneApp import views2,views3,views4

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('patro', views.patro,name='patro'),
    path('affBranche', views.affBranche),
    path('affArbre', views.affArbre),
    path('profession', views2.profession),
    path('listemetiers', views2.listemetiers),
    path('profcamp', views2.profcamp),
    path('stat', views2.stat),
    path('accounts/reset/done/', views2.pwdcomplete, name="password_change_done"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('adminform', views2.adminform),
    path('loginPlus', views2.loginPlus, name='loginPlus'),
    path('register', views2.sign_up,name='register'),
    path('resetpwd', views2.resetpwd,name='resetpwd'),
    path('cousacc', views2.cousacc,name='cousacc'),
    path('upload', views3.upload_file,name='upload'),
    path('enractes', views3.enractes,name='enractes'),
    path('TabActes', views3.TabActes,name='tabActes'),
    path('affActes', views3.affActes,name='affActes'),
    path('celebre', views3.celebre,name='celebre'),
    path('merci', views3.merci,name='merci'),
    path('gedDownload', views3.gedDownload,name='gedDownload'),
    path('download_file', views4.download_file,name='download_file'),
    path('profil', views2.profil,name='profil'),
    path('confirmation', views2.confirm_deletion,name='confirmation'),
    path('captcha/', include('captcha.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



