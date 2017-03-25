@echo off

:start

set endianness="little-endian"
set method="ToString"
python %~dp0HexStringConvertor.py --endianness=%endianness% --method=%method%

pause

goto start