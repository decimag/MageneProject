from MageneApp.models import INDIV,FAM,SOURCES
from django.shortcuts import render
from pathlib import Path
import os
# Create your views here.
# 65 in char is A
# 90 in char is Z
#for i in range(65, 91):
#    print(chr(i), end=" ")
def patro(request):
    ListAlph=[]
    for i in range(65, 91):
        ListAlph.append(chr(i))
    if 'letter' in request.GET:
        ll=request.GET['letter']
        listenom=INDIV.objects.values('NOM').filter(NOM__startswith=ll).order_by('NOM').distinct()
        return render(request, "patro.html", {'letter_list': ListAlph, 'toto': listenom})
    else:
        return render(request, "patro.html", {'letter_list': ListAlph})

def index(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    toto=os.path.join(BASE_DIR, 'MageneApp','static')
    return render(request, "index.html", {'toto': toto,'titi': BASE_DIR})

def getMar(idMar,Genre):
    ret=''
    if Genre=='F':
     listeMar=FAM.objects.filter(INDF=idMar)
     for indF in listeMar:
         if indF.INDM_id is not None:
            x1=INDIV.objects.get(CODEI=indF.INDM_id)
            ret=' X (' + str(indF.DATEM if indF.DATEM is not None else '') + ') ' + str(x1.NOM) + ' ' + str(x1.PRENOM if x1.PRENOM is not None else '')
    else:
        listeMar=FAM.objects.filter(INDM=idMar).select_related('INDM')
        for indF in listeMar:
          if indF.INDF_id is not None:
            x1=INDIV.objects.get(CODEI=indF.INDF_id)
            ret=ret + ' X (' + str(indF.DATEM if indF.DATEM is not None else '') + ') ' + str(x1.NOM) + ' ' + str(x1.PRENOM if x1.PRENOM is not None else '')
    return ret



def affBranche(request):
    listeNom=[]
    if 'patro' in request.GET:
        patro = request.GET['patro']
        listenom=INDIV.objects.filter(NOM=patro).order_by('CODEPATRO')
        for rec in listenom:
            CODEF=FAM.objects.filter(INDM=rec.CODEI) | FAM.objects.filter(INDF=rec.CODEI)
            strNom=str(rec.NOM) + ' ' + str(rec.PRENOM if rec.PRENOM is not None else '')
            strDateN= '(°' + str(rec.DATEN if rec.DATEN is not None else '') + ')'
            strMar= getMar(rec.CODEI, rec.GENRE)
            tab=[]
            tab.append(rec.CODEPATRO)
            tab.append(strNom)
            tab.append(strDateN)
            tab.append(strMar)
            tab.append(CODEF[0].CODEF)

            listeNom.append(tab)
        return render(request, "affBranche.html", {'html': listeNom})

def getIndiCode(Fam,Genre):
    if Fam is not None:
        listeMar = FAM.objects.get(CODEF=Fam)
        if Genre=='F':
         ret=str(listeMar.INDF_id if listeMar.INDF_id is not None else '')
        else:
         ret=str(listeMar.INDM_id if listeMar.INDM_id is not None else '')
    else:
        ret=''
    return ret

def getIndObj(vInd):
    Ind=INDIV.objects.filter(CODEI=vInd)[0]
    return Ind

def getMariObj(vMar):
    Mar=FAM.objects.filter(CODEF=vMar)[0]
    return Mar
def getEnf(vCodef):
    EnfListe = INDIV.objects.filter(CODEF_id=vCodef)
    CodeFEnf = []
    for enf in EnfListe:
        TB1=[]
        CODEF = FAM.objects.filter(INDM=enf.CODEI) | FAM.objects.filter(INDF=enf.CODEI)
        TB1.append(CODEF[0].CODEF)
        TB1.append(enf.PRENOM)
        CodeFEnf.append(TB1)
    return CodeFEnf

def getListeMar(vInd,vFamExl):
    CodeFMar=[]
    listMar = FAM.objects.filter(INDM=vInd) | FAM.objects.filter(INDF=vInd)
    for fam in listMar:
        if str(fam.CODEF) != str(vFamExl):
            CodeFMar.append(fam.CODEF)
    return CodeFMar
def affArbre(request):
    listeMMar=[]
    listeFMar=[]
    if 'CODEF' in request.GET:
        CodeM=request.GET['CODEF']
        Mar=getMariObj(CodeM)
        EnfListe=getEnf(CodeM)
        MaleCode=getIndiCode(CodeM, 'M')
        CodeF21=-1
        if MaleCode != '':
            listeMMar=getListeMar(MaleCode,CodeM)
            MaleInfo=getIndObj(MaleCode)
            Fam = FAM.objects.filter(INDM_id=MaleCode)
            SRCN = SOURCES.objects.filter(CODES=MaleInfo.CODESN)
            SRCD = SOURCES.objects.filter(CODES=MaleInfo.CODESD)
            SRCM = SOURCES.objects.filter(CODES=Fam[0].CODESM)
            MaleCode21=getIndiCode(MaleInfo.CODEF_id, 'M')

            if MaleCode21 != '':
                MaleInfo21 = getIndObj(MaleCode21)
                Fam21 = FAM.objects.filter(INDM=MaleCode21)
                SRC21N= SOURCES.objects.filter(CODES=MaleInfo21.CODESN)
                SRC21D = SOURCES.objects.filter(CODES=MaleInfo21.CODESD)
                SRC21M = SOURCES.objects.filter(CODES=Fam21[0].CODESM)
                CodeF21 = Fam21[0].CODEF
                Mar21 = getMariObj(CodeF21)
                MaleCode31 = getIndiCode(MaleInfo21.CODEF_id, 'M')
                if MaleCode31 != '':
                   MaleInfo31 = getIndObj(MaleCode31)
                   Fam31 = FAM.objects.filter(INDM=MaleCode31)
                   SRC31N = SOURCES.objects.filter(CODES=MaleInfo31.CODESN)
                   SRC31D = SOURCES.objects.filter(CODES=MaleInfo31.CODESD)
                   SRC31M = SOURCES.objects.filter(CODES=Fam31[0].CODESM)
                   CodeF31 = Fam31[0].CODEF
                   Mar31 = getMariObj(CodeF31)
                else:
                    CodeF31 = -1
                    SRC31N = SOURCES
                    SRC31D = SOURCES
                    SRC31M = SOURCES
                    Mar31 = FAM
                    MaleInfo31=INDIV
                FemelleCode31 = getIndiCode(MaleInfo21.CODEF_id, 'F')
                if FemelleCode31 != '':
                    FemelleInfo31 = getIndObj(FemelleCode31)
                    Fam31 = FAM.objects.filter(INDF=FemelleCode31)
                    SRC31NF = SOURCES.objects.filter(CODES=FemelleInfo31.CODESN)
                    SRC31DF = SOURCES.objects.filter(CODES=FemelleInfo31.CODESD)
                    SRC31MF = SOURCES.objects.filter(CODES=Fam31[0].CODESM)
                    CodeF31F = Fam31[0].CODEF
                else:
                    FemelleInfo31 = INDIV
                    SRC31NF = SOURCES
                    SRC31DF = SOURCES
                    SRC31MF = SOURCES
                    CodeF31F=-1
            else:
                MaleInfo21=INDIV
                CodeF21 = -1
                SRC21N = SOURCES
                SRC21D = SOURCES
                SRC21M = SOURCES
                Mar21 = FAM
                MaleInfo31 = INDIV
                Mar31 = FAM
                CodeF31 = -1
                SRC31N = SOURCES
                SRC31D = SOURCES
                SRC31M = SOURCES
                FemelleInfo31 = INDIV
                SRC31NF = SOURCES
                SRC31DF = SOURCES
                SRC31MF = SOURCES
                CodeF31F = -1
                Mar31 = FAM
            FemelleCode21 = getIndiCode(MaleInfo.CODEF_id, 'F')
            if FemelleCode21 != '':
                FemelleInfo21 = getIndObj(FemelleCode21)
                Fam31 = FAM.objects.filter(INDF=FemelleCode21)
                SRC21NF = SOURCES.objects.filter(CODES=FemelleInfo21.CODESN)
                SRC21DF = SOURCES.objects.filter(CODES=FemelleInfo21.CODESD)
                SRC21MF = SOURCES.objects.filter(CODES=Fam31[0].CODESM)
                CodeF21F = Fam31[0].CODEF
                MaleCode32 = getIndiCode(FemelleInfo21.CODEF_id, 'M')
                if MaleCode32 != '':
                    MaleInfo32 = getIndObj(MaleCode32)
                    Fam32 = FAM.objects.filter(INDM=MaleCode32)
                    SRC32N = SOURCES.objects.filter(CODES=MaleInfo32.CODESN)
                    SRC32D = SOURCES.objects.filter(CODES=MaleInfo32.CODESN)
                    SRC32M = SOURCES.objects.filter(CODES=Fam32[0].CODESM)
                    CodeF32 = Fam32[0].CODEF
                    Mar32 = getMariObj(CodeF32)
                else:
                    MaleInfo32 = INDIV
                    SRC32N = SOURCES
                    SRC32D = SOURCES
                    Mar32 = FAM
                    SRC32M = SOURCES
                    CodeF32 = -1
                FemelleCode32 = getIndiCode(FemelleInfo21.CODEF_id, 'F')
                if FemelleCode32 != '':
                    FemelleInfo32 = getIndObj(FemelleCode32)
                    Fam31 = FAM.objects.filter(INDF=FemelleCode32)
                    SRC32NF = SOURCES.objects.filter(CODES=FemelleInfo32.CODESN)
                    SRC32DF = SOURCES.objects.filter(CODES=FemelleInfo32.CODESD)
                    SRC32MF = SOURCES.objects.filter(CODES=Fam31[0].CODESM)
                    CodeF32F = Fam31[0].CODEF
                else:
                    FemelleInfo32 = INDIV
                    Mar32 = FAM
                    SRC32NF = SOURCES
                    SRC32DF = SOURCES
                    SRC32MF = SOURCES
                    CodeF32F = -1
            else:
                FemelleInfo21=INDIV
                Mar21 = FAM
                SRC21NF = SOURCES
                SRC21DF = SOURCES
                SRC21MF = SOURCES
                CodeF21F = -1
                MaleInfo32 = INDIV
                Mar32 = FAM
                SRC32N = SOURCES
                SRC32D = SOURCES
                SRC32M = SOURCES
                CodeF32 = -1
                FemelleInfo32 = INDIV
                SRC32NF = SOURCES
                SRC32DF = SOURCES
                SRC32MF = SOURCES
                CodeF32F = -1
        else:
            MaleInfo=INDIV
            SRCN = SOURCES
            SRCD = SOURCES
            SRCM = SOURCES
            MaleInfo21 = INDIV
            Mar21 = FAM
            SRC21N = SOURCES
            SRC21D = SOURCES
            SRC21M = SOURCES
            CodeF21 = -1
            FemelleInfo21 = INDIV
            SRC21NF = SOURCES
            SRC21DF = SOURCES
            SRC21MF = SOURCES
            CodeF21F = -1
            MaleInfo31 = INDIV
            Mar31 = FAM
            SRC31N = SOURCES
            SRC31D = SOURCES
            SRC31M = SOURCES
            CodeF31 = -1
            FemelleInfo31 = INDIV
            SRC31NF = SOURCES
            SRC31DF = SOURCES
            SRC31MF = SOURCES
            CodeF31F = -1
            MaleInfo32 = INDIV
            Mar32 = FAM
            SRC32N = SOURCES
            SRC32D = SOURCES
            SRC32M = SOURCES
            CodeF32 = -1
            FemelleInfo32 = INDIV
            SRC32NF = SOURCES
            SRC32DF = SOURCES
            SRC32MF = SOURCES
            CodeF32F = -1
        FemelleCode=getIndiCode(CodeM, 'F')
        if FemelleCode != '':
            listeFMar = getListeMar(FemelleCode, CodeM)
            FemelleInfo = getIndObj(FemelleCode)
            Fam = FAM.objects.filter(INDF_id=FemelleCode)
            SRCNF = SOURCES.objects.filter(CODES=FemelleInfo.CODESN)
            SRCDF = SOURCES.objects.filter(CODES=FemelleInfo.CODESD)
            SRCMF = SOURCES.objects.filter(CODES=Fam[0].CODESM)
            if FemelleInfo.CODEF is not None:
               MaleCode22 = getIndiCode(FemelleInfo.CODEF_id, 'M')
            else:
                MaleCode22=''
            if MaleCode22 != '':
                MaleInfo22 = getIndObj(MaleCode22)
                Fam22 = FAM.objects.filter(INDM=MaleCode22)
                SRC22N = SOURCES.objects.filter(CODES=MaleInfo22.CODESN)
                SRC22D = SOURCES.objects.filter(CODES=MaleInfo22.CODESN)
                SRC22M = SOURCES.objects.filter(CODES=Fam22[0].CODESM)
                CodeF22 = Fam22[0].CODEF
                Mar22 = getMariObj(CodeF22)
                MaleCode33 = getIndiCode(MaleInfo22.CODEF_id, 'M')
                if MaleCode33 != '':
                    MaleInfo33 = getIndObj(MaleCode33)
                    Fam33 = FAM.objects.filter(INDM=MaleCode33)
                    SRC33N = SOURCES.objects.filter(CODES=MaleInfo33.CODESN)
                    SRC33D = SOURCES.objects.filter(CODES=MaleInfo33.CODESN)
                    SRC33M = SOURCES.objects.filter(CODES=Fam33[0].CODESM)
                    CodeF33 = Fam33[0].CODEF
                    Mar33 = getMariObj(CodeF33)
                else:
                    MaleInfo33 = INDIV
                    SRC33N = SOURCES
                    SRC33D = SOURCES
                    SRC33M = SOURCES
                    Mar33 = FAM
                    CodeF33=-1
                FemelleCode33 = getIndiCode(MaleInfo22.CODEF_id, 'F')
                if FemelleCode33 != '':
                    FemelleInfo33 = getIndObj(FemelleCode33)
                    Fam31 = FAM.objects.filter(INDF=FemelleCode33)
                    SRC33NF = SOURCES.objects.filter(CODES=FemelleInfo33.CODESN)
                    SRC33DF = SOURCES.objects.filter(CODES=FemelleInfo33.CODESD)
                    SRC33MF = SOURCES.objects.filter(CODES=Fam31[0].CODESM)
                    CodeF33F = Fam31[0].CODEF
                else:
                    FemelleInfo33 = INDIV
                    Mar33 = FAM
                    SRC33NF = SOURCES
                    SRC33DF = SOURCES
                    SRC33MF = SOURCES
                    CodeF33F = -1
            else:
                MaleInfo22 = INDIV
                SRC22N = SOURCES
                SRC22D = SOURCES
                SRC22M = SOURCES
                Mar22 = FAM
                CodeF22=-1
                MaleInfo33 = INDIV
                SRC33N = SOURCES
                SRC33D = SOURCES
                SRC33M = SOURCES
                CodeF33 = -1
                Mar33= FAM
                FemelleInfo33 = INDIV
                SRC33NF = SOURCES
                SRC33DF = SOURCES
                SRC33MF = SOURCES
                CodeF33F = -1
            if FemelleInfo.CODEF is not None:
                FemelleCode22 = getIndiCode(FemelleInfo.CODEF_id, 'F')
            else:
                FemelleCode22=''
            if FemelleCode22 != '':
                FemelleInfo22 = getIndObj(FemelleCode22)
                Fam31 = FAM.objects.filter(INDF=FemelleCode22)
                SRC22NF = SOURCES.objects.filter(CODES=FemelleInfo22.CODESN)
                SRC22DF = SOURCES.objects.filter(CODES=FemelleInfo22.CODESD)
                SRC22MF = SOURCES.objects.filter(CODES=Fam31[0].CODESM)
                CodeF22F = Fam31[0].CODEF
                MaleCode34 = getIndiCode(FemelleInfo22.CODEF_id, 'M')
                if MaleCode34 != '':
                    MaleInfo34 = getIndObj(MaleCode34)

                    Fam34 = FAM.objects.filter(INDM=MaleCode34)
                    SRC34N = SOURCES.objects.filter(CODES=MaleInfo34.CODESN)
                    SRC34D = SOURCES.objects.filter(CODES=MaleInfo34.CODESN)
                    SRC34M = SOURCES.objects.filter(CODES=Fam34[0].CODESM)
                    CodeF34 = Fam34[0].CODEF
                    Mar34 = getMariObj(CodeF34)
                else:
                    MaleInfo34 = INDIV
                    SRC34N = SOURCES
                    SRC34D = SOURCES
                    SRC34M = SOURCES
                    Mar34 = FAM
                    CodeF34=-1
                FemelleCode34 = getIndiCode(FemelleInfo22.CODEF_id, 'F')
                if FemelleCode34 != '':
                    FemelleInfo34 = getIndObj(FemelleCode34)
                    SRC34NF = SOURCES.objects.filter(CODES=FemelleInfo34.CODESN)
                    SRC34DF = SOURCES.objects.filter(CODES=FemelleInfo34.CODESD)
                    SRC34MF = SOURCES.objects.filter(CODES=Fam31[0].CODESM)
                    CodeF34F = Fam31[0].CODEF
                else:
                    FemelleInfo34 = INDIV
                    Mar34 = FAM
                    SRC34NF = SOURCES
                    SRC34DF = SOURCES
                    SRC34MF = SOURCES
                    CodeF34F = -1
            else:
                FemelleInfo22 = INDIV
                Mar22 = FAM
                SRC22NF = SOURCES
                SRC22DF = SOURCES
                SRC22MF = SOURCES
                CodeF22F = -1
                MaleInfo34 = INDIV
                SRC34N = SOURCES
                SRC34D = SOURCES
                SRC34M = SOURCES
                Mar34 = FAM
                CodeF34 = -1
                FemelleInfo34 = INDIV
                SRC34NF = SOURCES
                SRC34DF = SOURCES
                SRC34MF = SOURCES
                CodeF34F = -1
        else:
            FemelleInfo = INDIV
            SRCNF = SOURCES
            SRCDF = SOURCES
            SRCMF = SOURCES
            MaleInfo22 = INDIV
            Mar22 = FAM
            SRC22N = SOURCES
            SRC22D = SOURCES
            SRC22M = SOURCES
            CodeF22 = -1
            FemelleInfo22 = INDIV
            SRC22NF = SOURCES
            SRC22DF = SOURCES
            SRC22MF = SOURCES
            CodeF22F = -1
            MaleInfo33 = INDIV
            Mar33 = FAM
            SRC33N = SOURCES
            SRC33D = SOURCES
            SRC33M = SOURCES
            CodeF33= -1
            FemelleInfo33 = INDIV
            SRC33NF = SOURCES
            SRC33DF = SOURCES
            SRC33MF = SOURCES
            CodeF33F = -1
            MaleInfo34 = INDIV
            Mar34 = FAM
            SRC34N = SOURCES
            SRC34D = SOURCES
            SRC34M = SOURCES
            CodeF34 = -1
            FemelleInfo34 = INDIV
            SRC34NF = SOURCES
            SRC34DF = SOURCES
            SRC34MF = SOURCES
            CodeF34F = -1
    TABMALE=[]
    TABMALE.append(MaleInfo)
    TABMALE.append(MaleInfo21)
    TABMALE.append(MaleInfo22)
    TABMALE.append(MaleInfo31)
    TABMALE.append(MaleInfo32)
    TABMALE.append(MaleInfo33)
    TABMALE.append(MaleInfo34)
    TABFEMELLE = []
    TABFEMELLE.append(FemelleInfo)
    TABFEMELLE.append(FemelleInfo21)
    TABFEMELLE.append(FemelleInfo22)
    TABFEMELLE.append(FemelleInfo31)
    TABFEMELLE.append(FemelleInfo32)
    TABFEMELLE.append(FemelleInfo33)
    TABFEMELLE.append(FemelleInfo34)
    CodeFMale=[]
    CodeFMale.append(-1)
    CodeFMale.append(CodeF21)
    CodeFMale.append(CodeF22)
    CodeFMale.append(CodeF31)
    CodeFMale.append(CodeF32)
    CodeFMale.append(CodeF33)
    CodeFMale.append(CodeF34)
    CodeFFemale = []
    CodeFFemale.append(-1)
    CodeFFemale.append(CodeF21F)
    CodeFFemale.append(CodeF22F)
    CodeFFemale.append(CodeF31F)
    CodeFFemale.append(CodeF32F)
    CodeFFemale.append(CodeF33F)
    CodeFFemale.append(CodeF34F)
    CodeSRCMaleN = []
    CodeSRCMaleN.append(SRCN)
    CodeSRCMaleN.append(SRC21N)
    CodeSRCMaleN.append(SRC22N)
    CodeSRCMaleN.append(SRC31N)
    CodeSRCMaleN.append(SRC32N)
    CodeSRCMaleN.append(SRC33N)
    CodeSRCMaleN.append(SRC34N)
    CodeSRCFemaleN = []
    CodeSRCFemaleN.append(SRCNF)
    CodeSRCFemaleN.append(SRC21NF)
    CodeSRCFemaleN.append(SRC22NF)
    CodeSRCFemaleN.append(SRC31NF)
    CodeSRCFemaleN.append(SRC32NF)
    CodeSRCFemaleN.append(SRC33NF)
    CodeSRCFemaleN.append(SRC34NF)
    CodeSRCMaleD = []
    CodeSRCMaleD.append(SRCD)
    CodeSRCMaleD.append(SRC21D)
    CodeSRCMaleD.append(SRC22D)
    CodeSRCMaleD.append(SRC31D)
    CodeSRCMaleD.append(SRC32D)
    CodeSRCMaleD.append(SRC33D)
    CodeSRCMaleD.append(SRC34D)
    CodeSRCFemaleD = []
    CodeSRCFemaleD.append(SRCDF)
    CodeSRCFemaleD.append(SRC21DF)
    CodeSRCFemaleD.append(SRC22DF)
    CodeSRCFemaleD.append(SRC31DF)
    CodeSRCFemaleD.append(SRC32DF)
    CodeSRCFemaleD.append(SRC33DF)
    CodeSRCFemaleD.append(SRC34DF)
    CodeSRCMaleM = []
    CodeSRCMaleM.append(SRCM)
    CodeSRCMaleM.append(SRC21M)
    CodeSRCMaleM.append(SRC22M)
    CodeSRCMaleM.append(SRC31M)
    CodeSRCMaleM.append(SRC32M)
    CodeSRCMaleM.append(SRC33M)
    CodeSRCMaleM.append(SRC34M)
    CodeSRCFemaleM = []
    CodeSRCFemaleM.append(SRCMF)
    CodeSRCFemaleM.append(SRC21MF)
    CodeSRCFemaleM.append(SRC22MF)
    CodeSRCFemaleM.append(SRC31MF)
    CodeSRCFemaleM.append(SRC32MF)
    CodeSRCFemaleM.append(SRC33MF)
    CodeSRCFemaleM.append(SRC34MF)
    Mariages=[]
    Mariages.append(Mar)
    Mariages.append(Mar21)
    Mariages.append(Mar22)
    Mariages.append(Mar31)
    Mariages.append(Mar32)
    Mariages.append(Mar33)
    Mariages.append(Mar34)
    return render(request, "affArbre.html", {'Male': TABMALE, 'Femelle': TABFEMELLE, 'Mariage': Mariages, 'EnfListe': EnfListe, \
                                             'CodeF':CodeFMale,'SRCNM':CodeSRCMaleN,'SRCDM':CodeSRCMaleD,'SRCMM':CodeSRCMaleM, \
                                             'CodeFF': CodeFFemale, 'SRCNF': CodeSRCFemaleM, 'SRCDF': CodeSRCFemaleD,
                                             'SRCMF': CodeSRCFemaleM, 'ListeMMar': listeMMar ,'ListeFMar': listeFMar})
