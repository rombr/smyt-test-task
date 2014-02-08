# -*- coding:utf-8 -*-
'''
Utils tools
'''
import os
import datetime
import xml

import logging
logger = logging.getLogger('foo')

from yaml import load
from yaml.parser import ParserError, ScannerError
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import xmltodict

from settings import MODELS_CONFIG


class LoadModelsError(Exception):
    pass


class NoConfigFileError(LoadModelsError):
    pass


class InvalidConfigFileFormatError(LoadModelsError):
    pass


class ConfigFileParseError(LoadModelsError):
    pass


def get_models_config(config_file=MODELS_CONFIG):
    config_file = config_file or ''

    if not os.path.exists(config_file):
        raise NoConfigFileError(u'Config file %s does not exist' % config_file)
    cfg_type = config_file.split('.')[-1]

    models_spec = {}
    if cfg_type == 'yaml':
        try:
            models_spec = load(open(MODELS_CONFIG, 'r').read(), Loader=Loader)
        except (ParserError, ScannerError) as e:
            raise ConfigFileParseError(e)
        else:
            logger.debug(models_spec)
    elif cfg_type == 'xml':
        try:
            models_spec = xmltodict.parse(open(MODELS_CONFIG, 'r').read()).get('models', {})
        except (xml.parsers.expat.ExpatError) as e:
            raise ConfigFileParseError(e)
        else:
            logger.debug(models_spec)
    else:
        raise InvalidConfigFileFormatError(u'Format: %s not supported' % cfg_type)
    return models_spec


def default_for_date(o):
    '''
    Сериализация для ключей кеша в ядре
    '''
    if isinstance(o, datetime.datetime):
        o = datetime.datetime.isoformat()
        return o
    else:
        if isinstance(o, datetime.date):
            o = datetime.datetime.strftime(o, '%Y-%m-%d')
            return o
    return None
