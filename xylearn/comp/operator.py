# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 23:55:54 2018

@author: twshe
"""

from collections import namedtuple
from functools import reduce
from typing import TypeVar, Callable
T = TypeVar('T')
G = TypeVar('G')

def postfix(a: T, b:Callable[[T], G]):
    return b(a)

__all__ = ['kv', 'op', 'hold', '_', 'KeyPair']

KeyPair = namedtuple('KeyPair', ['key', 'value'])
Monad = namedtuple('Monad', ['context'])

class Holder:
    __slots__ = ['holded']
    def __init__(self, holded=None):
        self.holded = holded
    def __matmul__(self, x):
        return Holder(x)

class KeyArrow:
    __slots__ = []
    @classmethod
    def __getitem__(cls, kv):
        if isinstance(kv, tuple) and len(kv) is 2:
            return KeyPair(*kv)
        else:
            raise TypeError('Invalid Key-Value pair.')
        
kv = KeyArrow()
hold = Holder()


class FunctionOperator:
    def __init__(self, take=()):
        self.dispatch = take
    
    def __or__(self, x):
        return FunctionOperator((*self.dispatch, x))
    
    def __add__(self, x):
        raise NotImplemented 
    
    def __and__(self, x):
        raise NotImplemented
    
    def __xor__(self, x):
        raise NotImplemented    
    
    def __mod__(self, x):
        raise NotImplemented
    
    def __truediv__(self, x):
        raise NotImplemented
    
    def __call__(self, x):
        return reduce(postfix, self.dispatch, x)
        
op = FunctionOperator()    

    
class Lambda:
    """applicative lambda
    _ = Lambda()
    map(_ + 1, )
    """
    __slots__ = ['right']
    
    @property
    def r(self):
        return Lambda(right = True)
    
    def __init__(self, right=False):
        self.right = right
    
    def __add__(self, x):
        if self.right:
            return lambda add_right: x + add_right
        return lambda add_left: add_left + x
    
    def __truediv__(self, x):
        if self.right:
            return lambda div_right: x / div_right
        return lambda div_left: div_left / x
    
    
    def _is(self, x):
        if self.right:
            return lambda is_right: x is is_right
        return lambda is_left: x is is_left
    
    def _or(self, x):
        if self.right:
            return lambda or_right: x or or_right
        return lambda or_left: or_left or x
    
    def _and(self, x):
        if self.right:
            return lambda and_right: x and and_right
        return lambda and_left: and_left and x
    
    def __floordiv__(self, x):
        if self.right:
            return lambda floordiv_right: x // floordiv_right
        return  lambda floordiv_left: floordiv_left // x
    
    def __pow__(self, x):
        if self.right:
            return lambda pow_right: x ** pow_right
        return lambda pow_left: pow_left ** x
    
    
    def __not__(self):
        return lambda x: not x
    
    def __or__(self, x):
        if self.right:
            return lambda pipe_or_right: x | pipe_or_right
        return lambda pipe_or_left: pipe_or_left | x

    def __and__(self, x):
        if self.right:
            return lambda xand_right: x | xand_right
        return lambda xand_left: xand_left | x
    
    def __invert__(self):
        return lambda x: ~x
    
    def __call__(self, *args, **kwargs):
        return lambda y: y(*args, **kwargs)
    
fn = _ = Lambda()
    
    
    
    
    
    
    
        
    
    
        

    
        
    
    
    


        
    
    

    