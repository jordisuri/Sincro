from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import subprocess
import os.path

import ModulSincro
import FAjuda

#--------------------------------------------------
#--------------------------------------------------

from PyQt5 import uic
class FinPpal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('FSincro.ui',self)
        self.setWindowIcon(QIcon("Sincro2.ico"))
        self.resize(720,600)
        self.PrepararWidgets()
        self.Connexions()
        self.CrearAtributs()
    '''
from FSincro import Ui_MainWindow
class FinPpal(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon("Sincro2.ico"))
        self.resize(720,600)
        self.PrepararWidgets()
        self.Connexions()
        self.CrearAtributs()
    '''
    #·····································
    def PrepararWidgets(self):
        self.TAccions.setHorizontalHeaderLabels(("Element","Acció","ts M","ts S"))
        self.TAccions.setColumnWidth(0,350)
        self.TAccions.setColumnWidth(1,50)
        self.TAccions.setColumnWidth(2,145)
        self.TAccions.setColumnWidth(3,145)
        header=self.TAccions.verticalHeader()
        header.setDefaultSectionSize(15)
    #·····································
    def CrearAtributs(self):
        self.topM="D:\\Feina NB\\Altres\\Altres"
        self.topS="J:\\Feina NB\\Altres\\Altres"
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
    # intercanvia Master i Slave
    def InvertirMS(self):
        aux=self.topM
        self.topM=self.topS
        self.topS=aux
        self.EtopM.setText(self.topM)
        self.EtopS.setText(self.topS)
    #·····································
    # Omple la taula amb els elements i accions de la revisió 
    def OmplirTaula(self,accions):
        # omplim amb les accions
        num_files=len(accions)
        self.TAccions.setRowCount(num_files)
        for i in range(len(accions)):
            accio=accions[i]
            cella0=QTableWidgetItem(accio[0])
            cella1=QTableWidgetItem(accio[1])

            cella0.setFlags(cella0.flags() & ~Qt.ItemIsEditable)
            cella1.setFlags(cella1.flags() & ~Qt.ItemIsEditable)
            cella1.setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))

            self.TAccions.setItem(i,0,cella0)
            self.TAccions.setItem(i,1,cella1)
            self.TAccions.item(i,1).setBackground(Qt.green)    # el color indica el permís per realitzar l'acció

            if accio[1][0]=='-':
                self.TAccions.item(i,0).setBackground(QColor(240,240,0))

            if accio[1][0]=='!':
                self.TAccions.item(i,0).setBackground(QColor(240,0,0))

            if accio[1][0]=='*' or accio[1][0]=='!':
                cella2=QTableWidgetItem(accio[2])
                cella3=QTableWidgetItem(accio[3])
                cella2.setFlags(cella2.flags() & ~Qt.ItemIsEditable)
                cella3.setFlags(cella3.flags() & ~Qt.ItemIsEditable)
                self.TAccions.setItem(i,2,cella2)
                self.TAccions.setItem(i,3,cella3)
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
        self.TAccions.clearContents()       # eliminem valors previs
        self.LReady.setText("Revisant...")
        self.DesactivarBotons()
        QApplication.processEvents()
        self.topM=self.EtopM.text()
        self.topS=self.EtopS.text()
        accions_revisar,total_revisats=ModulSincro.Revisar(self.topM,self.topS,self.LReady)
        QApplication.processEvents()
        self.OmplirTaula(accions_revisar)
        self.ActivarBotons()
        self.LReady.setText(f'Fet: {total_revisats:4d} revisats')        
    #·····································
    # fa la sincronització segons el que hi ha indicat en la taula
    def Sincronitzar(self):
        num_accions=self.TAccions.rowCount()
        # comprovació de seguretat
        if num_accions==0:
            self.LReady.setText("No hi ha res per sincronitzar")
            return
        confSinc = QMessageBox.question(self, 'Comprovació', "Vols sincronitzar?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confSinc == QMessageBox.No:
            return
        
        # procedim amb la sincronització
        self.DesactivarBotons()
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
