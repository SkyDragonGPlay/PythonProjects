#coding:utf-8

import ConfigParser

class UnityLibFuncOffsetConfig:
    
    __unityLibFuncOffsetDic__ = {}
    
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read('SmallPackageBuildAPKTool/UnityLibConfig.ini')
        
        for section in cf.sections():
            self.__unityLibFuncOffsetDic__[section] = UnityLibFuncOffset(cf, section)
        
    def get(self, unityVersion):
        result = None
        if self.__unityLibFuncOffsetDic__.has_key(unityVersion):
            result = self.__unityLibFuncOffsetDic__[unityVersion]
        return result


class UnityLibFuncOffset:
    def __init__(self, configParser, unityVersion):
        self.unityVersion = unityVersion
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
