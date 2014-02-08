# -*- coding:utf-8 -*-
from fabric.api import *


def setup_local():
    local('virtualenv env --no-site-packages', capture=False)
    local('env/bin/pip install -r requirements.txt', capture=False)


def update_local_env():
    local('env/bin/pip install -r requirements.txt -U', capture=False)


def test_local():
    local("env/bin/python manage.py test")
