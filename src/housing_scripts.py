import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from FormatScripts import hello



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

def abr_suf(x):
    if x == 'Street':
        return ' st'
    elif x == 'Avenue':
        return ' ave'
    elif x == 'Boulevard':
        return ' blvd'
    elif x == 'Drive':
        return ' dr'
    elif x == 'Way':
        return ' wy'
    elif x == 'Place' or x == 'place':
        return ' pl'
    elif x == 'Lane':
        return ' ln'
    elif x == 'Court':
        return ' ct'
    elif x == 'Parkway':
        return ' pkwy'
    elif x == 'Road':
        return ' rd'
    else:
        return ''

def prop_type_update(x):
    if x == 'Duplex' or x == 'Triplex' or x == 'Duadruplex':
        return 'Multi'
    elif x == 'Studio' or x == 'Loft' or x == 'Condominium':
        return 'Condominium'
    elif x == 'Townhouse':
        return 'Townhouse'
    else:
        return 'Single Family Residence'

def yn_impute(x):
    if x == True:
        return 1
    else:
        return 0

def impute_features(df, feature_list):
    for feature in feature_list:
        df[feature] = df[feature].apply(yn_impute)

def wall_clean(x):
    if x == 'No Common Walls' or x == 'End Unit' or x == 'End Unit, No Common Walls' or x == 'No Common Walls, End Unit':
        return 1
    else:
        return 0
