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
HOME = "../../ctr/"
DATA_DIR = "../../data/"
TEST_DIR = "../../tests/"
STEP_DIRECTORIES = {"pipeline": "00_pipeline", "data_access": "01_data_access",
               "data_preprocessing": "02_data_preprocessing", "eda": "03_eda",
               "data_preparation": "04_data_preparation", 
               "model_development": "05_model_development",
               "model_selection": "06_model_selection",
               "model_evaluation": "07_model_evaluation",
               "deployment": "08_deployment",
               "documentation": "09_documentation"}

STEP_SUBDIRECTORIES = {"inputs": "01_inputs", "code": "02_code", "outputs": "03_outputs",
                      "temp": "04_temp"}               


# --------------------------------------------------------------------------- #
#                                  LOGGING                                    #
# --------------------------------------------------------------------------- #
LOGFILE_DIR = "../../ctr/log/"
LOGFILE_NAME = "ctr.log"
LOGFILE_PATH = os.path.join(LOGFILE_DIR, LOGFILE_NAME)
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_console_handler():
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(FORMATTER)
    return ch

def get_file_handler():
    fh = logging.handlers.TimedRotatingFileHandler(LOGFILE_PATH, when="midnight")
    fh.setFormatter(FORMATTER)
    return fh

def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
