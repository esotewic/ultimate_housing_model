import numpy as np
import pandas as pd




def string(x):
    return str(x)


def add_unit(x):
    if x != 0:
        return ' ' + str(x)
    else:
        return ''


def lower(x):
    return x.lower()


def roound(x):
    if isinstance(x,str)==True:
        return x
    else:
        return round(x)
