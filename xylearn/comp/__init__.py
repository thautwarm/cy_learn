# 
"""v-wazhao 2018/1/26 2:40 Beijing

Package `comp`: Components for composing 
"""

from .fn import *
from .operator import *
def using(closure):
    if callable(closure):
        closure().update(globals())
    else:
        closure.update(globals())