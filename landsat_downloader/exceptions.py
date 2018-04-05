# -*- coding: utf-8 -*-


class DownloaderErrors(Exception):
    def __init__(self, errors, *args, **kwargs):
        super(DownloaderErrors, self).__init__(*args, **kwargs)
        self.errors = errors

class WrongSceneNameError(Exception):
    pass


class RemoteFileDoesntExist(Exception):
    pass


class InvalidBandError(Exception):
    pass
