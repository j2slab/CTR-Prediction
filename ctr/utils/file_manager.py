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
""" File management utilities."""
#%%
import csv
import os
import shutil

from boto.s3.connection import S3Connection
# --------------------------------------------------------------------------- #
def tab_to_csv(txtfile, csvfile):
    """ Converts a file from tab delimited to comma delimited format."""

    with open(txtfile, 'r') as infile, open(csvfile, 'w') as outfile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        writer = csv.writer(outfile)
        writer.writerows(lines)         

    return True

def copy_file(src_path, dest_dir):
    """ Copies a file and its metadata from the src_path to the dest_dir."""
    
    try:
        shutil.copy2(src_path, dest_dir)
    except OSError as e:
        print(e)

    return True

def rm_directory_tree(directory):
    """ Recursively removes a directory and its subdirectories and files.""" 
    
    try:
        shutil.rmtree(directory)
    except OSError as e:
        print(e)
    
    return True

def make_directory(directory):
    """ Creates the designated directory."""
    
    try:
        os.mkdir(directory)
    except OSError as e:
        print(e)
        
    return True

def download_aws(bucket_name, filename, dirname):
    """ Downloads a file from an Amazon AWS Bucket to the designated directory."""

    aws_connection = S3Connection()
    bucket = aws_connection.get_bucket(bucket_name)
    key = bucket.get_key(filename)
    key.get_contents_to_filename(dirname)    
    return True


# %%
