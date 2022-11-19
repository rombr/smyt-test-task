"""
Utils tools
"""
import os
import datetime
import xml
import logging

from yaml import load
from yaml.parser import ParserError, ScannerError

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import xmltodict

from .settings import MODELS_CONFIG


logger = logging.getLogger("foo")


class LoadModelsError(Exception):
    pass


class NoConfigFileError(LoadModelsError):
    pass


class InvalidConfigFileFormatError(LoadModelsError):
    pass


class ConfigFileParseError(LoadModelsError):
    pass


def get_models_config(config_file=MODELS_CONFIG):
    config_file = config_file or ""

    if not os.path.exists(config_file):
        raise NoConfigFileError(f"Config file {config_file} does not exist")
    cfg_type = config_file.split(".")[-1]

    models_spec = {}
    if cfg_type == "yaml":
        try:
            models_spec = load(open(config_file, "r").read(), Loader=Loader)
        except (ParserError, ScannerError) as e:
            raise ConfigFileParseError(e)
        else:
            logger.debug(models_spec)
    elif cfg_type == "xml":
        try:
            models_spec = xmltodict.parse(open(config_file, "r").read()).get(
                "models", {}
            )
        except (xml.parsers.expat.ExpatError) as e:
            raise ConfigFileParseError(e)
        else:
            logger.debug(models_spec)
    else:
        raise InvalidConfigFileFormatError(f"Format: {cfg_type} not supported")
    return models_spec


def default_for_date(o):
    """
    Сериализация для ключей кеша в ядре
    """
    if isinstance(o, datetime.datetime):
        o = datetime.datetime.isoformat()
        return o
    else:
        if isinstance(o, datetime.date):
            o = datetime.datetime.strftime(o, "%Y-%m-%d")
            return o
    return None
