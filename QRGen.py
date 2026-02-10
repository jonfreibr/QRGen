"""
Author      : Jon Freivald
Date        : 10/17/2024
Purpose     : Generate QR Codes
Copyright   : 2024, 2026, Blue Ridge Medical Center
Platform    : Microsoft Windows
License     : MIT
Change log  : at eof
"""

import PySimpleGUI as sg
import segno
from segno import helpers
import os
import subprocess
from sys import platform
import sys
import atexit
from datetime import datetime

BRMC = {'BACKGROUND': '#73afb6',
                 'TEXT': '#00446a',
                 'INPUT': '#ffcf01',
                 'TEXT_INPUT': '#00446a',
                 'SCROLL': '#ce7067',
                 'BUTTON': ('#ffcf01', '#00446a'),
                 'PROGRESS': ('#ffcf01', '#00446a'),
                 'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                 }
sg.theme_add_new('BRMC', BRMC)

progver = 'v 1.1c'
mainTheme = 'BRMC'
errorTheme = 'HotDogStand'

# --------------------------------------------------
def do_update():
    sg.theme('Kayak')
    layout = [ [sg.Text('There is an update available for the IQT application.')],
                [sg.Text('Automatic updates are only available for Windows at this time.')],
                [sg.Text('Other platforms please check with your systems administrator.')],
                [sg.Button("Update"), sg.Button("Skip")]]
    window = sg.Window("Updates", layout)
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Skip'):
            atexit.unregister(update_app)
            window.close()
            break
        if event == "Update":
            exit()

# --------------------------------------------------

def update_app():
    if platform == "win32":
        subprocess.Popen(["cmd", "/c", "H:/_BRMCApps/QR Code Generator/install.bat", "/min"], stdout=None, stderr=None)

# --------------------------------------------------

def make_code():
    qrcode=False
    wifisec_options = ['WPA', 'WEP', 'nopass']
    name = subprocess.check_output(
        'net user "%USERNAME%" /domain | find /I "Full Name"', shell=True, text=True
    )
    full_name = name.replace("Full Name", "").strip()
    first_name = full_name.split()[0]
    sg.theme(mainTheme)
    col1 = [
            [sg.Text(f"Welcome {first_name}")],
            [sg.Text("Data to encode: ")],
            [sg.Text("--OR--", text_color='red', background_color='yellow')],
            [sg.Text("WiFi SSID:")],
            [sg.Text("WiFi Password:")],
            [sg.Text("WiFi Security:")],
            [sg.Text("--OR--", text_color='red', background_color='yellow')],
            [sg.Text("Name (Required):")],
            [sg.Text("Display Name:")],
            [sg.Text("Org:")],
            [sg.Text("Job Title:")],
            [sg.Text("Phone:")],
            [sg.Text("Cell Phone:")],
            [sg.Text("P.O. Box:")],
            [sg.Text("Street Address:")],
            [sg.Text("City, State, Zip Code:")],
            [sg.Text("EMail:")],
            [sg.Text("URL:")],
            [sg.Text("--AND--", text_color='red', background_color='yellow')],
            [sg.Text("Filename:")],
            [sg.Text("--THEN--", text_color='red', background_color='yellow')],
            [sg.Button('Create', bind_return_key=True, button_color=('yellow', 'green')), sg.Button('Done', button_color=('yellow', 'red'))],
        ]
    col2 = [
            [sg.Text("")],
            [sg.InputText(size=(80,None), key='qrdat')],
            [sg.Text("")],
            [sg.InputText(size=(60,None), key='wfssid')],
            [sg.InputText(size=(60,None), key='wfpass')],
            [sg.Combo(wifisec_options,default_value=wifisec_options[0], key='wfsec')],
            [sg.Text("")],
            [sg.InputText(size=(60,None), key='vCname'), sg.Text('Format: "Last; First"')],
            [sg.InputText(size=(60,None), key='vCdname')],
            [sg.InputText(size=(60,None), key='vCorg')],
            [sg.InputText(size=(60,None), key='vCrole')],
            [sg.InputText(size=(14,None), key='vCphone')],
            [sg.InputText(size=(14,None), key='vCcphone')],
            [sg.InputText(size=(40,None), key='vCpobox')],
            [sg.InputText(size=(60,None), key='vCstreet')],
            [sg.InputText(size=(30,None), key='vCcity'), sg.InputText(size=(3,None), key='vCstate'), sg.InputText(size=(12,None), key='vCzip')],
            [sg.InputText(size=(50,None), key='vCemail')],
            [sg.InputText(size=(60,None), key='vCurl')],
            [sg.Text("")],
            [sg.InputText(size=(40,None), key='filnam'), sg.Text(".png (will be in your Downloads folder)")],
            [sg.Text("")],
            [sg.Text("", key='msg')],
        ]
    layout = [
        [sg.Column(col1), sg.Column(col2)]
    ]
    window = sg.Window(f"Create QR Code {progver}", layout, element_justification='left', modal=True, finalize=True)
    window.BringToFront()
    window['qrdat'].set_focus()
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Done'):
            window.close()
            return
        if event == 'Create':
            window['msg'].update("")
            if values['qrdat']:
                qrcode = segno.make_qr(values['qrdat'])
            elif values['vCname']:
                qrcode = helpers.make_vcard(name=values['vCname'], displayname=values['vCdname'], org=values['vCorg'], title=values['vCrole'],
                                            phone=values['vCphone'], cellphone=values['vCcphone'], pobox=values['vCpobox'],
                                            street=values['vCstreet'], city=values['vCcity'], region=values['vCstate'],
                                            zipcode=values['vCzip'], email=values['vCemail'], url=values['vCurl'])
            elif values['wfssid']:
                wifi_settings = {
                    'ssid': values['wfssid'],
                    'password': values['wfpass'],
                    'security': values['wfsec']
                }
                qrcode = helpers.make_wifi(**wifi_settings)
            if values['filnam'] and qrcode:
                fileroot = values['filnam']
                file = f'{os.path.expanduser("~")}/Downloads/{fileroot}.png'
                qrcode.save(
                    file,
                    scale=5,
                )
                window['msg'].update(f"QR Code saved to: {file}")
            window['qrdat'].update("")
            window['filnam'].update("")
            window['vCname'].update("")
            window['vCdname'].update("")
            window['vCorg'].update("")
            window['vCrole'].update("")
            window['vCphone'].update("")
            window['vCcphone'].update("")
            window['vCpobox'].update("")
            window['vCstreet'].update("")
            window['vCcity'].update("")
            window['vCstate'].update("")
            window['vCzip'].update("")
            window['vCemail'].update("")
            window['vCurl'].update("")

# --------------------------------------------------

if __name__ == '__main__':
    answer = False
    try:
        if platform == "win32":
            if datetime.fromtimestamp(os.path.getmtime(__file__)) < datetime.fromtimestamp(os.path.getmtime('H:/_BRMCApps/QR Code Generator/QRGen.py')):
                atexit.register(update_app)
                answer = do_update()
    except:
        pass

    if answer:
        sys.exit()
    else:
        make_code()

"""
v 0.1   : 10/17/24  : Initial version -- PySimpleGUI wrapper around segno library to generate QR codes.
v 0.2   : 10/18/24  : Fleshed it out a little -- won't create an empty file, saves to (Windows) users Downloads directory, 
                    : greets user by name.
v 0.3   : 11/5/24   : Added the ability to create a vCard.
v 0.4   : 11/5/24   : Simple UI tweaks
v 0.5   : 11/5/24   : Total UI overhaul.
v 1.0   : 11/13/24  : Added address and cell phone to vCard.
v 1.1   : 10/10/25  : Added WiFi QR Code generator.
v 1.1a  : 10/13/25  : Added application auto-update.
v 1.1b  : 02/09/26  : Removed PySimpleGUI v5 license key, converted to PySimpleGUI-4-foss.
v 1.1c  : 02/10/26  : simple UI update
"""