from django.db import models
from django.contrib.auth.models import User


class GENUSERS_PROFIL(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    WEBSITE = models.CharField(max_length=500,null=True)
    DATEMODIFIED=models.DateField(null=True)
    LASTCONNECTION=models.DateField(null=True)
    NBCONNECTIONS=models.IntegerField(null=True)

# Create your models here.
class INDIV(models.Model):
    CODEI=models.IntegerField(primary_key=True)
    CODEPATRO = models.CharField(max_length=500,null=True)
    COMMUNED = models.CharField(max_length=20,null=True)
    COMMUNEN = models.CharField(max_length=20,null=True)
    GENRE = models.CharField(max_length=1,null=True)
    CODEF = models.ForeignKey('FAM', on_delete=models.CASCADE,null=True)
    DEPTD = models.CharField(max_length=20,null=True)
    DEPTN = models.CharField(max_length=20,null=True)
    LIEUD = models.CharField(max_length=30,null=True)
    LIEUN = models.CharField(max_length=30,null=True)
    DATED = models.CharField(max_length=20,null=True)
    DATEN = models.CharField(max_length=20,null=True)
    NOM = models.CharField(max_length=20,null=True)
    PRENOM = models.CharField(max_length=20,null=True)
    PROF = models.CharField(max_length=30,null=True)
    SIECLE = models.IntegerField(null=True)
    CODESN = models.IntegerField(null=True)
    CODESD = models.IntegerField(null=True)

class FAM(models.Model):
    CODEF = models.IntegerField(primary_key=True)
    COMMUNEM = models.CharField(max_length=20,null=True)
    DEPTM = models.CharField(max_length=20,null=True)
    LIEUM = models.CharField(max_length=30,null=True)
    DATEM = models.CharField(max_length=20,null=True)
    INDM = models.ForeignKey('INDIV',related_name='HOMMELINK',null=True,on_delete=models.CASCADE)
    INDF = models.ForeignKey('INDIV',related_name='FEMMELINK',null=True,on_delete=models.CASCADE)
    CODESM = models.IntegerField(null=True)

class SOURCES(models.Model):
    CODES = models.IntegerField(primary_key=True)
    TITRE = models.CharField(max_length=20,null=True)
    DESCRIPTION = models.CharField(max_length=200,null=True)

class METIERS(models.Model):
    LETTRE = models.CharField(max_length=1,null=True)
    NOMPROF = models.CharField(max_length=20,null=True)
    PERIODE = models.CharField(max_length=10,null=True)
    OCCURENCE= models.IntegerField(null=True)
    DEPT= models.CharField(max_length=20,null=True)
    DEF= models.CharField(max_length=1000,null=True)

class STAT_PATRO(models.Model):
    NOM = models.CharField(max_length=20, null=True)
    OCCURENCE = models.IntegerField(null=True)

class STAT_LIEUX(models.Model):
    COMMUNE = models.CharField(max_length=20, null=True)
    OCCURENCE = models.IntegerField(null=True)
    LATTITUDE = models.FloatField(null=True)
    LONGITUDE = models.FloatField(null=True)

class STAT_AGEMAR(models.Model):
    AGEMOYEN = models.FloatField(null=True)
    SIECLE = models.IntegerField(null=True)
    GENRE = models.IntegerField(null=True)

class STAT_ESPVIE(models.Model):
    ESPVIEMOYEN = models.FloatField(null=True)
    SIECLE = models.IntegerField(null=True)
    GENRE = models.IntegerField(null=True)

class ACTES(models.Model):
    class Part(models.TextChoices):
        PART1 = "1", "PART 1"
        PART2 = "2", "PART 2"
        PART3 = "3", "PART 3"
        PART4 = "4", "PART 4"

    class TYPE(models.TextChoices):
            C0 = "", "Vide"
            C1 = "MARIAGE", "MARIAGE"
            C2 = "NAISSANCE", "NAISSANCE"
            C3 = "DECES", "DECES"
    NUMACTES= models.IntegerField(primary_key=True)
    LOGIN= models.CharField(max_length=20, null=True,blank=True)
    TYPE= models.CharField(max_length=20, choices=TYPE.choices,default="")
    INTITULE= models.CharField(max_length=100, null=True,blank=True)
    LINKACTE = models.CharField(max_length=100, null=True,blank=True)
    DATE= models.CharField(max_length=20, null=True,blank=True)
    IMG_ACTES= models.ImageField(upload_to='img/actes',blank=True,null=True)
    NOM1= models.CharField(max_length=20, null=True)
    NOM2= models.CharField(max_length=20, null=True,blank=True)
    PRENOM1 = models.CharField(max_length=20, null=True)
    PRENOM2 = models.CharField(max_length=20, null=True,blank=True)
    DATE_ACTE = models.CharField(max_length=20, null=True)
    LINKACTE = models.CharField(max_length=100, null=True,blank=True)
    NUMPART_ACTE=models.CharField(
        max_length=1,
        choices=Part.choices,
        default=Part.PART1
    )



