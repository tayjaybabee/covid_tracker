import PySimpleGUIQt as qt
from assets.images.icons import main as c_icon, error as err_icon
from conf import run


class SettingsWindow:
    '''

    Settings window for the CoVid 19 tracker program

    '''

    @staticmethod
    def button_frame():
        _layout = [[qt.Button('OK', enable_events=True, key='settings_win_ok_bttn', bind_return_key=True),
                    qt.Button('Apply', enable_events=True, key='settings_win_apply_bttn', visible=False),
                    qt.Button('Cancel', enable_events=True, key='settings_win_cancel_bttn', visible=False)]]
        _frame = qt.Frame('', _layout)
        return _frame

    @staticmethod
    def form_frame():
        _layout = [[qt.Text('Look & Feel: '), qt.Combo(qt.theme_list(), enable_events=True, key='look_and_feel_combo')]]
        _frame = qt.Frame('Settings', _layout)
        return _frame

    def layout(self):
        _layout = [
            [self.form_frame()],
            [self.button_frame()]

        ]
        return _layout

    def window(self):
        if self.config is None:
            qt.theme('Dark2')
        else:
            qt.theme(self.config['GUI']['theme'])

        window = qt.Window('Settings - CoViD 19 Tracker', layout=self.layout(), icon=c_icon, force_toplevel=True)

        return window

    def __init__(self):

        self.config = run.config

        win = self.window()

        while True:
            event, values = win.read(timeout=100)

            if event is None or event == 'settings_win_cancel_bttn':
                win.close()

            if event == 'settings_win_ok_bttn':
                qt.PopupOK(
                    'Saving settings isn\'t currently implemented. This will close the window and NOT save settings',
                    icon=err_icon)
                win.close()

            if event == 'look_and_feel_combo':
                qt.theme(str(values['look_and_feel_combo']))
                win.refresh()


SettingsWindow()
