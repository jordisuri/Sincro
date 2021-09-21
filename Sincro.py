from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import subprocess
import os.path
import time

import ModulSincro
import FAjuda

#--------------------------------------------------
#--------------------------------------------------
'''
# usa el .ui
from PyQt5 import uic
class FinPpal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('FSincro.ui',self)
        self.Continuar__init__()
'''


# usa el ui convertit en classe
from FSincro import Ui_MainWindow
class FinPpal(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Continuar__init__()
    #·····································
    def Continuar__init__(self):
        self.LReady.setText("210921.1740")
        self.setWindowIcon(QIcon("Sincro2.ico"))
        self.resize(744,600)
        self.PrepararWidgets()
        self.Connexions()
        self.CrearAtributs()
    #·····································
    def PrepararWidgets(self):
        self.TAccions.setHorizontalHeaderLabels(("Element","Acció","ts M","ts S"))
        self.TAccions.setColumnWidth(0,370)
        self.TAccions.setColumnWidth(1,50)
        self.TAccions.setColumnWidth(2,140)
        self.TAccions.setColumnWidth(3,140)
        header=self.TAccions.verticalHeader()
        header.setDefaultSectionSize(15)
        
        self.BAturar.setEnabled(False)
    #·····································
    def CrearAtributs(self):
        # les arrels per defecte es troben en les dues primeres
        # línies del fitxer d'ajuda. Per canviar-les cal editar el fitxer
        f=open("TextAjuda.txt","r",encoding='utf-8')
        self.topM=f.readline().strip()
        self.topS=f.readline().strip()
        f.close()
        self.EtopM.setText(self.topM)
        self.EtopS.setText(self.topS)

        self.aturar=False
    #·····································
    def Connexions(self):
        self.BSelM.clicked.connect(self.SeleccionarM)
        self.BSelS.clicked.connect(self.SeleccionarS)
        self.BInvertirMS.clicked.connect(self.InvertirMS)
        
        self.BRev.clicked.connect(self.Revisar)
        self.BSinc.clicked.connect(self.Sincronitzar)
        self.BAturar.clicked.connect(self.Aturar)
        
        self.TAccions.cellClicked.connect(self.CanviAccio)
        self.TAccions.cellDoubleClicked.connect(self.ObrirExplorador)

        hv=self.TAccions.horizontalHeader()
        hv.sectionClicked.connect(self.HeaderClicat)
    #·····································
    def SeleccionarM(self):
        self.topM=QFileDialog.getExistingDirectory(self,"Seleccionar directori Master",".",QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
        self.topM=self.topM.replace('/','\\')   # a Windows no li agraden les /
        self.EtopM.setText(self.topM)
        self.SeleccionarS() ###
    #·····································
    def SeleccionarS(self):
        self.topS=QFileDialog.getExistingDirectory(self,"Seleccionar directori Slave",".",QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
        self.topS=self.topS.replace('/','\\')
        self.EtopS.setText(self.topS)
    #·····································
    # actualitza topM i topS a el que hi ha escrit en el LineEdit, per si
    # l'usuari ho ha sobreescrit (el programa no ho controla i no se n'assebenta
    def ActualitzarTops(self):
        self.topM=self.EtopM.text()
        self.topS=self.EtopS.text()
    #·····································
    # intercanvia Master i Slave
    def InvertirMS(self):
        self.ActualitzarTops()
        aux=self.topM
        self.topM=self.topS
        self.topS=aux
        self.EtopM.setText(self.topM)
        self.EtopS.setText(self.topS)
    #·····································
    # obre l'explorador al M i a l'S a un doble clic de l'element en la taula
    def ObrirExplorador(self,f,c):
        self.TAccions.item(f,c).setSelected(False)
        dnS=self.TAccions.item(f,0).text()
        
        if os.path.exists(dnS):
            if os.path.isfile(dnS):
                dnS=os.path.dirname(dnS)    # només el directori; trec el nom del fitxer
            subprocess.Popen('explorer "'+dnS+'"')
        else:   # si no existeix, obrim el top
            subprocess.Popen('explorer "'+self.topS+'"')
        
        dnM=dnS.replace(self.topS,self.topM)
        if os.path.exists(dnM):
            if os.path.isfile(dnM):
                dnM=os.path.dirname(dnM)    # només el directori
            subprocess.Popen('explorer "'+dnM+'"')
        else:
            subprocess.Popen('explorer "'+self.topM+'"')
    #·····································
    # s'ha clicat un header: ordenar segons aquesta columna
    def HeaderClicat(self,c):
        self.TAccions.sortItems(c)
        self.TAccions.clearSelection()
    #·····································
    # alterna l'activació o desactivació d'una acció
    def CanviAccio(self,f,c):
        self.TAccions.item(f,c).setSelected(False)
        if c==1:
            if self.TAccions.item(f,1).background()==Qt.green:
                self.TAccions.item(f,1).setBackground(Qt.red)      # vermell: acció no permesa
            elif self.TAccions.item(f,1).background()==Qt.red:
                self.TAccions.item(f,1).setBackground(Qt.green)    # verd: acció permesa
            # no permeto canviar de blanc (ja s'ha completat l'acció)
    #·····································
    #·····································
    # revisa el M i l'S
    def Revisar(self):
        self.aturar=False
        self.BAturar.setEnabled(True)
        
        self.ActualitzarTops()              # actualitzem possibles canvis dels tops
        self.DesactivarBotons()
        self.TAccions.clearContents()       # eliminem valors previs de la taula
        self.TAccions.setRowCount(0)
        dif=self.DSBDif.value()             # intèrval de temps per considerar diferents els fitxers
        self.LReady.setText("Revisant...")
        QApplication.processEvents()

        # M->S
        copiarD=[]
        exclosos=[]
        n=0
        itM=os.walk(self.topM)
        for dirM,fillsM,fitxersM in itM:
            n+=len(fillsM)+len(fitxersM)
            dirS=dirM.replace(self.topM,self.topS)
            
            ModulSincro.CompararSubdirsMS(fillsM,dirM,dirS,copiarD,exclosos,self.TAccions)
            if self.aturar:
                break
            ModulSincro.CompararFitxersMS(fitxersM,dirM,dirS,self.topS,self.topM,exclosos,self.TAccions,dif)
            if self.aturar:
                break
            
            self.LReady.setText(f'M->S: {n:4d} revisats')
            QApplication.processEvents()

        # S->M
        esborrarD=[]
        exclosos=[]
        n=0
        itS=os.walk(self.topS)
        for dirS,fillsS,fitxersS in itS:
            n+=len(fillsS)+len(fitxersS)
            dirM=dirS.replace(self.topS,self.topM)
            
            ModulSincro.CompararSubdirsSM(fillsS,dirS,dirM,esborrarD,exclosos,self.TAccions)
            if self.aturar:
                break
            ModulSincro.CompararFitxersSM(fitxersS,dirS,dirM,exclosos,self.TAccions)
            if self.aturar:
                break
            
            self.LReady.setText(f'S->M: {n:4d} revisats')
            QApplication.processEvents()

        self.TAccions.sortItems(0)
        
        self.ActivarBotons()
        self.BAturar.setEnabled(False)
        self.LReady.setText(f'Fet! {n:4d} revisats')
        self.BSinc.setFocus()
        self.Flash()
    #·····································
    # fa la sincronització segons el que hi ha indicat en la taula
    def Sincronitzar(self):
        num_accions=self.TAccions.rowCount()
        # comprovació de seguretat
        if num_accions==0:
            self.LReady.setText("No hi ha res per sincronitzar")
            return
        confSinc=QMessageBox.question(self,'Comprovació',"Vols sincronitzar?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if confSinc==QMessageBox.No:
            return

        # procedim amb la sincronització
        self.aturar=False
        self.BAturar.setEnabled(True)
        self.ActualitzarTops()              # actualitzem possibles canvis dels tops
        self.DesactivarBotons()
        num_accions=self.TAccions.rowCount()
        for f in range(num_accions):
            self.LReady.setText(f'Sincronitzant {f:4d} de {num_accions:4d}')
            QApplication.processEvents()
            if self.TAccions.item(f,1).background()==Qt.green:
                # no permesa si vermell o blanc (ja feta)
                desti=self.TAccions.item(f,0).text()
                accio=self.TAccions.item(f,1).text()
                if accio=='+d':
                    origen=desti.replace(self.topS,self.topM)
                    res_ok=ModulSincro.CopiarDirectori(origen,desti)
                elif accio=='-d':
                    res_ok=ModulSincro.EsborrarDirectori(desti)
                elif accio=='+f' or accio=='*f' or accio=='!f':
                    origen=desti.replace(self.topS,self.topM)
                    res_ok=ModulSincro.CopiarFitxer(origen,desti)
                elif accio=='-f':
                    res_ok=ModulSincro.EsborrarFitxer(desti)
                if res_ok:
                    self.TAccions.item(f,0).setBackground(Qt.white)
                    self.TAccions.item(f,1).setBackground(Qt.white)
            if self.aturar:
                break
        self.ActivarBotons()
        self.BAturar.setEnabled(False)
        self.LReady.setText(f'Llest. {self.TAccions.rowCount():4d} sincronitzats')
        self.BRev.setFocus()
        self.Flash()
    #·····································
    #·····································
    def Aturar(self):
        self.aturar=True
        self.BAturar.setEnabled(False)
        self.LReady.setText(f'Aturat!')
        self.ActivarBotons()
    #·····································
    def DesactivarBotons(self):
        #w.setStyleSheet("background-color: rgb(192,0,0)")
        self.BRev.setEnabled(False)
        self.BSinc.setEnabled(False)
        self.BSelM.setEnabled(False)
        self.BSelS.setEnabled(False)
        self.BInvertirMS.setEnabled(False)
    #·····································
    def ActivarBotons(self):
        #w.setStyleSheet("background-color: rgb(225,225,225)")
        self.BRev.setEnabled(True)
        self.BSinc.setEnabled(True)
        self.BSelM.setEnabled(True)
        self.BSelS.setEnabled(True)
        self.BInvertirMS.setEnabled(True)
    #·····································
    def keyPressEvent(self,e):
        if e.key()==Qt.Key_F1:
            self.fa=FAjuda.FinAjuda()
            self.fa.setWindowModality(Qt.ApplicationModal)
            self.fa.show()
    #·····································
    def resizeEvent(self,e):
        # estiro la columna 0 de la taula per adaptar-la a la mida de la finestra
        nova_mida=e.size().width()
        self.TAccions.setColumnWidth(0,nova_mida-380)
    #·····································
    def Flash(self):
        for i in range(4):
            self.setStyleSheet("background-color: red;")
            QApplication.processEvents()
            time.sleep(.08)
            self.setStyleSheet("background-color: rgb(225,225,225)")
            QApplication.processEvents()
            time.sleep(.15)        
#--------------------------------------------------
#--------------------------------------------------
app=QApplication([])
fp=FinPpal()
fp.show()
app.exec_()
#--------------------------------------------------
#--------------------------------------------------
