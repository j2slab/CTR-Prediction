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
import logging.handlers
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
CONFIG_FILEPATH = "config.ini"
KDD_DATA_FILENAME = "kddcup2012-track2.zip"
KDD_DATA_FILEPATH_AWS = "00_external_data/" + KDD_DATA_FILENAME
KDD_DATA_FILEPATH_LOCAL = EXTERNAL_DATA_DIR + KDD_DATA_FILENAME
KDD_BUCKET_NAME_AWS = "ctr-prediction"
# Raw Data Filenames
RAW_DATA_FILENAMES = {"training": "training.txt", "user": "userid_profile.txt",
                      "description": "descriptionid_tokensid.txt",
                      "keyword": "purchasedkeywordid_tokensid.txt",
                      "query": "queryid_tokensid.txt",
                      "title": "titleid_tokensid.txt"}
    
# --------------------------------------------------------------------------- #
#                                  LOGGING                                    #
# --------------------------------------------------------------------------- #
LOGFILE_PATH = "./ctr/log/ctr.log"
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
