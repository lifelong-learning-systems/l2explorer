"""
Copyright © 2021 The Johns Hopkins University Applied Physics Laboratory LLC
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import itertools
import numpy as np
from .utils import l2random

"""
The function don't use context. The input is still present for 
compatibility
"""
def fixed_set(value_list):
    list_gen = itertools.cycle(value_list)    
    def f(context=None, count=1):
        lst = [next(list_gen) for  _ in range(count)]
        return lst
    return f

def constant(value):
    def f(context=None):
        return value
    return f

def binomial(n, p):
    def f(context=None):
        return l2random.binomial(n, p)
    return f

def choice(lst):
    # randint requires a 1-d array. The method below allows for list elements to be sublists.
    lst_len = len(lst)    
    def fcn(context=None):
        return lst[l2random.randint(0, lst_len)]
    return fcn    

def perturb(array_, limits=(0.0,1.0), noise=0.1):
    min_, max_ = limits
    def fcn(context=None):        
        perturbed_array = np.array(array_) + l2random.uniform(-noise, +noise)
        clipped_array = np.minimum(max_, np.maximum(min_, perturbed_array))
        return clipped_array
    return fcn


# --------------------------
# conditional distributions

def uniform_box_c(xlims, ylims):
    (xlow, xhigh) = xlims
    (ylow, yhigh) = ylims
    def f(context, count=1):
        (cx,cy) = context[0]
        xlocs = l2random.uniform(xlow, xhigh, size=(count,1)) + cx
        ylocs = l2random.uniform(ylow, yhigh, size=(count,1)) + cy
        locs = np.hstack([xlocs, ylocs])
        return locs
    return f   

def annulus_c(rmin, rmax):
    def f(context, count=1):
        (cx,cy) = context[0]
        r = l2random.uniform(rmin,rmax,size=(count,1))
        theta = l2random.uniform(0,2*np.pi,size=(count,1))
        x = cx + (r * np.sin(theta))
        y = cy + (r * np.cos(theta)) 
        return np.concatenate((x,y), axis=1)
    return f

def gaussian_c(cov):
    def f(context, count=1):
        (cx,cy) = context[0]
        pts = l2random.multivariate_normal(mean=[cx,cy], cov=cov, size=(count,))
        return pts
    return f
