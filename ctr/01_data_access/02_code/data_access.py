# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : CTR Prediction                                                    #
# File    : \01_onboard_data.py                                               #
# Python  : 3.8.5                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/j2slab/ctr_prediction                          #
# --------------------------------------------------------------------------- #
# Created       : Tuesday, September 1st 2020, 12:33:33 am                    #
# Last Modified : Wednesday, September 2nd 2020, 12:49:42 am                  #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 nov8.ai                                                  #
# =========================================================================== #
""" Module responsible for obtaining, staging, and creating the MySQL Database."""
#%%
import os
import pandas as pd
from ctr import DIRECTORIES, SUBDIRECTORIES, get
# --------------------------------------------------------------------------- #


def extract_data(path):
    """Extract required data and place it in the data access input folder."""

