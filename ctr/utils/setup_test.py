# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : CTR Prediction                                                    #
# File    : \paths.py                                                         #
# Python  : 3.8.5                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/j2slab/ctr_prediction                          #
# --------------------------------------------------------------------------- #
# Created       : Wednesday, September 2nd 2020, 9:52:59 pm                   #
# Last Modified : Wednesday, September 2nd 2020, 9:53:00 pm                   #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 nov8.ai                                                  #
# =========================================================================== #
""" Contains path information for the project."""
#%%
import sys
import os
import shutil
from ctr import HOME, TEST_DIR, STEP_DIRECTORIES, STEP_SUBDIRECTORIES, get_logger

# --------------------------------------------------------------------------- #
def main(path=None):    

    logger = get_logger()    
        
    for step in STEP_DIRECTORIES.values():
        step = os.path.join(TEST_DIR, step)        
        try: 
            os.mkdir(step)
            msg = "Directory {d} created.".format(d=step)
            logger.info(msg)
            try:
                shutil.copy2(os.path.join(HOME,"__init__.py"), step)
            except: 
                pass
        except FileExistsError:
            msg = "Directory {d} already exists.".format(d=step)
            logger.info(msg)
    
    
if __name__ == "__main__":
    main()

# %%
