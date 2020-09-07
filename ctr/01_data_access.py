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

from ctr import KDD_DATA_FILENAME, get_logger
# --------------------------------------------------------------------------- #

class ExtractZipData:
    """ Extracts and stores designated files from a zip archive.

    Parameters
    ----------
    zip_filename : str
        The name of the zip file including the ".zip" extension.

    src_dir : str
        The directory containing the zip file

    tgt_dir : str
        The directory into which the files are stored.

    file_ext : str (optional, default=None)
        The file extension for files to extract. If None, all files will
        be extracted.

    """
    def __init__(self, zip_filename, src_dir, tgt_dir, file_ext=None):
        self.zip_filename = zip_filename
        self.src_dir = src_dir
        self.tgt_dir = tgt_dir
        self.file_ext = file_ext        

    def _initialize(self):
        """ Prepares raw data directory, or returns False if data exists."""
        me = self.__class__.__name__ + " : " + inspect.stack()[0][3] 
        logger = get_logger(me)

        starting_extraction = "Initiating data extraction process."        
        data_exists = "The target directory is non empty. Do you wish to overwrite the data? [Y/N]"        

        logger.info(starting_extraction)

        if ".zip" in self.zip_filename:
            if os.path.exists(self.tgt_dir):
                if len(os.listdir(self.tgt_dir)) > 0:                
                    overwrite = input(data_exists)
                    if 'y' in overwrite.lower():
                        try:
                            shutil.rmtree(self.tgt_dir)
                            try:
                                os.mkdir(self.tgt_dir)
                            except OSError as e:
                                print(e)
                        except OSError as e:                            
                            logger.error(e)
                        return True
                    else:
                        logger.info("Data extraction aborted")
                        return False
            else:
                try:
                    os.mkdir(self.tgt_dir)
                except OSError as e:
                    print(e)
                return True
        else:
            raise TypeError("File is not a zipfile format.")

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
            if member[-4:] == '.txt':
                src_path = extract_path + member
                shutil.copy2(src_path, self.tgt_dir) 
                logger.info("Staging {f}".format(f=member))

            elif member[-4:] == '.zip':
                    self._extract_data(zipfile_name=member, base_path=extract_path)            
                
        return extract_path

    def _finalize(self):
        """ Cleans up extracted files from source directory."""
        me = self.__class__.__name__ + " : " + inspect.stack()[0][3] 
        logger = get_logger(me)
        logger.info("Data extraction complete.")

    def extract(self):
        if self._initialize():
            self._extract_data(zipfile_name=self.zip_filename, base_path=self.src_dir)
            self._finalize()

def main():

    SRC_DIR = "../data/external/"
    TGT_DIR = "../data/raw/"
    extractor = ExtractZipData(zip_filename=KDD_DATA_FILENAME, src_dir=SRC_DIR,
                               tgt_dir=TGT_DIR, file_ext=".txt")
    extractor.extract()
    
    

if __name__ == "__main__":
    main()
    
    

