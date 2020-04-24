# coding:utf-8

from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import QThread,pyqtSignal
import sys,json,struct,os,time
import qtawesome
from PyQt5.uic import loadUi
import threading,socket
from AES import keygen,encrypt,decrypt,ivgen
from Mine.Scheme import MyScheme
from Mine.Entity import Key,PriKey
import tosolc
from web3.auto import w3

sch = MyScheme()
class Thread_1(QThread):
    signal = pyqtSignal()
    def __init__(self,currentAccount,currentPassword):
        super().__init__()
        self.currentAccount = currentAccount
        self.currentPassword = currentPassword
        self.record = 0
    def run(self):
        while(True):
            Contract1 = tosolc.getContract(tosolc.contract1_abi, "0x54114cEb519710ADb10778c0FE1DB774dA92A05A")
            print(self.currentAccount,self.currentPassword)
            amount = int(tosolc.getAmount(Contract1, self.currentAccount, self.currentPassword)) #获取有多少个子合约
            print(amount)
            if(amount > self.record):
                self.record = amount
                Contract2Address = tosolc.getProjects(Contract1, self.currentAccount, self.currentPassword)[amount-1]
                self.Contract2 = tosolc.getContract(tosolc.contract2_abi, Contract2Address)
                state = tosolc.getState(self.Contract2)
                print("state: " + str(state))
                if(int(state)==1):
                    self.signal.emit()
            time.sleep(5)

