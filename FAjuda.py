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
        self.contingut=QLabel("Ajuda",self)
        self.contingut.setFont(QFont("Calibri",10))
        self.Omplir()
    #·····································
    def Omplir(self):
        f=open("TextAjuda.txt","r",encoding='utf-8')
        text=f.read()
        f.close()
        self.contingut.setText(text)
    #·····································
    def Close(self):
        self.deleteLater()
#--------------------------------------------------
#--------------------------------------------------
