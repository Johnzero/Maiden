@echo off

@set Filename=%date:~0,4%-%date:~5,2%-%date:~8,2% %time:~0,2%µã%time:~3,2%·Ö.backup
@set Dirname=%date:~0,7%

rem Èç¹ûµ±ÌìÊÇÒ»ºÅÔòÐÂ½¨ÐÂÔÂ·ÝÄ¿Â¼
@if %date:~8,2% == 01 (md f:\backup\"%Dirname%")

rem Èç¹ûÃ»ÓÐµ±ÔÂÄ¿Â¼ÔòÐÂ½¨µ±ÔÂÄ¿Â¼
@if not exist f:\backup\"%Dirname%" (md f:\backup\"%Dirname%")
cd C:\Program Files (x86)\PostgreSQL\9.1\bin\
rem Ö´ÐÐ±¸·ÝÈÎÎñ,±¸·ÝdatabasenameÊý¾Ý¿â£¬Çë½«version»»³ÉÄãµÄpgsql°æ±¾£¬»òÕß¸ù¾ÝÄãµÄpg_dumpÎÄ¼þËùÔÚÎ»ÖÃÐÞ¸Ä¡£
pg_dump -h localhost -p 5432 -U openpg -F t -v -f f:\backup\\"%Dirname%"\\"%Filename%" V7 

@echo on
