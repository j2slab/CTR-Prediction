# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : CTR Prediction                                                    #
# File    : \data_access.py                                                   #
# Python  : 3.8.5                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/j2slab/ctr_prediction                          #
# --------------------------------------------------------------------------- #
# Created       : Wednesday, September 2nd 2020, 2:39:23 am                   #
# Last Modified : Saturday, September 5th 2020, 5:30:13 pm                    #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 nov8.ai                                                  #
# =========================================================================== #
""" Module responsible for obtaining, staging, and creating the MySQL Database."""
#%%
import inspect
import os
import shutil
import zipfile

import mysql.connector

from ctr import get_logger
from ctr.utils.file_manager import copy_file, rm_directory_tree, make_directory
from ctr.utils.file_manager import tab_to_csv, download_aws
from ctr.utils.print import print_list
# --------------------------------------------------------------------------- #

class KDDCupData:
    """ Downloads, extracts and stages the raw KDD Cup Dataset. 

    Parameters
    ----------
    zip_filename : str
        The name of the zip file including the ".zip" extension.

    ext_data_dir : str
        The directory containing the zip file

    raw_data_dir : str
        The directory into which the files are stored.

    csv_data_dir : str
        The directory into which csv converted files are stored.        

    file_ext : str (optional, default=None)
        The file extension for files to extract. If None, all files will
        be extracted.

    """    

    def __init__(self, bucket_name, zip_filename, ext_data_dir, raw_data_dir, 
                 csv_data_dir, file_ext=None):
        self.bucket_name = bucket_name
        self.zip_filename = zip_filename
        self.ext_data_dir = ext_data_dir
        self.raw_data_dir = raw_data_dir
        self.csv_data_dir = csv_data_dir
        self.file_ext = file_ext        

    def _initialize(self):
        """ Prepares raw data directory, or returns False if data exists."""
        me = self.__class__.__name__ + " : " + inspect.stack()[0][3] 
        logger = get_logger(me)
        starting_extraction = "Initiating data extraction process."        
        logger.info(starting_extraction)
        
        data_exists = "The target directory is non empty. Do you wish to overwrite the data? [Y/N]"                

        if ".zip" in self.zip_filename:
            if os.path.exists(self.raw_data_dir):
                if len(os.listdir(self.raw_data_dir)) > 0:                
                    overwrite = input(data_exists)
                    if 'y' in overwrite.lower():
                        rm_directory_tree(self.raw_data_dir)
                        rm_directory_tree(self.csv_data_dir)
                        make_directory(self.raw_data_dir)
                        make_directory(self.csv_data_dir)
                        return True
                    else:
                        logger.info("Data extraction aborted")
                        return False
                else:
                    return True
            else:
                make_directory(self.raw_data_dir)
                make_directory(self.csv_data_dir)                
                return True
        else:
            raise TypeError("File is not a zipfile format.")

    def _download(self):
        """Downloads the dataset from the AWS S3 Bucket."""
        me = self.__class__.__name__ + " : " + inspect.stack()[0][3] 
        logger = get_logger(me)              
        proceed = True  

        data_exists = "The external data directory is not empty. \
            Are you sure that you want to download this dataset from AWS. \
                It may take a while."

        ext_data_file = self.ext_data_dir + self.zip_filename
        
        if os.path.exists(ext_data_file):
            overwrite = input(data_exists)
            proceed = True if 'y' in overwrite.lower() else False

        if proceed:
            logger.info("Downloading data from Amazon S3 Bucket")  
            download_aws(bucket_name=self.bucket_name, filename=self.zip_filename,
                         dirname=self.ext_data_dir)
            logger.info("Data download completed successfully.")
            return True
        else:
            logger.info("Download aborted.")
            return False

    def _extract_data(self, zipfile_name=None, base_path=None):
        """Extracts all members from zip file recursively."""
        me = self.__class__.__name__ + " : " + inspect.stack()[0][3] 
        logger = get_logger(me)        
        extracting = "Extracting {f}".format(f=zipfile_name)
        logger.info(extracting)
        
        # Format a path based upon the base of the zip file name
        filepath = base_path + zipfile_name    
        extract_path = filepath.strip('.zip')+'/'
        # Obtain the zipfile object and extract the members
        archive = zipfile.ZipFile(filepath)
        archive.extractall(extract_path)
        members = archive.namelist()    
        archive.close()

        for member in members:
            if member[-4:] == self.file_ext:

                logger.info("Staging {f}".format(f=member))
                src_path = extract_path + member
                copy_file(src_path, dest_dir=self.raw_data_dir)

            elif member[-4:] == '.zip':
                    self._extract_data(zipfile_name=member, base_path=extract_path)            
                
        return extract_path

    def _get_raw_data(self):
        """ Obtains raw data from external data."""
        me = self.__class__.__name__ + " : " + inspect.stack()[0][3] 
        logger = get_logger(me)
        logger.info("Obtaining raw data from {d}.".format(d=self.ext_data_dir))             
        proceed = True

        # If the external source file doesn't exist, download it from AWS
        source_filepath = self.ext_data_dir + self.zip_filename
        if not os.path.exists(source_filepath):
            proceed = self._download()
        
        if proceed:
            self._extract_data(zipfile_name=self.zip_filename, base_path=self.ext_data_dir)
            #TODO: call database creator
            return True
        else:
            return False        
        
    def stage(self):
        me = self.__class__.__name__ + " : " + inspect.stack()[0][3] 
        logger = get_logger(me)
        logger.info("Data access pipeline initiated.")     
        proceed = True

        if os.path.exists(self.raw_data_dir):
            contents = os.listdir(self.raw_data_dir)
            if len(contents) > 0:
                print("The raw data directory is not empty. It contains:")
                print_list(contents)
                overwrite = input("Do you wish to overwrite this data.")
                proceed = 'y' in overwrite.lower() 
                
        if proceed:
            self._get_raw_data()

def main():

    AWS_BUCKET_NAME = "ctr-prediction"
    EXT_DATA_DIR = "./data/external/"
    RAW_DATA_DIR = "./data/raw/"
    CSV_DATA_DIR = "./data/csv/"
    KDD_DATA_FILENAME = "kddcup2012-track2.zip"

    kdd = KDDCupData(bucket_name=AWS_BUCKET_NAME, zip_filename=KDD_DATA_FILENAME, 
                     ext_data_dir=EXT_DATA_DIR, raw_data_dir=RAW_DATA_DIR, 
                     csv_data_dir=CSV_DATA_DIR, file_ext=".txt")
    kdd.stage()
    
    

if __name__ == "__main__":
    main()
    
#%%
    

