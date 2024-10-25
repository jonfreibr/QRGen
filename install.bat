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
h:
cd "\_BRMCApps\QR Code Generator"
echo Installing Python 3.11.5
python-3.11.5-amd64.exe /passive
echo upgrading pip
%LocalAppData%\Programs\Python\Python311\python.exe -m pip install --upgrade pip -q
echo Adding package requirements
%LocalAppData%\Programs\Python\Python311\Scripts\pip.exe install -r requirements.txt -q
echo Copying shortcut to Desktop
copy /y "QR Generator.lnk" %USERPROFILE%\Desktop > nul 2>&1
echo Done with installation, Running QR Generator
"%USERPROFILE%\Desktop\QR Generator.lnk"
rem pause
rem exit