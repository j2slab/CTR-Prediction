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

import pandas as pd
import boto3
from ctr import AWS_CREDENTIALS 
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

    local_filepath = dirname + filename
    remote_filepath = "00_external_data/" + filename
    
    credentials = pd.read_csv(AWS_CREDENTIALS, dtype=str, index_col=0)
    aws_access_key = credentials["Access key ID"][0]
    aws_secret_key = credentials["Secret access key"][0]
    aws_host = "us-east-2"

    s3 = boto3.client('s3',
                        aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key,
                        region_name=aws_host)
    
    s3.download_file(bucket_name, remote_filepath, local_filepath)
    return True





# %%
