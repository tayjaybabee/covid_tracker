import os

PROG_NAME = 'US-CoVIn'



class Config:

    def __init__(self):
        main_dir = os.path.expanduser('~/.inspyre_softworks')
        if os.path.exists(user_dir):
            print('oh my')



class ApplicationError(Exception):

     def __init__(self, doc_url=None, **kwargs):
         self.docs = 'https://github.com/tayjaybabee/covid_tracker'
         if doc_url is not None:
             self.docs = doc_url


class NotYetImplementedError(ApplicationError):

    def __init__(self, feat=None, **kwargs):
        """

        Args:
            feat:
        """
        super(NotYetImplementedError, self).__init__(feat, **kwargs)
        if feat is not None:
            f_feat = feat.replace(' ', '')
            if f_feat == '':
                feat = None

        if feat is None:
            feat = 'This feature'

        self.message = str(f'{feat} has not yet been implemented\n\n'\
                           f'For more information please see the link below\n {self.docs}')

