# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : CTR Prediction                                                    #
# File    : \format.py                                                        #
# Python  : 3.8.5                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/j2slab/ctr_prediction                          #
# --------------------------------------------------------------------------- #
# Created       : Tuesday, September 8th 2020, 5:32:51 pm                     #
# Last Modified : Tuesday, September 8th 2020, 5:33:05 pm                     #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 nov8.ai                                                  #
# =========================================================================== #
"""Miscellaneous formatting functions."""
#%%
import re
import random
import string
import textwrap

def proper(s):
    """Strips then capitalizes each word in a string.""" 
    s = s.replace("-", " ").title()
    s = s.replace("_", " ").title()
    return s    

def snake(s):
    """Converts string to snake case suitable for filenames."""
    s = re.sub(r"[^a-zA-Z0-9._// ]+", '', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    s = s.replace(" ", "_")
    pattern = '_' + '{2,}'
    s = re.sub(pattern, '_', s)
    return s

def format_text(x):
    x = " ".join(x.split())
    formatted = textwrap.fill(textwrap.dedent(x))
    return formatted        


# %%
