
# ModulSincro.py

'''
M màster, S esclau.

COMPARACIÓ M->S

Fills
- E(dM), no E(dS)
    · copiar dM->dS
    · ignorar fills de dM
- E(dM), E(dS)
    · no fer res

Fitxers
- E(fM), no E(fS)
    · copiar fM->fS

- E(fM), E(fS)
    if data(fM)<data(fS) # fM més vell que fS
        · copiar fM->fS
        · avisar sobreescriptura fS
    if data(fM)>data(fS) # fM més nou que fS
        · copiar fM->fS
    if data(fM)=data(fS)
        · no fer res


COMPARACIÓ S->M

Fills
- E(dS), no E(dM)
    · esborrar dS

Fitxers
- E(fS), no E(fM)
    · esborrar fS
- E(fS), E(fM)
    · ja tractat, no fer res
'''
#------------------------------------------------------
import os        # walk, unlink
import os.path   # join, normpath
import shutil    # rmtree, copytree, copy2
import datetime  # datetime, utcfromtimestamp, strftime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#------------------------------------------------------
def DadesTS(ts):
    # mostra de manera entenedora un timestamping
    # NO USAT
    dt = datetime.datetime.utcfromtimestamp(ts)
    return dt.strftime('%Y-%m-%d %H:%M:%S')
#------------------------------------------------------
# Master -> Slave
#------------------------------------------------------
def CompararFillsMS(fillsM,dirM,dirS,copiarD,exclosos):
    fillsS=[os.path.join(dirS,x) for x in fillsM] # els que "hauria" de tenir
    for dS in fillsS:
        if not os.path.exists(dS):
            # cal copiar dS, però només si no hi ha un seu antecessor (que ja es copiarà)
            trobat=False
            for d in copiarD:
                if d in dS:  # comprovem si d és un antecessor
                    trobat=True
            if not trobat:
                copiarD.append(dS)
            exclosos.append(dS) # d'una manera o d'altra, a aquest dir no li hem de mirar els fitxers
#------------------------------------------------------
def CompararFitxersMS(fitxersM,dirM,dirS,topS,topM,copiarF,exclosos):
    fitxersS=[os.path.join(dirS,x) for x in fitxersM] # els que "hauria" de tenir
    for fS in fitxersS:
        if not os.path.exists(fS):
            nom_dir=os.path.dirname(fS)
            if nom_dir not in exclosos:
                # no és a S ni a la llista de dirs exclosos; s'hi ha d'afegir
                copiarF.append([fS,'+f'])    # no hi és; s'ha d'afagir
        else:
            # és a S; comparem dates
            fM=fS.replace(topS,topM)    # nom sencer del fitxer del Màster
            tsM=os.stat(fM).st_mtime
            tsS=os.stat(fS).st_mtime
            if tsM>tsS:                 # fM més nou que fS: copiar (actualitzar)
                nom_dir=os.path.dirname(fS)
                if nom_dir not in exclosos:
                    copiarF.append([fS,'*f',DadesTS(tsM),DadesTS(tsS)])
            elif tsM<tsS:               # fM més vell que fS: copiar (però amb avís)
                nom_dir=os.path.dirname(fS)
                if nom_dir not in exclosos:
                    copiarF.append([fS,'!f',DadesTS(tsM),DadesTS(tsS)])
            #else tsM==tsS i no cal fer res
#------------------------------------------------------
# compara el M amb el S
def ComparacioMS(topM,topS,zzz):
    copiarD=[]
    copiarF=[]
    exclosos=[]
    n=0
    itM=os.walk(topM)
    for dirM,fillsM,fitxersM in itM:
        n+=len(fillsM)+len(fitxersM)
        dirS=dirM.replace(topM,topS)
        CompararFillsMS(fillsM,dirM,dirS,copiarD,exclosos)
        CompararFitxersMS(fitxersM,dirM,dirS,topS,topM,copiarF,exclosos)
        zzz.setText(f'{n:4d} M->S revisats')
        QApplication.processEvents()
    return copiarD,copiarF,n
