# coding=utf-8


# log目录名称
DIR_NAME = "./Log"

class LOGClass():
    def __init__(self):
        print("__init__", self)

    def __del__(self):
        print("__del__", self)