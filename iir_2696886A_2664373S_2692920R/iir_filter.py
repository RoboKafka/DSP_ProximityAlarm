#
# (C) 2020 Bernd Porr, mail@berndporr.me.uk
# Apache 2.0 license
#
import numpy as np
import unittest

class IIR2_filter:
    """2nd order IIR filter"""

    def __init__(self,s):
        """Instantiates a 2nd order IIR filter
        s -- numerator and denominator coefficients
        """
        self.numerator0 = s[0]
        self.numerator1 = s[1]
        self.numerator2 = s[2]
        self.denominator1 = s[4]
        self.denominator2 = s[5]
        self.buffer1 = 0
        self.buffer2 = 0

    def filter(self,v):
        """Sample by sample filtering
        v -- scalar sample
        returns filtered sample
        """
        input = v - (self.denominator1 * self.buffer1) - (self.denominator2 * self.buffer2)
        output = (self.numerator1 * self.buffer1) + (self.numerator2 * self.buffer2) + input * self.numerator0
        self.buffer2 = self.buffer1
        self.buffer1 = input
        return output

class IIR_filter:
    """IIR filter"""
    def __init__(self,sos):
        """Instantiates an IIR filter of any order
        sos -- array of 2nd order IIR filter coefficients
        """
        self.cascade = []
        for s in sos:
            self.cascade.append(IIR2_filter(s))

    def filter(self,v):
        """Sample by sample filtering
        v -- scalar sample
        returns filtered sample
        """
        for f in self.cascade:
            v = f.filter(v)
        return v
    

class unit_test_IIR2_filter(unittest.TestCase):
    soscoef1 = [5.7, 7.3, 3.4, 1, 9, 6]
    input1 = [4, 2, 3, 7]
    output1 = [22.8, -164.6, 1389.9, -11452.9]

    f1 = IIR2_filter(soscoef1)
    output1_test = []
    for val in input1:
        output1_test.append(f1.filter(val))
    
    soscoef2 = [7.6, 1.3, 3.5, 1, 5.9, 2.7]
    input2 = [5, 9, 3, 8]
    output2 = [38.0, -149.3, 830.27, -4399.283]

    f2 = IIR2_filter(soscoef2)
    output2_test = []
    for val in input2:
        output2_test.append(f2.filter(val))

    threshold=1e-04
    def test1(self):
        for i in range(len(self.output1)):
            self.assertTrue(np.abs(self.output1[i]-self.output1_test[i])<self.threshold,"Unit test case failed")
    
    def test2(self):
        for i in range(len(self.output2)):
            self.assertTrue(np.abs(self.output2[i]-self.output2_test[i])<self.threshold,"Unit test case failed")
    


class unit_test_IIR_filter(unittest.TestCase):
    soscoef3 = [[1.2, 2.3, 3.4, 1, 5, 6], [3.21, 4.56, 6.31,1,7,9]]
    input3 = [4, 6, 1, 0]
    output3 = [   15.408,  -110.364,   750.846, -4525.681]

    f3 = IIR_filter(soscoef3)
    output3_test = []
    for val in input3:
        output3_test.append(f3.filter(val))
    
    soscoef4 = [[1.7, 1.3, 1.4, 1, 9, 6], [1.6, 1.3, 3.5, 1, 5.9, 2.7]]
    input4 = [4, 2, 3, 7]
    output4 = [ 1.08800000e+01, -1.39512000e+02,  1.46260480e+03, -1.37433559e+04]

    f4 = IIR_filter(soscoef4)
    output4_test = []
    for val in input4:
        output4_test.append(f4.filter(val))

    threshold=1e-04
    def test3(self):
        for i in range(len(self.output3)):
            self.assertTrue(np.abs(self.output3[i]-self.output3_test[i])<self.threshold,"Unit test case failed")
    
    def test4(self):
        for i in range(len(self.output4)):
            self.assertTrue(np.abs(self.output4[i]-self.output4_test[i])<self.threshold,"Unit test case failed")
    
