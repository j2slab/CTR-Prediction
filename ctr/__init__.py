# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : CTR Prediction                                                    #
# File    : \__init__.py                                                      #
# Python  : 3.8.5                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/j2slab/ctr_prediction                          #
# --------------------------------------------------------------------------- #
# Created       : Monday, August 31st 2020, 8:36:27 pm                        #
# Last Modified : Saturday, September 5th 2020, 3:58:06 am                    #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 nov8.ai                                                  #
# =========================================================================== #
"""Top-level package for Click Through Rate Prediction."""
#%%
from collections import OrderedDict
import logging
import os
import sys
# --------------------------------------------------------------------------- #
#                                CONSTANTS                                    #
# --------------------------------------------------------------------------- #
__author__ = """John James"""
__email__ = 'john.james@nov8.ai'
__version__ = '0.1.0'
# Filenames and Directories

DATA_DIR = "../data/"
EXTERNAL_DATA_DIR = "../data/external/"
RAW_DATA_DIR = "../data/raw/"
PREPROCESSED_DATA_DIR = "../data/preprocessed/"
CLEAN_DATA_DIR = "../data/clean/"
PROCESSED_DATA_DIR = "../data/processed/"

KDD_DATA_FILENAME = "kddcup2012-track2.zip"
AWS_CREDENTIALS = "./credentials/user_credentials.csv"
    
# --------------------------------------------------------------------------- #
#                                  LOGGING                                    #
# --------------------------------------------------------------------------- #
LOGFILE_PATH = "./log/ctr.log"
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_console_handler():
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(FORMATTER)
    return ch

def get_file_handler():
    fh = logging.handlers.TimedRotatingFileHandler(LOGFILE_PATH, when="midnight")
    fh.setFormatter(FORMATTER)
    return fh

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        logger.addHandler(get_console_handler())
        logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
