# -*- encoding:utf-8 -*-
# author: liuheng
class InitException(Exception):
    def __str__(self):
        return repr('init failed')