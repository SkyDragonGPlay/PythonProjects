#coding:utf-8

import subprocess, os, shutil, re
from UnpackAPKTool import unpack_apk
import UnityLibFuncOffsetConfig, utils

def buildUnitySmallPackage(unity_version, unity_proj_path):
    unity_exe_path = 'D:\Program Files\Unity5\Unity' + unity_version + '\Editor\Unity.exe'
    if len(unity_version) > 0 and unity_version[0] == '4':
        unity_exe_path = 'G:\SkyDragon\Unity\Program Files\Unity4\Unity' + unity_version + '\Editor\Unity.exe'
    unity_exe_args = '-quit -batchmode -projectPath "' + unity_proj_path + '" -executeMethod BuildProcessor.BuildAndroid' + ' GPlaySmallPackageTest.apk'

    command = '"' + unity_exe_path + '"' + ' ' + unity_exe_args
    print 'call: ', command
    subprocess.call(command, shell=True)


def replace_addr(lineContentList, addr, beginIdx, placeholderLen):
    addrLen = len(addr)
    for i in range(addrLen):
        lineContentList[beginIdx + i] = addr[i]

    for i in range(placeholderLen - addrLen):
        lineContentList[beginIdx + addrLen + i] = '\0'

    return lineContentList


def modify_so_file(unity_proj_path, unityLibFuncOffset):
    
    origionOSFileRelativePath = 'SmallPackageBuildAPKTool/libgplay.so'
    if not os.path.isfile(origionOSFileRelativePath):
        print 'Origion lib file is not found'
        return False

    soFilePath = os.path.join(unity_proj_path, 'Assets\\Plugins\\Android\\libs\\armeabi-v7a\\libgplay.so')
    soFilePathDir = os.path.dirname(soFilePath)

    if os.path.isfile(soFilePath):
        os.remove(soFilePath)

    if not os.path.isdir(soFilePathDir):
        os.makedirs(soFilePathDir)

    #shutil.copy(origionOSFileRelativePath, soFilePathDir)

    origionSOFile = open(origionOSFileRelativePath, 'rb')
    soFile = open(soFilePath, 'wb')
    
    count = 0
    for line in origionSOFile.readlines():
        isInitList = False
        lineContentList = []

        idx = line.find('JNI_ONLOAD_ADDR_STR')
        if idx >= 0:
            count += 1
            isInitList = True
            lineContentList = list(line)
            replace_addr(lineContentList, unityLibFuncOffset.JNI_OnLoad_Addr, idx, len('JNI_ONLOAD_ADDR_STR'))

        idx = line.find('UNITY_SEND_MESSAGE_ADDR_STR')
        if idx >= 0:
            count += 1
            if not isInitList:
                isInitList = True
                lineContentList = list(line)
            replace_addr(lineContentList, unityLibFuncOffset.UnitySendMessage_Addr, idx, len('UNITY_SEND_MESSAGE_ADDR_STR'))
            
        idx = line.find('APK_OPEN_ADDR_STR')
        if idx >= 0:
            count += 1
            if not isInitList:
                isInitList = True
                lineContentList = list(line)
            replace_addr(lineContentList, unityLibFuncOffset.apkOpen_Addr, idx, len('APK_OPEN_ADDR_STR'))
            
        idx = line.find('IS_FILE_CREATED_ADDR_STR')
        if idx >= 0:
            count += 1
            if not isInitList:
                isInitList = True
                lineContentList = list(line)
            replace_addr(lineContentList, unityLibFuncOffset.IsFileCreated_Addr, idx, len('IS_FILE_CREATED_ADDR_STR'))
        
        if isInitList:
            for i in range(len(lineContentList)):
                soFile.write(lineContentList[i])
        else:
            soFile.write(line)

    print 'Find out ', count, ' function address placeholder.'

    soFile.close()
    origionSOFile.close()
    return True


if __name__ == '__main__':
    unity_version = '4.6.0f3'
    unity_proj_path = 'D:\Unity' + unity_version[0] + '\Projects\GPlaySmallPackageTest'

    unityLibFuncOffsetConfig = UnityLibFuncOffsetConfig.UnityLibFuncOffsetConfig()
    unityLibFuncOffset = unityLibFuncOffsetConfig.get(unity_version)

    if unityLibFuncOffset != None:
        unityLibFuncOffset.display()

        is_modify_success = modify_so_file(unity_proj_path, unityLibFuncOffset)
        if is_modify_success:
            apkPath = os.path.join(unity_proj_path, 'GPlaySmallPackageTest.apk')
            if os.path.isfile(apkPath):
                os.remove(apkPath)

            buildUnitySmallPackage(unity_version, unity_proj_path)
            
            if os.path.isfile(apkPath):
                unpack_apk(apkPath)
                subprocess.call('adb uninstall com.gabo.test', shell=True)
                subprocess.call('adb install ' + apkPath, shell=True)
    else:
        print 'Not found ', unity_version, ' section in UnityLibConfig.ini file'
    

#JNI_ONLOAD_ADDR_STR
#UNITY_SEND_MESSAGE_ADDR_STR
#APK_OPEN_ADDR_STR
#IS_FILE_CREATED_ADDR_STR

