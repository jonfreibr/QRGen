"""
Author      : Jon Freivald
Date        : 10/17/2024
Purpose     : Generate QR Codes
Copyright   : 2024, Blue Ridge Medical Center
Platform    : Microsoft Windows
License     : MIT
Change log  : at eof
"""

# Distribution license for PySimpleGUI v5
PySimpleGUI_License = 'eEygJDMKaqWCNxlnb8nCNQlXViHAlWwQZrSVI66MIgkuRhpncx3hRhyzaJWoJ41qd7G8lmvebmifIms7IYksxrpbYL2sVkuYcy2cVzJ1RACnI46EMMTgc1x3ODTOk3zNMgjBce5KNQyuwKiPTdGTlijVZDWG54zGZbUGRZlCcuGaxAvQe7W91flrbJnvRuWfZ2XVJ6zza1WX9PuVIwjRoYi0NoSe4vwQIfiOwQitTmmDF2tqZrUsZHp7c7ntNd00I7jZo3isSmmt9UuJIqipwxiyTcmhFttkZSUnx7hec63VQgidOTiWJHGXc0miV7p4dFmHFqswZXCmI5sJIakVNSvzbFXgBPhmbWnrkGikOXiXJjCxbTHgVUldIeF0JnpYZqGkdQlnImEx1ylIZpGTlQjNYfWwwPgfQE2rV5u4dsGVVvykIBi4wOiWQr3jVLzmdJGC9htiZDX7JnJ6RmCyIi6mI4jzkr3tNQTsE6i4LgCBJtEEY2XTRmlWSkXGNDzkdBWfVjk3I8j6ociOM0jYApy0NoCu0xwWN8yJ0VwdMqirIAsPI8kpR0hbdTGTVJFnedH3BTp7c5mwVyzQIWjtoeiaMXjfABySN5SB0lwBMYyh0bxyOrSvIvsPICkSVvtmYmWHl0svQdW5RAkQcjmhV6zCcZyEI46AIHmupRmHcImLV0pSdSmBF0sCZrEOBCibcJmu1JlSZcGElrj6YoWsw7uwYY2Z9ZtwIKidwLiBSsV8BmBrZzGERzyFZgXQNwzbIVjjoKiuMFjDAh1uLHj7IlyIMWCw4eyjMOzkUYuSMyzXQ0iJfoQ8=A=b8271950926a545600f2f1033bf533e55d9b697a2dfce0a0ced401428b1ad9753eedcc663477a54ccf3225a8cb7bd886562e05aeddeea68adc91d57cabd33fba6cf6082befac466e3ecdde665f5487ebfd5b5cd4240c4eba3eedb923a49117c1b83ac08a8e9eb19d521f15e6c903da0b234d0987850ce5259a7920fb37f14ad5479622e81e5df279682f552ddb7136dc13ef73e62b49d45ef534ecb1edca78b47fd59db2ef098eed3855aa771cfacc7f3c104576eca792351d023fc02b5b111a59358d6e0d33b46099e5b80728bfcab2d1a876fb5f3d509ed8ca69cf9ec62e214be35b01b72c22e00cca3a989dcea424cda4b54f614f92a0a4cdd92b475c08af8dc1a715ea61b9431c75fb4d1a5ced13c779ec939d6e99229dea2b328467e936136cc37dd9ec567b02aeb75cb6b07932cfc27348bb096908dd98bec5554fdf9e83afff5fc8e91172779806ac08d19a1675fde17aae3d233432f80060f2af3d7f68779ff75fa8b4ddfee10d83e61239dc8cbe197c56543827215b52455b35e668a6a844781120bef888e1d1a23b59a0a616aaaa7645fbe41eef39a6d552233b6171d87d10c19b39a262e1a6e1ad7fa0b8ccc08caf9e9b018f302231a87795b534da43f15d3b9ff15ff78da645ddaec09b7aff50ce81908750b4b4eb2310d48ca4edc113138622f831d58784968c0824773395aec085aa5e7b4b938dff2d5d1da0b'

import PySimpleGUI as sg
import segno
from segno import helpers
import os
import subprocess

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

progver = 'v 1.0'
mainTheme = 'BRMC'
errorTheme = 'HotDogStand'

def make_code():
    qrcode=False
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
            [sg.InputText(size=(40,None), key='filnam'), sg.Text(".png")],
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



if __name__ == '__main__':
    make_code()

"""
v 0.1   : 10/17/24  : Initial version -- PySimpleGUI wrapper around segno library to generate QR codes.
v 0.2   : 10/18/24  : Fleshed it out a little -- won't create an empty file, saves to (Windows) users Downloads directory, 
                    : greets user by name.
v 0.3   : 11/5/24   : Added the ability to create a vCard.
v 0.4   : 11/5/24   : Simple UI tweaks
v 0.5   : 11/5/24   : Total UI overhaul.
v 1.0   : 11/13/24  : Added address and cell phone to vCard.
"""