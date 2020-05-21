from socket import *
import struct
import json
import os,time
import pymysql,hashlib,py_ecc
from py_ecc import bn128 as bn
from multiprocessing import Process, Lock, Manager, Value
import threading
from Mine.Scheme import MyScheme
from Mine.Entity import Key,PriKey,PubKey,TrapKey,CipherII,ReKey,Token
import tosolc
from ctypes import c_char_p
buffsize = 10240
class wanttosend:
    wanttosend=''

wanttosend = wanttosend()
sch = MyScheme()
def check(currentAccount, currentPassword,sharestr,cipheri,send_filename):
    db = pymysql.connect(host='123.56.160.68', port=3306, user='root', passwd='123456', db='data-trade', charset='utf8')
    cursor = db.cursor()
    Contract1 = tosolc.getContract(tosolc.contract1_abi, "0xC6605fd9F15DbF27A115e74C0E94Ebc1ED2eE376")
    print(currentAccount,currentPassword)
    amount = int(tosolc.getAmount(Contract1, currentAccount, currentPassword)) #获取有多少个子合约
    record = amount
    search_filename = ''
    while(True):
        Contract1 = tosolc.getContract(tosolc.contract1_abi, "0xC6605fd9F15DbF27A115e74C0E94Ebc1ED2eE376")
        print(currentAccount,currentPassword)
        amount = int(tosolc.getAmount(Contract1, currentAccount, currentPassword)) #获取有多少个子合约
        print(amount)
        if(amount > record  and amount > 0):
            Contract2Address = tosolc.getProjects(Contract1, currentAccount, currentPassword)[amount-1]
            print(Contract2Address)
            Contract2 = tosolc.getContract(tosolc.contract2_abi, Contract2Address)
            state = tosolc.getState(Contract2)
            print("state: " + str(state))
            if(int(state)==2):
                record = amount
                Tw = tosolc.getTrapdoor(Contract2, currentAccount, currentPassword)
                Tw_1 = (py_ecc.fields.bn128_FQ(int(Tw[0])),py_ecc.fields.bn128_FQ(int(Tw[1])))
                Tw_2 = (py_ecc.fields.bn128_FQ(int(Tw[2])),py_ecc.fields.bn128_FQ(int(Tw[3])))
                Tw = TrapKey((py_ecc.fields.bn128_FQ2(Tw_1),py_ecc.fields.bn128_FQ2(Tw_2)))
                rk = tosolc.getReKey(Contract2, currentAccount, currentPassword)
                #print(rk)
                rk = ReKey((py_ecc.fields.bn128_FQ(int(rk[0])),py_ecc.fields.bn128_FQ(int(rk[1]))))
                sql = "select user,filename,price,cipherii1,cipherii2,cipherii3,cipherii4,cipherii5 from filerecord"
                cursor.execute(sql)
                data = cursor.fetchall()
                for i in range(0, len(data)):
                    search_filename = data[i][0]
                    for j in range(3, 7):
                        if(data[i][j] != None):
                            cipherii = strtocipherii(data[i][j])
                            reth = sch.Search(cipherii, Tw, rk)
                            print(reth)
                            if(reth):
                                params = []
                                params.append(sch.hashfromCipherII(cipherii))
                                print(sch.hashfromCipherII(cipherii))
                                params.append(int(data[i][2]))
                                tosolc.searchDone(Contract2, currentAccount, currentPassword, params)
                                state = tosolc.getState(Contract2)
                                while(int(state)!=4):
                                    state = tosolc.getState(Contract2)
                                    time.sleep(2)
                                if(int(state)==4):
                                    tk = tosolc.getToken(Contract2, currentAccount, currentPassword)
                                    tk_1=(py_ecc.fields.bn128_FQ(int(tk[0])),py_ecc.fields.bn128_FQ(int(tk[1])))
                                    tk_2=(py_ecc.fields.bn128_FQ(int(tk[2])),py_ecc.fields.bn128_FQ(int(tk[3])))
                                    tk=Token((py_ecc.fields.bn128_FQ2(tk_1),py_ecc.fields.bn128_FQ2(tk_2)))
                                    cipheri_u = sch.ReEnc(cipherii, rk, tk)
                                    cipheri_list = list(map(int, str(cipheri_u).replace(')','').replace('(','').replace(',','').split(' ')))
                                    tosolc.sendc1(Contract2, currentAccount, currentPassword, cipheri_list[0:2])
                                    tosolc.sendc2(Contract2, currentAccount, currentPassword, cipheri_list[2:6])
                                    tosolc.sendc3(Contract2, currentAccount, currentPassword, cipheri_list[6:18])
                                    tosolc.sendc4(Contract2, currentAccount, currentPassword, cipheri_list[18:])
                                    #tosolc.getMoney(Contract2, currentAccount, currentPassword)
                                    sharestr.value = str(tosolc.getPubkey(Contract2, currentAccount, currentPassword))
                                    cipheri.value = str(cipheri_u)
                                    send_filename.value = str(data[i][1])
        time.sleep(1)

def strtocipherii(str):
    list=str.split('\n')
    list_c1=list[0][5:-1].split(',')
    c1=(py_ecc.fields.bn128_FQ(int(list_c1[0])),py_ecc.fields.bn128_FQ(int(list_c1[1])))
    list_c2=list[1][6:-1].split(')')
    list_c21=list_c2[0].split(',')
    list_c22=list_c2[1][3:].split(',')
    c2_1=(py_ecc.fields.bn128_FQ(int(list_c21[0])),py_ecc.fields.bn128_FQ(int(list_c21[1])))
    c2_2=(py_ecc.fields.bn128_FQ(int(list_c22[0])),py_ecc.fields.bn128_FQ(int(list_c22[1])))
    c2=(py_ecc.fields.bn128_FQ2(c2_1),py_ecc.fields.bn128_FQ2(c2_2))
    list_c3=list[2][5:-1].split(',')
    list_c3=[int(i) for i in list_c3]
    c3=bn.FQ12(list_c3)
    cipherii=CipherII(c1,c2,c3)
    return cipherii

