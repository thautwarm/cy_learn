# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 02:38:28 2018

@author: misakawa
"""
from functools import reduce
from xylearn.comp.operator import postfix, Holder, KeyPair


from typing import Callable, List, TypeVar, Union
T = TypeVar('T')
G = TypeVar('G')


__all__ = [
        'and_then', 
        'sexpr'
]

def _cause_type_err(e):
    raise TypeError(e)

def and_then(*f: Union[List, Callable]):
    """
    from xylearn.comp.operator import kv
    and_then(
            [np.transpose, (2, 0, 1)],
            np.shape,
            [np.matmul, hold@np.mean],
            [print, kv['sep', ';']]
    )(np.array([[1,2], [3,4]])) 
    
    ->
    
    arr = np.array([[1,2], [3,4]])
    arr = np.transpose(arr, (2, 0, 1))
    arr = np.shape(arr)
    arr = np.matmul(arr, np.mean(arr))
    arr = print(arr, sep=';')
    """
    
    # TODO: use `GroupBy` to optimize this one
    f = [fn if callable(fn) else 
                (lambda x: fn[0](
                        x, # arg
                        *(arg(x)  # varargs
                        if isinstance(arg, Holder) else arg for arg in filter(lambda _: not isinstance(_, KeyPair), fn[1:]))
                        , 
                        **{k: v for k, v in filter(lambda _: isinstance(_, KeyPair), fn[1:])} # kwargs
                        ))
            if isinstance(fn, list) else
                _cause_type_err("Unknow type during `and_then` pipeline.")
            for fn in f]

    def apply(x):
        return reduce(postfix, f, x)

    return apply
        
def sexpr(head, *tail):
    """
    pretend to be s-expression.
    sexpr(lambda x, y: x-y, 2, 3) -> -1
    sexpr(
        lambda x: x*2,
        (lambda y, z: y//5 + z, 10, (sum, [1, 2]))) -> (10 // 5 + (sum([1, 2]))) * 2
    """
    if isinstance(head, tuple):
        head = sexpr(*head)
        
    return head(*map(lambda _: sexpr(*_) if isinstance(_, tuple) else _, 
                     tail))

    
    

