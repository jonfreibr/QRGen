@echo off
rem Example install batch file for Windows environment.
rem Run from the application directory
rem Required files:
rem     QR Generator.lnk            create this shortcut file to reflect your installation and runtime requirements!!
rem     QRGen.py                    The main application file
rem     python-3.11.5-amd64.exe     The Python source file
rem     requirements.txt            Used by Python to install required libraries
rem     unattend.xml                Required to run a "hands-off" install of Python.
rem
echo Installing Python 3.11.5
"%~dp0\python-3.11.5-amd64.exe" /passive
echo upgrading pip
%LocalAppData%\Programs\Python\Python311\python.exe -m pip install --upgrade pip
echo Adding package requirements
%LocalAppData%\Programs\Python\Python311\Scripts\pip.exe install -r "%~dp0\requirements.txt"
%LocalAppData%\Programs\Python\Python311\Scripts\pip.exe install -i https://PySimpleGUI.net/install PySimpleGUI
echo Copying shortcut to Desktop
copy /y "%~dp0\QR Generator.lnk" %USERPROFILE%\Desktop > nul 2>&1
echo Done with installation