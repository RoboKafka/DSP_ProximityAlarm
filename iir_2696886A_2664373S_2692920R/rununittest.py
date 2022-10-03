# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 23:31:41 2022

@author: Group 65
"""

import unittest
from iir_filter import unit_test_IIR2_filter
from iir_filter import unit_test_IIR_filter

if __name__=='__main__':
    unittest.main(defaultTest=["unit_test_IIR2_filter.test1","unit_test_IIR2_filter.test2","unit_test_IIR_filter.test3","unit_test_IIR_filter.test4"])
    