# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : CTR Prediction                                                    #
# File    : \file_manager.py                                                  #
# Python  : 3.8.5                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/j2slab/ctr_prediction                          #
# --------------------------------------------------------------------------- #
# Created       : Wednesday, September 2nd 2020, 9:52:59 pm                   #
# Last Modified : Thursday, September 10th 2020, 10:54:29 pm                  #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 nov8.ai                                                  #
# =========================================================================== #
""" File management utilities."""
#%%
from abc import ABC, abstractmethod
import configparser
import csv
import inspect
import os
import shutil
import zipfile

import boto3, botocore
from botocore.exceptions import ClientError
import mysql.connector
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from ctr import get_logger, CONFIG_FILEPATH
from ctr.utils.print import print_list
# --------------------------------------------------------------------------- #
#                           TRANSFORMERS                                      #
# --------------------------------------------------------------------------- #
class AbstractX4ma(ABC, BaseEstimator, TransformerMixin):
    """ Abstract transformer class defining interface for all transformers."""

    def fit(self):
        """ Fits the transformer to the data."""
        return self

    @abstractmethod
    def transform(self):
        """ Performs the transformation."""
        pass

    def fit_transform(self):
        """ Combines the fit and transform methods."""
        self.fit()
        return self.transform() 

    def predict(self, X):
        """ Exists to meet scikit-learn's Pipeline class predict method requirement."""  
        pass
# --------------------------------------------------------------------------- #
class AWSUploader(AbstractX4ma):
    """ Uploads file to an AWS S3 bucket.

    Parameters
    ----------
    filepath : str
        The path to the file to be uploaded.

    bucket_name : str
        The name of the AWS bucket 

    object_name : str
        The full name of the object, including its directory path on AWS
    """    


    def __init__(self, filepath, bucket_name, object_name=None):
        self.filepath = filepath
        self.bucket_name = bucket_name
        self.object_name = object_name        
        self._logger = get_logger(self.__class__.__name__)               

    def transform(self):
        """ Performs the upload to the designated S3 bucket."""

        if self.object_name is None:
            self.object_name = os.path.basename(self.filepath)

        config = configparser.ConfigParser()
        config.read(CONFIG_FILEPATH)

        # Upload the file
        s3 = boto3.client('s3',
            aws_access_key_id=config['AWS']['access_key'],
            aws_secret_access_key=config['AWS']['secret_key'],
            region_name=config['AWS']['region'])
        try:
            s3.upload_file(self.filepath, self.bucket_name, self.object_name)
        except ClientError as e:
            self._logger.error(e)
            return False
        return True        


 
# --------------------------------------------------------------------------- #
class AWSDownloader(AbstractX4ma):
    """ Downloads file from an AWS S3 bucket. 

    Parameters
    ----------
    bucket_name : str
        The name of the AWS bucket 

    object_name : str
        The full name of the object, including its directory path on AWS

    local_filepath : str
        The local destination file path.

    """    

    def __init__(self, bucket_name, object_name, local_filepath, force=False):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.local_filepath = local_filepath
        self.force = force
        self._logger = get_logger(self.__class__.__name__)                

    def transform(self):
        """Downloads the dataset from the AWS S3 Bucket."""

        if not self.force and os.path.exists(self.local_filepath):
            filename = os.path.basename(self.local_filepath)
            dirname = os.path.dirname(self.local_filepath)
            self._logger.info("File {f} exists at {d}. Download aborted."\
                .format(f=filename, d=dirname))
            return False

        else:
            check_directory(os.path.dirname(self.local_filepath))
                        
            config = configparser.ConfigParser()
            config.read(CONFIG_FILEPATH)

            s3 = boto3.client('s3',
                        aws_access_key_id=config['AWS']['access_key'],
                        aws_secret_access_key=config['AWS']['secret_key'],
                        region_name=config['AWS']['region'])
            try:
                self._logger.info("Downloading {f} from Amazon S3 Bucket.".format(f=self.object_name))
                s3.download_file(self.bucket_name, self.object_name, self.local_filepath)           

            except s3.exceptions.NoSuchBucket as error:                                
                self._logger.error(error)
                raise Exception(error)

            except botocore.exceptions.ParamValidationError as error:
                self._logger.error('Invalid parameters')
                raise ValueError('The parameters you provided are incorrect: {}'.format(error))                

            self._logger.info("Data download completed successfully.")   
            return True         

