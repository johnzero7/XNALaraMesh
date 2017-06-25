# -*- coding: utf-8 -*-
# <pep8 compliant>

import os
import time
import timeit


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__,
                                             (time2 - time1) * 1000.0))
        return ret
    return wrap
