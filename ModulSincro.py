
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
def CompararSubdirsMS(fillsM,dirM,dirS,copiarD,exclosos,taula):
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
                AfegirAccioTaula(taula,[dS,'+d'])
            exclosos.append(dS) # d'una manera o d'altra, a aquest dir no li hem de mirar els fitxers
#------------------------------------------------------
def CompararFitxersMS(fitxersM,dirM,dirS,topS,topM,copiarF,exclosos,taula):
    fitxersS=[os.path.join(dirS,x) for x in fitxersM] # els que "hauria" de tenir
    for fS in fitxersS:
        if not os.path.exists(fS):
            nom_dir=os.path.dirname(fS)
            if nom_dir not in exclosos:
                # no és a S ni a la llista de dirs exclosos; s'hi ha d'afegir
                copiarF.append([fS,'+f'])    # no hi és; s'ha d'afagir
                AfegirAccioTaula(taula,[fS,'+f'])
        else:
            # és a S; comparem dates
            fM=fS.replace(topS,topM)    # nom sencer del fitxer del Màster
            tsM=os.stat(fM).st_mtime
            tsS=os.stat(fS).st_mtime

            # evito que fitxers iguals al segon (però no a la dècima) siguin considerats diferents
            if tsM!=tsS:
                tsM=round(tsM,2)        # sembla que els segons són dos decimals
                tsS=round(tsS,2)
                
            if tsM>tsS:                 # fM més nou que fS: copiar (actualitzar)
                nom_dir=os.path.dirname(fS)
                if nom_dir not in exclosos:
                    copiarF.append([fS,'*f',DadesTS(tsM),DadesTS(tsS)])
                    AfegirAccioTaula(taula,[fS,'*f',DadesTS(tsM),DadesTS(tsS)])
            elif tsM<tsS:               # fM més vell que fS: copiar (però amb avís)
                nom_dir=os.path.dirname(fS)
                if nom_dir not in exclosos:
                    copiarF.append([fS,'!f',DadesTS(tsM),DadesTS(tsS)])
                    AfegirAccioTaula(taula,[fS,'!f',DadesTS(tsM),DadesTS(tsS)])
            #else tsM==tsS i no cal fer res
#------------------------------------------------------
# compara el M amb el S
def ComparacioMS(topM,topS,etiq,taula):
    copiarD=[]
    copiarF=[]
    exclosos=[]
    n=0
    itM=os.walk(topM)
    for dirM,fillsM,fitxersM in itM:
        n+=len(fillsM)+len(fitxersM)
        dirS=dirM.replace(topM,topS)
        
        CompararSubdirsMS(fillsM,dirM,dirS,copiarD,exclosos,taula)
        print("CS")
        CompararFitxersMS(fitxersM,dirM,dirS,topS,topM,copiarF,exclosos,taula)        
        print("CF")
        
        etiq.setText(f'{n:4d} M->S revisats')
        QApplication.processEvents()
    
'''    
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


def ComparacioMS0(topM,topS,zzz):
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
'''
#------------------------------------------------------
# afegeix una nova acció a la taula
def AfegirAccioTaula(taula,accio):
    i=taula.rowCount()
    taula.insertRow(i)   # afegeix una fila al final
    taula.setRowHeight(i,20)
    cella0=QTableWidgetItem(accio[0])
    cella1=QTableWidgetItem(accio[1])

    cella0.setFlags(cella0.flags() & ~Qt.ItemIsEditable)
    cella1.setFlags(cella1.flags() & ~Qt.ItemIsEditable)
    cella1.setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))

    taula.setItem(i,0,cella0)
    taula.setItem(i,1,cella1)
    taula.item(i,1).setBackground(Qt.green)    # el color indica el permís per realitzar l'acció

    if accio[1][0]=='-':
        taula.item(i,0).setBackground(QColor(240,240,0))

    if accio[1][0]=='!':
        taula.item(i,0).setBackground(QColor(240,0,0))

    if accio[1][0]=='*' or accio[1][0]=='!':
        cella2=QTableWidgetItem(accio[2])
        cella3=QTableWidgetItem(accio[3])
        cella2.setFlags(cella2.flags() & ~Qt.ItemIsEditable)
        cella3.setFlags(cella3.flags() & ~Qt.ItemIsEditable)
        taula.setItem(i,2,cella2)
        taula.setItem(i,3,cella3)
        
    QApplication.processEvents()
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
def ComparacioSM(topM,topS,etiq,taula):
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
        etiq.setText(f'{n:4d} S->M revisats')
        QApplication.processEvents()
    return esborrarD,esborrarF,n
#------------------------------------------------------
#------------------------------------------------------
'''
def Revisar(topM,topS,zzz):
    ComparacioMS(topM,topS,zzz)     # comparació M->S
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
'''
#------------------------------------------------------
#------------------------------------------------------
# accions
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
