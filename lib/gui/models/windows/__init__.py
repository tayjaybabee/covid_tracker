from configparser import ConfigParser



class PopupClassError(Exception):

    def __init__(self):
        pass


class InvalidArgumentError(PopupClassError):

    def __init__(self, info=None):
        """



        """
        message = 'You must supply a valid argument to create a popup!'
        if info is not None:
            message = str(message + ' ' + "Additional info" + info)
            



