# -*- coding: utf-8 -*-


def makefunc(variables, expression, envir=globals()):
    return eval('(lambda ' + ','.join(variables)[:1] + ': ' + expression + ')', envir)
