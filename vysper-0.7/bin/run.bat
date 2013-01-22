@REM ----------------------------------------------------------------------------
@REM Copyright 2001-2004 The Apache Software Foundation.
@REM
@REM Licensed under the Apache License, Version 2.0 (the "License");
@REM you may not use this file except in compliance with the License.
@REM You may obtain a copy of the License at
@REM
@REM      http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM Unless required by applicable law or agreed to in writing, software
@REM distributed under the License is distributed on an "AS IS" BASIS,
@REM WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM See the License for the specific language governing permissions and
@REM limitations under the License.
@REM ----------------------------------------------------------------------------
@REM

@echo off

set ERROR_CODE=0

:init
@REM Decide how to startup depending on the version of windows

@REM -- Win98ME
if NOT "%OS%"=="Windows_NT" goto Win9xArg

@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" @setlocal

@REM -- 4NT shell
if "%eval[2+2]" == "4" goto 4NTArgs

@REM -- Regular WinNT shell
set CMD_LINE_ARGS=%*
goto WinNTGetScriptDir

@REM The 4NT Shell from jp software
:4NTArgs
set CMD_LINE_ARGS=%$
goto WinNTGetScriptDir

:Win9xArg
@REM Slurp the command line arguments.  This loop allows for an unlimited number
@REM of agruments (up to the command line limit, anyway).
set CMD_LINE_ARGS=
:Win9xApp
if %1a==a goto Win9xGetScriptDir
set CMD_LINE_ARGS=%CMD_LINE_ARGS% %1
shift
goto Win9xApp

:Win9xGetScriptDir
set SAVEDIR=%CD%
%0\
cd %0\..\.. 
set BASEDIR=%CD%
cd %SAVEDIR%
set SAVE_DIR=
goto repoSetup

:WinNTGetScriptDir
set BASEDIR=%~dp0\..

:repoSetup
if exist %BASEDIR%\bin\setenv.bat call %BASEDIR%\bin\setenv.bat

if "%JAVACMD%"=="" set JAVACMD=java

if "%REPO%"=="" set REPO=..\lib

set CLASSPATH="%BASEDIR%"\config;"%REPO%"\nbxml-0.7.jar;"%REPO%"\vysper-core-0.7.jar;"%REPO%"\commons-io-1.4.jar;"%REPO%"\commons-lang-2.5.jar;"%REPO%"\dnsjava-2.0.8.jar;"%REPO%"\xep0045-muc-0.7.jar;"%REPO%"\xep0060-pubsub-0.7.jar;"%REPO%"\xep0124-xep0206-bosh-0.7.jar;"%REPO%"\jetty-servlet-7.2.1.v20101111.jar;"%REPO%"\jetty-security-7.2.1.v20101111.jar;"%REPO%"\vysper-websockets-0.7.jar;"%REPO%"\jetty-websocket-7.2.1.v20101111.jar;"%REPO%"\jetty-server-7.2.1.v20101111.jar;"%REPO%"\jetty-continuation-7.2.1.v20101111.jar;"%REPO%"\jetty-http-7.2.1.v20101111.jar;"%REPO%"\jetty-io-7.2.1.v20101111.jar;"%REPO%"\jetty-util-7.2.1.v20101111.jar;"%REPO%"\servlet-api-2.5.jar;"%REPO%"\spring-context-3.0.5.RELEASE.jar;"%REPO%"\spring-aop-3.0.5.RELEASE.jar;"%REPO%"\aopalliance-1.0.jar;"%REPO%"\spring-beans-3.0.5.RELEASE.jar;"%REPO%"\spring-core-3.0.5.RELEASE.jar;"%REPO%"\spring-expression-3.0.5.RELEASE.jar;"%REPO%"\spring-asm-3.0.5.RELEASE.jar;"%REPO%"\mina-core-2.0.2.jar;"%REPO%"\jcr-1.0.jar;"%REPO%"\jackrabbit-core-1.5.3.jar;"%REPO%"\concurrent-1.3.4.jar;"%REPO%"\commons-collections-3.1.jar;"%REPO%"\jackrabbit-api-1.5.0.jar;"%REPO%"\jackrabbit-jcr-commons-1.5.3.jar;"%REPO%"\jackrabbit-spi-commons-1.5.0.jar;"%REPO%"\jackrabbit-spi-1.5.0.jar;"%REPO%"\jackrabbit-text-extractors-1.5.0.jar;"%REPO%"\poi-3.0.2-FINAL.jar;"%REPO%"\commons-logging-1.1.jar;"%REPO%"\poi-scratchpad-3.0.2-FINAL.jar;"%REPO%"\pdfbox-0.7.3.jar;"%REPO%"\fontbox-0.1.0.jar;"%REPO%"\jempbox-0.2.0.jar;"%REPO%"\nekohtml-1.9.7.jar;"%REPO%"\xercesImpl-2.8.1.jar;"%REPO%"\xml-apis-1.3.03.jar;"%REPO%"\lucene-core-2.3.2.jar;"%REPO%"\derby-10.2.1.6.jar;"%REPO%"\commons-codec-1.4.jar;"%REPO%"\slf4j-api-1.5.3.jar;"%REPO%"\slf4j-log4j12-1.5.3.jar;"%REPO%"\log4j-1.2.14.jar;"%REPO%"\jcl-over-slf4j-1.5.3.jar;"%REPO%"\spec-compliance-0.7.jar;"%REPO%"\ehcache-core-2.2.0.jar;"%REPO%"\vysper-0.7.pom
set EXTRA_JVM_ARGUMENTS=
goto endInit

@REM Reaching here means variables are defined and arguments have been captured
:endInit

%JAVACMD% %JAVA_OPTS% %EXTRA_JVM_ARGUMENTS% -classpath %CLASSPATH_PREFIX%;%CLASSPATH% -Dapp.name="run" -Dapp.repo="%REPO%" -Dbasedir="%BASEDIR%" org.apache.vysper.spring.ServerMain %CMD_LINE_ARGS%
if ERRORLEVEL 1 goto error
goto end

:error
if "%OS%"=="Windows_NT" @endlocal
set ERROR_CODE=1

:end
@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" goto endNT

@REM For old DOS remove the set variables from ENV - we assume they were not set
@REM before we started - at least we don't leave any baggage around
set CMD_LINE_ARGS=
goto postExec

:endNT
@endlocal

:postExec

if "%FORCE_EXIT_ON_ERROR%" == "on" (
  if %ERROR_CODE% NEQ 0 exit %ERROR_CODE%
)

exit /B %ERROR_CODE%
