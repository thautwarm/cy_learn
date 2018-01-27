# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 00:13:54 2018

@author: twshe
"""


import unittest
from xylearn.comp.operator import Lambda
_ = Lambda()


def code_gen_dualop():
        templates = (
        " x = _ {op} right "
        " self.assertEqual({left} {op} {right}, x({left})) "
        " x = _.r {op} {left} "
        " self.assertEqual({left} {op} {right}, x({right})) ")
        
        left = 10
        right = 3
        codes = []
        
        for op in {'+', '-', '*', 
                   '/','//', '@',
                   '%', '^', '&',
                   '|'}:
            
            codes.append(
                    templates.format(op=op, left=left, right=right))
            
            
            
        
class TestLambda(unittest.TestCase):
    
    def dual_operator(self):
        pass
    
        
        