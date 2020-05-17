import PySimpleGUIQt as Qt
from lib.api import fetch_data
from lib import PROG_NAME
from assets.images.icons import main as c_icon
from lib.gui.models.popups.warnings import not_yet_implemented
from lib.gui.models.windows.settings import SettingsWindow

import logging


class MainWindow:

    fetched = False

    app_theme = 'DarkAmber'

    Qt.theme(app_theme)

    menu_def = [['Application', 'Settings']]

    layout = [
        [Qt.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [Qt.MultilineOutput(autoscroll=True, key='output', do_not_clear=False)],
        [Qt.Button('Refresh', enable_events=True, key='refresh_bttn'),
         Qt.Button('Inspect', enable_events=True, key='inspect_bttn', visible=False),
         Qt.CloseButton('Close', key='close_bttn')]
    ]

    window = Qt.Window('CoVid 19 United States Stats', layout, size=(500, 600), icon=c_icon)

    while True:
        event, values = window.read(timeout=100)

        if not fetched:
            data = fetch_data(gui=True, main_win=window['output'])
            fetched = True

        if fetched:
            window['inspect_bttn'].Update(visible=True)
            window.refresh()

        if event is None or event == 'close_bttn':
            window.close()
            exit()

        if event == 'refresh_bttn':
            fetched = False

        if event == 'inspect_bttn':
            not_yet_implemented.pop('Inspect')

        if event == 'Settings':
            settings_window = SettingsWindow()