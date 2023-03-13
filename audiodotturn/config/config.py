import os
import configparser
import pkg_resources


class ConfigBase:
    """
    Package config values are set, these should not be changed by user
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.userconfig = configparser.ConfigParser()
        self.path = pkg_resources.resource_filename(__name__, "config.ini")
        self.config.read(self.path)

    @property
    def user_paths(self):
        try:
            paths = self.config['PROGRAM']['userpaths'].replace(' ', '').split(',')
            return [os.path.expanduser(path.strip()) for path in paths]
        except:
            raise KeyError('PACKAGE CONFIG HAS ERRORS')

    @property
    def app_name(self):
        try:
            return self.config['APP']['name']
        except:
            raise KeyError('PACKAGE CONFIG HAS ERRORS')
    
    @property
    def output_opts(self):
        try:
            return self.config['PROGRAM']['output_opts'].replace(' ', '').split(',')
        except:
            raise KeyError('PACKAGE CONFIG HAS ERRORS')

    @property
    def constructors(self):
        try:
            return self.config['PROGRAM']['constructors'].replace(' ', '').split(',')
        except:
            raise KeyError('PACKAGE CONFIG HAS ERRORS')

class ConfigUser(ConfigBase):
    """
    Configurable user settings
    """
    def __init__(self, config_path: str = None):
        super().__init__()
        if config_path is not None:
            self.userconfig.read(config_path)
            self.path = config_path
        else:
            for path in self.user_paths:
                if os.path.exists(path):
                    self.userconfig.read(path)
                    self.path = path
                    break
    
    @property
    def config_path(self):
        if self.path is None:
            raise KeyError("CONFIG PATH ERROR")
        return self.path

    @property
    def db_path(self):
        try:
            return self.userconfig['DATABASE']['path']
        except KeyError:
            try:
                return self.config['DATABASE']['path']
            except:
                raise TypeError("PROBLEM WITH CONFIG")

    @property
    def dry(self):
        try:
            dry = self.userconfig['PROGRAM']['dry']
            return dry.lower() == 'true'
        except KeyError:
            try:
                dry = self.config['PROGRAM']['dry']
                return dry.lower() == 'true'
            except:
                raise TypeError("PROBLEM WITH CONFIG")

    @property
    def exts(self):
        try:
            return self.userconfig['PROGRAM']['exts'].replace(' ', '').split(',')
        except KeyError:
            try:
                return self.config['PROGRAM']['exts'].replace(' ', '').split(',')
            except:
                raise TypeError("PROBLEM WITH CONFIG")
