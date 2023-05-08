import sys
from configparser import ConfigParser
from src.exception import CustomException


def db_config(filename='config.ini', section='postgresql'):
    try:
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise CustomException(
                'Section {0} not found in the {1} file'.format(section, filename), sys)
        return db
    except Exception as error:
        raise CustomException(error, sys)


def page_config(filename='config.ini', section='pageconfig'):
    try:
        parser = ConfigParser()
        parser.read(filename)
        page = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                page[param[0]] = param[1]
        else:
            raise CustomException(
                'Section {0} not found in the {1} file'.format(section, filename), sys)
        return page
    except Exception as error:
        raise CustomException(error, sys)


def url_config(filename='config.ini', section='urlconfig'):
    try:
        parser = ConfigParser()
        parser.read(filename)
        url = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                url[param[0]] = param[1]
        else:
            raise CustomException(
                'Section {0} not found in the {1} file'.format(section, filename), sys)
        return url
    except Exception as error:
        raise CustomException(error, sys)
