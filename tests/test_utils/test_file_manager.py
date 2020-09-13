# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : CTR Prediction                                                    #
# File    : \test_file_manager.py                                             #
# Python  : 3.8.5                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/j2slab/ctr_prediction                          #
# --------------------------------------------------------------------------- #
# Created       : Thursday, September 10th 2020, 11:45:51 pm                  #
# Last Modified : Thursday, September 10th 2020, 11:45:51 pm                  #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 nov8.ai                                                  #
# =========================================================================== #
#%%
import os

import boto3
from boto3.exceptions import S3UploadFailedError
import pytest
from pytest import mark

from ctr.utils.file_manager import AWSUploader, AWSDownloader, ZipDataExtractor
from ctr.utils.file_manager import copy_file, check_directory, check_s3, rm_directory_tree
# --------------------------------------------------------------------------- #
TEMP_DIR = "./ctr/data/temp/"
BUCKET_NAME = "ctr-prediction"
OBJECT_NAME = "T0_code_tests/testfile.csv"
FILEPATH = "./tests/test_data/testfile.csv"
ZIPFILEPATH = "./tests/test_data/test_data.zip"
EXTRACT_DIR = "./tests/test_data/extract/"
# --------------------------------------------------------------------------- #
#                           Test AWSUploader                                  #
# --------------------------------------------------------------------------- #
@mark.upload
class AWSUploaderTests:
    """ Tests the AWSUploader."""

    def test_upload(self):
        ul = AWSUploader(filepath=FILEPATH,
                         bucket_name=BUCKET_NAME,
                         object_name=OBJECT_NAME)        
        ul.fit_transform()
        assert check_s3(BUCKET_NAME, OBJECT_NAME)

# --------------------------------------------------------------------------- #
#                           Test AWSDownloader                                #
# --------------------------------------------------------------------------- #
@mark.download
class AWSDownloaderTests:
    """ Tests the AWSDownloader."""

    def test_normal_download(self):          
        dl = AWSDownloader(bucket_name=BUCKET_NAME, 
                            object_name=OBJECT_NAME,
                            local_filepath=FILEPATH,
                            force=True)

        dl.fit_transform()  


    def test_aborted_download(self):             
        dl = AWSDownloader(bucket_name=BUCKET_NAME, 
                            object_name=OBJECT_NAME,
                            local_filepath=FILEPATH)

        dl.fit_transform()    

    def test_forced_download(self):             
        dl = AWSDownloader(bucket_name=BUCKET_NAME, 
                            object_name=OBJECT_NAME,
                            local_filepath=FILEPATH,
                            force=True)

        dl.fit_transform()    

# --------------------------------------------------------------------------- #
#                           Test ZipDataExtractor                             #
# --------------------------------------------------------------------------- #
@mark.extract
class ZipDataExtractorTests:
    """ Tests ZipDataExtractor (in case that wasn't already obvious). """

    def test_invalid_zipfile(self):        
        xtr = ZipDataExtractor(zipfile_path="/filedir/file.zip", extract_dir=EXTRACT_DIR,
                               file_type=".pdf")
        with pytest.raises(FileNotFoundError):
            xtr.fit_transform()

    def test_normal_unzip(self):        
        xtr = ZipDataExtractor(zipfile_path=ZIPFILEPATH, extract_dir=EXTRACT_DIR,
                               file_type=".pdf")
        assert xtr.fit_transform(), "Normal unzip didn't work"
        assert len(os.listdir(EXTRACT_DIR)) > 0, "No files were extracted"

    def test_file_exists_no_force(self):        
        xtr = ZipDataExtractor(zipfile_path=ZIPFILEPATH, extract_dir=EXTRACT_DIR,
                               file_type=".pdf")
        assert not xtr.fit_transform(), "Transform didn't return false"
    
    def test_file_exists_w_force(self):        
        xtr = ZipDataExtractor(zipfile_path=ZIPFILEPATH, extract_dir=EXTRACT_DIR,
                               file_type=".pdf", force=True)
        assert xtr.fit_transform(), "Transform didn't return true"    
        assert len(os.listdir(EXTRACT_DIR)) > 0, "Extract directory should not be empty"
        rm_directory_tree(EXTRACT_DIR)
        

        