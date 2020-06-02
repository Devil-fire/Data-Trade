#### 目录介绍

+ Client
  + Mine：实现可搜索加密的具体操作
  + AES.py：对AES加密的封装
  + AlgoIfce.py：对可搜索加密的封装
  + MainUi.py：主界面与程序入口的代码
  + tosolc.py：用于处理与智能合约交互的代码
  + choosefile.ui：卖文件时选择文件的界面设计
  + filehash：存储文件关键词与哈希对应关系的文件
  + key：存储客户端私钥的文件

+ Server
  + Mine：实现可搜索加密的具体操作
  + socket_server.py：用于处理外包存储方的代码
  + AlgoIfce.py：对可搜索加密的封装
  + tosolc.py：用于处理与智能合约交互的代码
+ Solidity
  + altbn128.sol
  + main.sol

#### 界面展示

<img src="C:\Users\Devil\AppData\Roaming\Typora\typora-user-images\image-20200526154711937.png" alt="image-20200526154711937" style="zoom:80%;" />

+ 数据搜索
  + 搜索方
    + 在框1中搜索栏输入您想要搜索的数据后按回车即可搜索
    + 检索到数据之后搜索方会弹出付款请求，如果点击yes则会向智能合约付款
    + 收到文件后会提示文件已收到，如果点击yes则会确认收货，将智能合约里的钱给外包存储方和卖方
  + 售卖方
    + 收到数据检索请求后会提示是否允许检索，如果点击yes则会上传rk
    + 用户确认收货后，会提示已经收到钱

+ 数据售卖：点击框2的“卖数据”根据提示选择文件、输入金额和关键词即可

#### 所需环境

python 3，solidity 0.4.2.6

#### 额外引用包

pyqt5,pymysql,pysha3,py_ecc

