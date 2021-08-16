from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
            
#--------------------------------------------------
#--------------------------------------------------
class FinAjuda(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajuda")
        self.resize(600,400)
        
        self.contingut=QTextEdit(self)
        self.contingut.setReadOnly(True)
        self.contingut.setCurrentFont(QFont("Calibri",12))
        hbl=QHBoxLayout(self)
        hbl.addWidget(self.contingut)
        self.setLayout(hbl)
        
        self.Omplir()
    #·····································
    def Omplir(self):
        f=open("TextAjuda.txt","r",encoding='utf-8')
        f.readline()
        f.readline()
        text=f.read()
        f.close()
        self.contingut.setText(text)
    #·····································
    def Close(self):
        self.deleteLater()
#--------------------------------------------------
#--------------------------------------------------
