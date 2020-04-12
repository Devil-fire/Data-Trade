from socket import *
import struct
import json
import os
import pymysql,hashlib
from multiprocessing import Process,Lock
import threading
from Mine.Scheme import MyScheme
buffsize = 10240
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
    head_struct = c1.recv(4)  # 接收报头的长度,
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
    c1.close()
    print("fileend")
def process_op(lock,c1,c2,addr):
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
        elif(op=='quit'):
            print('quit')
            c1.close()
            break
        elif(op=='file'):
            thread = threading.Thread(target=recv,args=(c2,public,cursor,db))
            thread.start()
        elif('cansearch'):
            if(os.path.exists(public)):
                os.chdir(public)
    print('close')

if __name__ == '__main__':
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
    while True:
        c1,addr = s.accept()
        print ('连接地址：', c1)
        c2,addr = fi.accept()
        print ('连接地址：', c2)
        p = Process(target=process_op, args=(lock,c1,c2,addr))
        p.start()
        c1.close()
        c2.close()