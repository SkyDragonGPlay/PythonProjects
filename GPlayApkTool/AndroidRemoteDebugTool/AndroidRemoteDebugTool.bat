@echo off

rem set packageName="com.zzl.uplay"				::包名
rem set activityName="com.unity3d.player.UnityPlayerActivity"
rem set jdbFilePath="C:\Program Files\Java\jdk1.8.0_91\bin\jdb.exe"


set packageName="com.gabo.test"
set activityName="com.unity3d.player.UnityPlayerActivity"
set jdbFilePath="C:\Program Files\Java\jdk1.8.0_91\bin\jdb.exe"

:start

python %~dp0AndroidRemoteDebugTool.py --package=%packageName% --activity=%activityName% --jdb=%jdbFilePath%
pause

goto start