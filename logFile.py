# coding=utf-8

import os
# log目录名称
DIR_NAME = "./Log"

class LOGClass():

    fileHandle = None

    def __init__(self, fileName:str):
        print("__init__", self)
        self.fileHandle = self.log_file_open(fileName)

    def __del__(self):
        print("__del__", self)

    # 创建or打开log文件 
    def log_file_open(self, fileName:str):

        # 判断目录是否存在
        if os.path.isdir(DIR_NAME) == False:
            os.mkdir(DIR_NAME)
            print("目录不存在，创建目录:" + DIR_NAME)

        #print(time_str)
        print("fileName:", fileName)
        # 追加的方式打开文件
        return(open(DIR_NAME + "/" + fileName+ ".csv", "a"))   

    def log_file_write(self, strData:str):
        
        self.fileHandle.writelines(strData)   
        self.fileHandle.flush()
        self.fileHandle.close() 