#------------------------------------------------------
#------------------------------------------------------
# Slave -> Master
#------------------------------------------------------
#------------------------------------------------------
def CompararFillsSM(fillsS,dirS,dirM,esborrarD,exclosos):
    for dS in fillsS:               # recorrem els fills en S (dS és només el nom, sense el path)
        dM=os.path.join(dirM,dS)    # generem els equivalents en M
        if not os.path.exists(dM):  # l'equivalent en M no existeix: s'ha d'eliminar el d'S
            # comprovem que no s'hagi marcat per eliminar un antrcessor seu (que ja s'eliminarà)
            dS2=os.path.join(dirS,dS)
            trobat=False
            for d in esborrarD:
                if d in dS2:        # comprovem si d és un antecessor
                    trobat=True
            if not trobat:
                esborrarD.append(dS2)
            exclosos.append(dS2)
#------------------------------------------------------
def CompararFitxersSM(fitxersS,dirS,dirM,esborrarF,exclosos):
    for fS in fitxersS:
        fM=os.path.join(dirM,fS)
        if not os.path.exists(fM):
            fS=os.path.join(dirS,fS)
            if dirS not in exclosos:
                # no és a M ni a la llista de dirs exclosos; s'hi ha d'afegir
                esborrarF.append(fS)    # no hi és; s'ha d'afagir
        # else:   existeix a ambdós llocs: ja tractat en el cas M->S i no cal fer res
#------------------------------------------------------
def ComparacioSM(topS,topM,zzz):
    esborrarD=[]
    esborrarF=[]
    exclosos=[]
    n=0
    itS=os.walk(topS)
    for dirS,fillsS,fitxersS in itS:
        n+=len(fillsS)+len(fitxersS)
        dirM=dirS.replace(topS,topM)
        CompararFillsSM(fillsS,dirS,dirM,esborrarD,exclosos)
        CompararFitxersSM(fitxersS,dirS,dirM,esborrarF,exclosos)
        zzz.setText(f'{n:4d} S->M revisats')
        QApplication.processEvents()
    return esborrarD,esborrarF,n
#------------------------------------------------------
#------------------------------------------------------
def Revisar(topM,topS,zzz):
    copiarD,copiarF,n1=ComparacioMS(topM,topS,zzz)     # comparació M->S
    esborrarD,esborrarF,n2=ComparacioSM(topS,topM,zzz) # comparació S->M
    
    accions=[]
    for c in copiarD:
        accions.append([c,'+d'])
    for c in copiarF:
        accions.append(c)
    for c in esborrarD:
        accions.append([c,'-d'])
    for c in esborrarF:
        accions.append([c,'-f'])
    accions.sort()
    return accions,n1+n2
#------------------------------------------------------
#------------------------------------------------------
# realització d'accions
#------------------------------------------------------
#------------------------------------------------------
def CopiarDirectori(origen,desti):
    try:
        shutil.copytree(origen,desti)
        return True
    except:
        return False
#------------------------------------------------------
def EsborrarDirectori(desti):
    try:
        shutil.rmtree(desti)
        return True
    except:
        return False
#------------------------------------------------------
def CopiarFitxer(origen,desti):
    try:
        shutil.copy2(origen,desti)
        return True
    except:
        return False
#------------------------------------------------------
def EsborrarFitxer(desti):
    try:
        os.unlink(desti)
        return True
    except:
        return False
#------------------------------------------------------
#------------------------------------------------------
if __name__=="__main__":
    # M és el màster, S és l'esclau
##    topM=os.path.normpath(".\X1\Z")
##    topS=os.path.normpath(".\X2\Z")
    topM=os.path.normpath("C:/Users/70175/Desktop/Sincro/X1/Z")
    topS=os.path.normpath("C:/Users/70175/Desktop/Sincro/X2/Z")

    # comparació M->S
    copiarD,copiarF=ComparacioMS(topM,topS)
    print("copiarD",copiarD)
    print("copiarF",copiarF)

    print("**************************************")

    # comparació S->M
    esborrarD,esborrarF=ComparacioSM(topS,topM)
    print("esborrarD",esborrarD)
    print("esborrarF",esborrarF)

    accions=[]
    for c in copiarD:
        accions.append([c,'+d'])
    for c in copiarF:
        accions.append(c)
    for c in esborrarD:
        accions.append([c,'-d'])
    for c in esborrarF:
        accions.append([c,'-f'])
    print(accions)
    accions.sort()
    print(accions)
#------------------------------------------------------
