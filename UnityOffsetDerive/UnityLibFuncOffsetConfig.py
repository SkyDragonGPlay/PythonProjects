#coding:utf-8

import ConfigParser, os

class UnityLibFuncOffsetConfig:
    
    __unityLibFuncOffsetDic__ = {}
    __cf__ = ConfigParser.ConfigParser()
    
    def __init__(self):

        if not os.path.isfile('UnityLibConfig.ini'):
            f = open(os.getcwd() + "/UnityLibConfig.ini", "w")
            f.close()

        self.__cf__.read('UnityLibConfig.ini')
        
        for section in self.__cf__.sections():
            funcOffset = UnityLibFuncOffset()
            self.__unityLibFuncOffsetDic__[section] = funcOffset.init(self.__cf__, section)
        
    # get item with unity version
    def get(self, unityVersion):
        result = None
        if self.__unityLibFuncOffsetDic__.has_key(unityVersion):
            result = self.__unityLibFuncOffsetDic__[unityVersion]
        return result

    # get empty items
    def getEmptyVers(self):
        emptyVers = []
        for k, v in self.__unityLibFuncOffsetDic__.items():
            if v.JNI_OnLoad_Addr == 0:
                emptyVers.append(k)
        return emptyVers

    # set item to dictionary
    def setFuncOffset(self, funcOffset):
        self.__unityLibFuncOffsetDic__[funcOffset.unityVersion] = funcOffset


    # save to config file
    def save(self):
        for k, v in self.__unityLibFuncOffsetDic__.items():
            self.__cf__.add_section(k)
            self.__cf__.set(k, "JNI_OnLoad_Addr", v.JNI_OnLoad_Addr_STR)
            self.__cf__.set(k, "UnitySendMessage_Addr", v.UnitySendMessage_Addr_STR)
            self.__cf__.set(k, "apkOpen_Addr", v.apkOpen_Addr_STR)
            self.__cf__.set(k, "IsFileCreated_Addr", v.IsFileCreated_Addr_STR)
            self.__cf__.set(k, "WWW_Create_Addr", v.WWWCreate_Addr_STR)

        self.__cf__.write(open(os.getcwd() + "/UnityLibConfig.ini", "w"))
        return

class UnityLibFuncOffset:

    def __init__(self):
        self.JNI_OnLoad_Addr = 0
        self.UnitySendMessage_Addr = 0
        self.apkOpen_Addr = 0
        self.IsFileCreated_Addr = 0
        
        self.JNI_OnLoad_Addr_STR = ""
        self.UnitySendMessage_Addr_STR = ""
        self.apkOpen_Addr_STR = ""
        self.IsFileCreated_Addr_STR = ""
        self.WWWCreate_Addr_STR = ""


    def init(self, configParser, unityVersion):
        self.unityVersion = unityVersion

        if configParser.get(unityVersion, 'JNI_OnLoad_Addr') == "0x":
            self.JNI_OnLoad_Addr = 0
            self.UnitySendMessage_Addr = 0
            self.apkOpen_Addr = 0
            self.IsFileCreated_Addr = 0
        else:
            self.JNI_OnLoad_Addr = str(int(configParser.get(unityVersion, 'JNI_OnLoad_Addr'), 16))
            self.UnitySendMessage_Addr = str(int(configParser.get(unityVersion, 'UnitySendMessage_Addr'), 16))
            self.apkOpen_Addr = str(int(configParser.get(unityVersion, 'apkOpen_Addr'), 16))
            self.IsFileCreated_Addr = str(int(configParser.get(unityVersion, 'IsFileCreated_Addr'), 16))


    def display(self):
        print self.unityVersion
        print 'JNI_OnLoad_Addr: ', self.JNI_OnLoad_Addr
        print 'UnitySendMessage_Addr: ',  self.UnitySendMessage_Addr
        print 'apkOpen_Addr: ', self.apkOpen_Addr
        print 'IsFileCreated_Addr: ', self.IsFileCreated_Addr


