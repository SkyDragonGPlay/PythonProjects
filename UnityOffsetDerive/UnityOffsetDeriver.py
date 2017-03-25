#coding:utf-8

import UnityLibFuncOffsetConfig, os, shutil, glob, sys, subprocess, re


#正则匹配指定函数的偏移值
def GetFuncAddressOnNone(funcName, content):
    match = re.match(r'\d+:\s(\w+)\s+.*\S*'+ funcName + '\S*', content)
    if not match == None:
        return match.group(1)
    return None

#通过符号文件　初始化　UnityLibFuncOffsetConfig　实例
def GetFuncOffset(symbolsFile, funcOffset):
    with open(symbolsFile) as f:
        for line in f:
            result = GetFuncAddressOnNone("JNI_OnLoad", line)
            if not result == None:
                funcOffset.JNI_OnLoad_Addr_STR = "0x" + result

            result = GetFuncAddressOnNone("UnitySendMessage", line)
            if not result == None:
                funcOffset.UnitySendMessage_Addr_STR = "0x" + result

            result = GetFuncAddressOnNone("apkOpen", line)
            if not result == None:
                funcOffset.apkOpen_Addr_STR = "0x" + result

            result = GetFuncAddressOnNone("IsFileCreated", line)
            if not result == None:
                funcOffset.IsFileCreated_Addr_STR = "0x" + result

            result = GetFuncAddressOnNone("WWW6Create", line)
            if not result == None:
                funcOffset.WWWCreate_Addr_STR = "0x" + result



if __name__ == '__main__':
    
    if not len(sys.argv) >= 2:
        cfg = UnityLibFuncOffsetConfig.UnityLibFuncOffsetConfig()
        emptyVers = cfg.getEmptyVers()

        destDir = "D:\\Program Files\\Unity5\\Symbols"
        if not os.path.isdir(destDir):
            os.mkdir(destDir)

        for v in emptyVers:
            symbolsFile = "D:\\Program Files\Unity5\\Unity" + v + "\\Editor\\Data\\PlaybackEngines\\AndroidPlayer\\Variations\\mono\\Release\\Symbols\\armeabi-v7a\\libunity.sym.so"
            destSymboFile = destDir + "\\libunity" + v + ".sym.so";
            shutil.copy(symbolsFile, destSymboFile)
    else:
        config = UnityLibFuncOffsetConfig.UnityLibFuncOffsetConfig()
        
        symbolsFiles = glob.glob("./Symbols/*.sym.so")
        for file in symbolsFiles:
            command = "readelf -a " + file + " > " + file + ".txt"
            subprocess.call(command, shell = True)

            funcOffset = UnityLibFuncOffsetConfig.UnityLibFuncOffset()
            funcOffset.unityVersion = file[-14:-7]
            GetFuncOffset(file + ".txt", funcOffset)
            config.setFuncOffset(funcOffset)
        config.save()






