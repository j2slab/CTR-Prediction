# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : CTR Prediction                                                    #
# File    : \db_manager.py                                                    #
# Python  : 3.8.5                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/j2slab/ctr_prediction                          #
# --------------------------------------------------------------------------- #
# Created       : Thursday, September 10th 2020, 1:24:50 am                   #
# Last Modified : Thursday, September 10th 2020, 1:25:40 am                   #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 nov8.ai                                                  #
# =========================================================================== #
#%%
from datetime import date, time, datetime 
import os
import mysql.connector as mysql
from configparser import ConfigParser

from ctr import db_config_filepath
# --------------------------------------------------------------------------- #

dtypes = {int: "INTEGER", float: "DOUBLE", date: "DATE", time: "TIME", 
          datetime : "TIMESTAMP", str: "VARCHAR"}
config_filename = "../../ctr/credentials/db_config.ini"          

class KDDb:
    """ KDD database class"""

    def __init__(self, name):
        """Creates an instance encapsulating MySQL functionality."""
        self.name = name

    def connect(self):

    def _read_db_config(filename=config_filename, section='mysql'):
        """ Reads the database configuration file and returns a dictionary object.
        
        Parameters
        ----------
        filename : str
            The filename containing the configuration

        section : str
            section of the database configuration

        Returns
        -------
        dict : a dictionary of database parameters
        
        """
        # create parser and read ini configuration file
        parser = ConfigParser()
        parser.read(filename)

        # get section, default to mysql
        db = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file'.format(section, filename))

        return db

    def connect(self):
        """ Returns the database connection. """
        return self.db

    def show_databases(self):
        """ Prints the database to console."""
        databases = self.db.cursor().fetchall()
        for database in databases:
            print(database)

    def create_table(self, spec):
        """ Creates a table based upon a specification dictionary."""
        table_name = spec.keys()
        print(table_name)

        self.connect()
        self.db.cursor().execute("CREATE DATABASE {t}".format(t=table_name))

table = {"test": {"id": str, "name": str, "height": float, "age": int, "bday":date, "btime": time, "timestamp": datetime,}}
assert os.path.exists("../../ctr/credentials/db_config.ini")
# kdd = KDDb()
# kdd.create_table(table)