def recv(c1,public,cursor,db):
    head_struct = c1.recv(4)  # 接收报头的长度
    if head_struct:
        print('已连接,等待接收数据')
    head_len = struct.unpack('i', head_struct)[0]  # 解析出报头的字符串大小
    data = c1.recv(head_len)  # 接收长度为head_len的报头内容的信息 (包含文件大小,文件名的内容)
    head_dir = json.loads(data.decode('utf-8'))
    filesize_b = head_dir['filesize_bytes']
    filename = head_dir['filename']
    price = head_dir['price']
    keyword_len = int(head_dir['keyword_len'])
    name = hashlib.md5(public.encode("utf-8")).hexdigest()
    if(not os.path.exists(os.getcwd()+'\\'+name)):
        os.mkdir(os.getcwd()+'\\'+name)
    sql = "select user,filename from filerecord where user = '{0}' and filename = '{1}'".format(public,filename)
    cursor.execute(sql)
    data = cursor.fetchone()
    if(data == None):
        sql = "insert into filerecord(user,filename,cipherii_len,price) values ('{0}','{1}','{2}','{3}')"\
            .format(public,filename,keyword_len,price)
        cursor.execute(sql)
        db.commit()
    for i in range(0,keyword_len):
        sql = " update filerecord set {0} = '{1}' where user = '{2}' and filename = '{3}'"\
            .format('cipherii'+str(i+1),c1.recv(2048).decode('utf-8'),public,filename)
        cursor.execute(sql)
        db.commit()
    recv_len = 0
    recv_mesg = b''
    if(os.path.exists(os.getcwd()+'\\'+name+'\\'+filename)):
        os.remove(os.getcwd()+'\\'+name+'\\'+filename)

    f = open(os.getcwd()+'\\'+name+'\\'+filename, 'ab+')
    print(filesize_b)
    while recv_len < filesize_b:
        percent = recv_len / filesize_b
        if filesize_b - recv_len > buffsize:
            recv_mesg = c1.recv(buffsize)
            f.write(recv_mesg)
            recv_len += len(recv_mesg)
        else:
            recv_mesg = c1.recv(filesize_b - recv_len)
            recv_len += len(recv_mesg)
            f.write(recv_mesg)
    f.close()
    #c1.close()
    print("fileend")
def send_cipherifile(c1,c2,public,sharestr,cipheri,send_filename):
    while(True):
        #print(public[1:-1])
        if(public[1:-1]==sharestr.value[1:-1]):
            print(type(c1))
            c1.send(cipheri.value.encode('utf-8'))

            name = hashlib.md5(public.encode("utf-8")).hexdigest()
            fileName = send_filename.value
            filesize_bytes = os.path.getsize(os.getcwd()+'\\'+name+'\\'+fileName)
            dirc = {
                'filename': fileName,
                'filesize_bytes': filesize_bytes
            }
            head_info = json.dumps(dirc)
            head_info_len = struct.pack('i', len(head_info))
            c2.send(head_info_len)
            c2.send(head_info.encode('utf-8'))
            f=open(os.getcwd()+'\\'+name+'\\'+fileName,'rb')
            data=f.read(83886080)
            while data:
                c2.sendall(data)
                data=f.read(83886080)
            break
        time.sleep(5)
def process_op(lock,c1,c2,addr,sharestr,cipheri,send_filename):
    public=''
    db = pymysql.connect(host='123.56.160.68', port=3306, user='root', passwd='123456', db='data-trade', charset='utf8')
    cursor = db.cursor()
    while True:
        op=c1.recv(1024).decode('utf-8')
        print(op)
        print(op.find('login',0,len(op))!=-1)
        if(op.find('login',0,len(op))!=-1):
            public = op[len('login'):]
            sql = "select public from info where public = '{0}'".format(public)
            cursor.execute(sql)
            data = cursor.fetchone()
            if(data==None):
                sql = "insert into info(public) values ('{0}')".format(public)
                cursor.execute(sql)
                db.commit()
            thread = threading.Thread(target=send_cipherifile,args=(c1,c2,public,sharestr,cipheri,send_filename))
            thread.start()
        elif(op=='quit'):
            print('quit')
            c1.close()
            c2.close()
            break
        elif(op=='file'):
            thread = threading.Thread(target=recv,args=(c2,public,cursor,db))
            thread.start()
        elif('cansearch'):
            if(os.path.exists(public)):
                os.chdir(public)
    print('close')

if __name__ == '__main__':
    manager = Manager()
    sharestr=manager.Value(c_char_p,'')
    cipheri=manager.Value(c_char_p,'')
    send_filename = manager.Value(c_char_p,'')

    currentAccount, currentPassword = tosolc.setAccount(tosolc.xzb_ad, tosolc.xzb_sk)
    lock = Lock()
    s = socket(AF_INET, SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888
    s.bind((host, port))
    s.listen(5)
    fi = socket(AF_INET, SOCK_STREAM)
    port = 9999
    fi.bind((host, port))
    fi.listen(5)
    thread = threading.Thread(target=check,args=(currentAccount, currentPassword,sharestr,cipheri,send_filename))
    thread.start()
    while True:
        c1,addr = s.accept()
        print ('连接地址：', c1)
        c2,addr = fi.accept()
        print ('连接地址：', c2)
        p = Process(target=process_op, args=(lock,c1,c2,addr,sharestr,cipheri,send_filename))
        p.start()
        c1.close()
        c2.close()