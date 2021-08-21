from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import subprocess
import os.path

import ModulSincro
import FAjuda

#--------------------------------------------------
#--------------------------------------------------

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
        '''
    #·····································
    def Continuar__init__(self):
        self.LReady.setText("210819.1000")
        self.setWindowIcon(QIcon("Sincro2.ico"))
        self.resize(720,600)
        self.PrepararWidgets()
        self.Connexions()
        self.CrearAtributs()
    #·····································
    def PrepararWidgets(self):
        self.TAccions.setHorizontalHeaderLabels(("Element","Acció","ts M","ts S"))
        self.TAccions.setColumnWidth(0,350)
        self.TAccions.setColumnWidth(1,50)
        self.TAccions.setColumnWidth(2,170)
        self.TAccions.setColumnWidth(3,170)
        header=self.TAccions.verticalHeader()
        header.setDefaultSectionSize(15)
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
    #·····································
    def Connexions(self):
        self.BSelM.clicked.connect(self.SeleccionarM)
        self.BSelS.clicked.connect(self.SeleccionarS)
        self.BInvertirMS.clicked.connect(self.InvertirMS)
        
        self.BRev.clicked.connect(self.Revisar)
        self.BSinc.clicked.connect(self.Sincronitzar)
        
        self.TAccions.cellClicked.connect(self.CanviAccio)
        self.TAccions.cellDoubleClicked.connect(self.ObrirExplorador)

        hv=self.TAccions.horizontalHeader()
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
        self.ActualitzarTops()              # actualitzem possibles canvis dels tops
        self.DesactivarBotons()
        self.TAccions.clearContents()       # eliminem valors previs de la taula
        self.TAccions.setRowCount(0)
        self.LReady.setText("Revisant...")
        QApplication.processEvents()
        
        #accions_revisar,total_revisats=ModulSincro.Revisar(self.topM,self.topS,self.LReady)
        ModulSincro.ComparacioMS(self.topM,self.topS,self.LReady,self.TAccions)
        ###ModulSincro.ComparacioSM(self.topM,self.topS,self.LReady,self.TAccions)
        
        QApplication.processEvents()
        
        self.ActivarBotons()
        self.LReady.setText(f'Fet:')### {total_revisats:4d} revisats')        
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
        self.ActivarBotons()
        self.LReady.setText(f'Llest. {self.TAccions.rowCount():4d} sincronitzats')
    #·····································
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
#--------------------------------------------------
#--------------------------------------------------
app=QApplication([])
fp=FinPpal()
fp.show()
app.exec_()
#--------------------------------------------------
#--------------------------------------------------