# --------------------------------------------------------------------------- #
class ZipDataExtractor(AbstractX4ma):
    """ Extracts files from zip archives."""

    def __init__(self, zipfile_path, extract_dir, file_type=".txt", force=False):        
        self.zipfile_path = zipfile_path
        self.extract_dir = extract_dir
        self.file_type = file_type
        self.force =force
        self._logger = get_logger(self.__class__.__name__)                

    def _extract_data(self, zipfile_name=None, zipfile_dir=None):
        """Extracts all members from zip file recursively."""
        extracting = "Unzipping {f}".format(f=zipfile_name)
        self._logger.info(extracting)

        # Extract archive to directory and list its members.        
        filepath = zipfile_dir + zipfile_name    
        extract_dir = os.path.splitext(filepath)[0]+'/'  
        try:      
            archive = zipfile.ZipFile(filepath)
        except IOError as e:
            self._logger.error(e)
            raise FileNotFoundError(e)
        archive.extractall(extract_dir)
        members = archive.namelist()    
        archive.close()

        # Store members of requested file type to extract directory. 
        for member in members:
            if os.path.splitext(member)[1] == self.file_type:
                self._logger.info("Extracting {f}".format(f=member))
                src_path = extract_dir + member
                copy_file(src_path, dest_dir=self.extract_dir)

            elif os.path.splitext(member)[1] == '.zip':
                self._extract_data(zipfile_name=member, zipfile_dir=extract_dir)            
                
        return extract_dir


    def transform(self):
        """ Extracts requested data to designated directory."""
        if os.path.exists(self.extract_dir) and len(os.listdir(self.extract_dir)) > 0 and \
            self.force is False:
            self._logger.info("Data exists in the extract directory and force=False. Aborting extraction.")
            return False                    
        
        check_directory(self.extract_dir)       
        zipfile_name = os.path.basename(self.zipfile_path)
        zipfile_dir = os.path.dirname(self.zipfile_path) + "/"
        self._extract_data(zipfile_name=zipfile_name, zipfile_dir=zipfile_dir)
        self._logger.info("Extraction complete.")
        return True
    

   
# --------------------------------------------------------------------------- #
#                          FILE HELPER FUNCTIONS                              #
# --------------------------------------------------------------------------- #
def tab_to_csv(txtfile, csvfile):
    """ Converts a file from tab delimited to comma delimited format."""

    with open(txtfile, 'r') as infile, open(csvfile, 'w') as outfile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        writer = csv.writer(outfile)
        writer.writerows(lines)         

    return True

def move_file(src_path, dest_dir, force=False):
    """ Moves a file and its metadata from the src_path to the dest_dir."""

    check_directory(dest_dir)    

    filename = os.path.basename(src_path)
    dest_filepath = dest_dir + filename

    if os.path.exists(dest_filepath) and not force:
        return True
    try:
        shutil.move(src_path, dest_dir)
    except OSError as e:
        raise(e)

    return True


def copy_file(src_path, dest_dir, force=False):
    """ Copies a file and its metadata from the src_path to the dest_dir."""

    check_directory(dest_dir)    

    filename = os.path.basename(src_path)
    dest_filepath = dest_dir + filename

    if os.path.exists(dest_filepath) and not force:
        return True
    try:
        shutil.copy2(src_path, dest_dir)
    except OSError as e:
        raise(e)

    return True

def rm_directory_tree(directory):
    """ Recursively removes a directory and its subdirectories and files.""" 
    
    try:
        shutil.rmtree(directory)
    except OSError as e:
        raise(e)
    
    return True

def check_directory(directory):
    """ If directory doesn't exist, it is created."""

    if not os.path.exists(directory):
        make_directory(directory)


def make_directory(directory):
    """ Creates the designated directory."""
    
    try:
        os.mkdir(directory)
    except OSError as e:
        raise(e)
        
    return True

def check_s3(bucket_name, file_path):
    """ Checks if a file exists in a given AWS S3 bucket."""
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket_name, file_path).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            msg = "Object {o} does not exist in {b}."\
                .format(o=file_path, b=bucket_name)
            print(msg)
            return False
        else:
            raise OSError(e)
    return True

