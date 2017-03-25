#coding:utf-8

import sys, subprocess, getopt

def get_port(psInfo):
    items = psInfo.split(' ')
    i = 0
    while i < len(items):
        if items[i] == '':
            del items[i]
        else:
            i += 1

    if len(items) > 2 and items[1].isdigit():
        port = items[1]
    else:
        port = '0'

    return port


def run_app_with_debug(packageName, activityName):
    command = 'adb shell am start -D -n ' + packageName + '/' + activityName
    print command
    subprocess.call(command, shell=True)

    appPort = '0'
    file_out = subprocess.Popen('adb shell ps', shell=True, bufsize=2048, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = file_out.stdout.readline()
        if line.find(packageName) > 0:
            print line
            items = line.split(' ')
            i = 0
            while i < len(items):
                if items[i] == '':
                    del items[i]
                else:
                    i += 1  
            if len(items) > 2 and items[1].isdigit():
                appPort = items[1]
            else:
                appPort = '0'
        if subprocess.Popen.poll(file_out) == 0: #判断子进程是否结束
            break
    return appPort


if __name__ == '__main__':
    
    prompt = '-h: help\n'
    prompt += '--package: package name\n'
    prompt += '--activity: activity name\n'
    prompt += '--jdb: jdb file path\n'
    if len(sys.argv) == 1:
        print prompt
    else:
        #Python 获得命令行参数的方法: http://blog.csdn.net/intel80586/article/details/8545572
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['package=', 'activity=', 'jdb='])
        #activityName = None
        #jdbFilePath = None
        for opt, value in opts:
            if opt == '--package':
                packageName = value
            elif opt == '--activity':
                activityName = value
            elif opt == '--jdb':
                jdbFilePath = value

        print 'packageName: ', packageName, '\nactivityName: ', activityName, '\njdbFilePath: ', jdbFilePath, '\n'

        if packageName==None or activityName==None or jdbFilePath==None:
            print 'Please enter arguments'
        else:
            appPort = run_app_with_debug(packageName, activityName)

            if appPort != '0':
                port = '5000'
                command = 'adb forward tcp:' + port + ' jdwp:' + appPort
                print command
                subprocess.call(command, shell=True)

                str = raw_input('输入回车')

                command = '"' + jdbFilePath + '" -connect com.sun.jdi.SocketAttach:hostname=localhost,port=' + port
                print command
                subprocess.call(command, shell=True)
    