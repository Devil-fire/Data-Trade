from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog,QMessageBox
import sys,os,hashlib
import random,string
from PyQt5 import QtWidgets,QtCore
from Crypto.Cipher import AES

    
class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(394, 154)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 40, 131, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 40, 131, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 100, 200, 25))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 394, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.pushButton.clicked.connect(self.encrypt)
        self.pushButton_2.clicked.connect(self.decrypt)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar) 
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AES"))
        self.pushButton.setText(_translate("MainWindow", "加密"))
        self.pushButton_2.setText(_translate("MainWindow", "解密"))
    def encrypt(self):
        key=self.lineEdit.text().encode('utf-8')
        self.lineEdit.clear()
        filename, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*)")
        if(filename!=''):
            f1=open(filename, 'rb')
            if os.path.exists(filename+'.enc'):
                os.remove(filename+'.enc')
            f2=open(filename+'.enc', 'ab')
            iv = ''.join(random.sample(string.ascii_letters + string.digits, 16)).encode('utf-8')
            f2.write(iv)
            data=f1.read(83886080)#10M
            while (data):
                mode = AES.MODE_CFB
                cryptos = AES.new(key, mode, iv)
                cipher_data = cryptos.encrypt(data)
                f2.write(cipher_data)
                data=f1.read(83886080)
        QMessageBox.about(self, "End", "加密完成")
    def decrypt(self):
        key=self.lineEdit.text().encode('utf-8')
        self.lineEdit.clear()
        filename, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*)")
        if(filename!=''):
            f1=open(filename, 'rb')
            index=filename.rfind("/",0,len(filename))
            filename=filename[:index+1]+'new'+filename[index+1:-4]
            if os.path.exists(filename):
                os.remove(filename)
            f2=open(filename, 'ab')
            iv=f1.read(16)
            data=iv
            while (data):
                data=f1.read(83886080)#10M
                mode = AES.MODE_CFB
                cryptos = AES.new(key, mode, iv)
                plain_data = cryptos.decrypt(data)
                f2.write(plain_data)
        QMessageBox.about(self, "End", "解密完成")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

