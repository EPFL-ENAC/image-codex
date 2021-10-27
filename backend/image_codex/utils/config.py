import configparser
import os


class EnvInterpolation(configparser.BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)


__config = configparser.ConfigParser(interpolation=EnvInterpolation())
__config.read('image_codex/config.ini')

fast_api_config = __config['fast_api']
cloudinary_config = __config['cloudinary']