class MainUi(QtWidgets.QMainWindow):
    def __init__(self, s1, s2):
        super().__init__()
        self.s1 = s1
        self.s2 = s2
        self.init_ui()
    def box(self):
        reply = QMessageBox.information(self,"检测到搜索请求", "xxx发起了关于xxx的搜索", QMessageBox.Yes | QMessageBox.No)
        if(reply == QMessageBox.Yes):
            print(self.thread_1.Contract2)
            rk = sch.ReKeyGen(keyB.pubkey, key_pres.prikey)
            #permitSearch(Contract2, self.currentAccount, self.currentPassword, params)
            #TODO:拿到买方pubkey计算rk

    def init_ui(self):
        global key_pres
        self.currentAccount, self.currentPassword = tosolc.setAccount(w3.eth.accounts[0], 123456)

        if(not os.path.exists(os.getcwd()+'\\'+'key')):
            with open(os.getcwd()+'\\'+'key', 'w') as f:
                key_pres = sch.KeyGen()
                f.write(str(key_pres))
        else:
            with open(os.getcwd()+'\\'+'key', 'r') as f:
                f.readline()
                f.readline()
                f.readline()
                prikey = int(f.readline()[3:])
                key_pres = Key(PriKey(prikey))
        self.s1.send(('login'+str(key_pres.pubkey)).encode('utf-8'))
        self.setFixedSize(960,700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')
        self.left_close = QtWidgets.QPushButton("") # 关闭按钮
        self.left_close.clicked.connect(self.close)
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        'self.left_close.clicked.connect(self.showMinimized)'
        self.left_label_1 = QtWidgets.QPushButton("每日推荐")
        self.left_label_1.setObjectName('left_label')
        '''self.left_label_2 = QtWidgets.QPushButton("我的音乐")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')'''
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.music',color='white'),"卖数据")
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.clicked.connect(self.selldata)
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment',color='white'),"反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_7.clicked.connect(self.message_question)
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_8.clicked.connect(self.message_contact)
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question',color='white'),"遇到问题")
        self.left_button_9.setObjectName('left_button')
        self.left_button_9.clicked.connect(self.message_bug)
        self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_close, 0, 0,1,1)
        self.left_layout.addWidget(self.left_mini, 0, 1,1,1)
        self.left_layout.addWidget(self.left_label_1,1,0,1,3)
        self.left_layout.addWidget(self.left_button_1, 2, 0,1,3)
        self.left_layout.addWidget(self.left_button_7, 10, 0,1,3)
        self.left_layout.addWidget(self.left_button_8, 11, 0,1,3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1,3)
        self.left_close.setFixedSize(15,15) # 设置关闭按钮的大小
        self.left_mini.setFixedSize(15, 15) # 设置最小化按钮大小
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格
        self.right_bar_widget = QtWidgets.QWidget() # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout() # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' '+'搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入您想要查找的关键词")
        self.right_bar_widget_search_input.returnPressed.connect(self.search)
        self.right_bar_widget_search_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.right_bar_layout.addWidget(self.search_icon,0,0,1,1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input,0,1,1,8)

        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.setHorizontalHeaderLabels(['卖方', '文件大小', '价格'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.right_layout.addWidget(self.tableWidget, 1, 0, 5, 9)

        self.right_layout.addWidget(self.right_recommend_widget, 1, 0, 2, 9)
        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        self.setWindowOpacity(0.95) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隐藏边框
        self.main_layout.setSpacing(0)
        self.thread_1 = Thread_1(self.currentAccount,self.currentPassword)
        self.thread_1.signal.connect(self.box)
        self.thread_1.start()
    def addrow(self, item_name,item_size, item_price):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        item_name.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        item_name.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item_price.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        item_price.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(row, 0, item_name)
        self.tableWidget.setItem(row, 1, item_size)
        self.tableWidget.setItem(row, 2, item_price)
    def closeEvent(self, event):
        self.s1.send('quit'.encode('utf-8'))
        self.s1.close()
        self.s2.close()
        self.close()
    def selldata(self):
        self.ChooseFile = ChooseFileWindow(self.s1, self.s2)
        self.ChooseFile.show()
    def search(self):
        thread = threading.Thread(target=self.search_impl, name=None,  args=())
        thread.start()   
    def message_question(self):
        QMessageBox.about(self, "反馈问题", "不行，我没有问题，不能反馈")
    def message_contact(self):
        QMessageBox.about(self, "联系我们", "不告诉你，不联系")
    def message_bug(self):
        QMessageBox.about(self, "反馈bug", "不行，我没有bug，不能反馈")
    def search_impl(self):
        Tw = sch.Trapdoor(key_pres.prikey, self.right_bar_widget_search_input.text())
        param=list(map(int, str(key_pres.pubkey).replace(')','').replace('(','').replace(',','').split(' ')))
        Tw = list(map(int, str(Tw).replace(')','').replace('(','').replace(',','').split(' ')))
        param = param + Tw
        #TODO:把Tw放在智能合约
        Contract1 = tosolc.getContract(tosolc.contract1_abi, "0x54114cEb519710ADb10778c0FE1DB774dA92A05A")
        print(param)
        tosolc.createProject(Contract1, self.currentAccount, self.currentPassword, param) #发送请求并创建子合约

def send_data(s1,s2,fileName,value,keyword1,keyword2,keyword3,keyword4,keyword5):
    thread = threading.Thread(target=send_data_impl, name=None,  args=(s1,s2,fileName,value,keyword1,keyword2,keyword3,keyword4,keyword5)) 
    thread.start() 
def send_data_impl(s1,s2,fileName,value,keyword1,keyword2,keyword3,keyword4,keyword5):
    s1.send('file'.encode('utf-8'))
    key=keygen('AES-128')
    keyword_list=[]
    if keyword1!='':
        keyword_list.append(keyword1)
    if keyword2!='':
        keyword_list.append(keyword2)
    if keyword3!='':
        keyword_list.append(keyword3)
    if keyword4!='':
        keyword_list.append(keyword4)
    if keyword5!='':
        keyword_list.append(keyword5)
    filesize_bytes = os.path.getsize(fileName) + 16
    dirc = {
        'filename': 'enc'+fileName[fileName.rfind("/",0,len(fileName))+1:],
        'filesize_bytes': filesize_bytes,
        'price': value,
        'keyword_len': str(len(keyword_list)),
    }
    head_info = json.dumps(dirc)
    head_info_len = struct.pack('i', len(head_info))
    s2.send(head_info_len)
    s2.send(head_info.encode('utf-8'))
    print(key_pres)
    for i in range(0,len(keyword_list)):
        cipherii, srecord = sch.Enc(key_pres.pubkey, key, keyword_list[i])
        s2.send(str(cipherii).encode('utf-8'))
    iv=ivgen()
    f=open(fileName,'rb')
    s2.send(iv)
    data=f.read(83886080)
    key=key.encode('utf-8')
    while data:
        cipher_data = encrypt(data,key,iv)
        print(len(cipher_data))
        s2.sendall(cipher_data)
        data=f.read(83886080)
    s2.close()

class ChooseFileWindow(QWidget):
    def __init__(self,s1,s2):
        super(ChooseFileWindow, self).__init__()
        loadUi("choosefile.ui", self)
        self.setWindowTitle("文件选择")
        self.s1 = s1
        self.s2 = s2
        self.fileName=''
        self.choosefile_button.clicked.connect(self.choose_callback)
        self.button.clicked.connect(self.quit)
    def choose_callback(self):
        self.fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*)")
        if(self.fileName!=''):
            self.lineEdit_2.setText(self.fileName)
    def quit(self):
        if(self.fileName!='' and self.lineEdit.text()!='' and self.lineEdit.text().isdigit()):
            send_data(self.s1,self.s2,self.fileName,self.lineEdit.text(),self.lineEdit_3.text(),self.lineEdit_4.text(),\
                self.lineEdit_5.text(),self.lineEdit_6.text(),self.lineEdit_7.text())
            self.close()
        elif(self.fileName==''):
            QMessageBox.about(self, "", "您未选择文件")
        elif(self.lineEdit.text()==''):
            QMessageBox.about(self, "", "未输入价格")
        elif(not self.lineEdit.text().isdigit()):
            QMessageBox.about(self, "", "价格格式错误（请输入数字）")
        

def main():
    s1 = socket.socket()
    host = "127.0.0.1"
    port = 8888
    s1.connect((host, port))
    port = 9999
    s2 = socket.socket()
    s2.connect((host, port))
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi(s1, s2)
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()