#!/usr/bin/env python

"""
This code is simplified version of DBSReaderModel.py class adopted to use as-is
with Flask and (Flask+uWSGI) frameworks). The congiguration is adopted to
use in modified code. We only used 3 DBS APIs: files, blocks, datasets
and strip off input parameter validation and security authentication decorators.
"""

import os
import re
import sys
import json
import traceback
import logging as logger


# WMCore modules
from WMCore.WebTools.RESTModel import RESTModel
from WMCore.Configuration import Configuration

from WMCore.Database.DBCore import DBInterface

# DBS modules
from dbs.business.DBSDataset import DBSDataset
from dbs.business.DBSBlock import DBSBlock
from dbs.business.DBSFile import DBSFile
from dbs.utils.dbsException import dbsException, dbsExceptionCode
from dbs.utils.dbsExceptionHandler import dbsExceptionHandler
from dbs.utils.DBSInputValidation import *

# load secrets
dbs3_secrets = json.load(open('/path/dbs_secrets.json'))

# get viewnames -> instance names list
view_mapping = { "default": { "DBSReader": ["dev/global"]}, "prod": { "DBSReader": ["prod/global"]}, "preprod": { "DBSReader": ["int/global"]}, "dev": { "DBSReader": ["dev/global"]} }

# instance name : connecturls, {reader needed roles, writer needed roles}
db_mapping = {'int/global': [dbs3_secrets,  {'reader':{},'writer':{'dbs': 'operator', 'dataops': 'production-operator'}}]}
config = Configuration()

config.component_('Webtools')
config.Webtools.port = 8252
config.Webtools.thread_pool = 15
config.Webtools.log_screen = False
config.Webtools.proxy_base = 'True'
config.Webtools.application = 'dbs'
config.Webtools.environment = 'production'

config.component_('database')
config.database.connectUrl = dbs3_secrets['connectUrl']
config.database.dbowner = dbs3_secrets['databaseOwner']

config.component_('dbs')
config.dbs.title = 'DBS Server'
config.dbs.description = 'CMS DBS Service'
config.dbs.section_('views')
config.dbs.admin = 'cmsdbs'
config.dbs.default_expires = 900
config.dbs.instances = list(set([i for r in view_mapping['preprod'].values() for i in r]))

class DBSReaderModel(RESTModel):
    """
    DBS3 Server API Documentation
    """
    def __init__(self, config, dbi=None):
        """
        All parameters are provided through DBSConfig module
        """
        config.__dict__['default_expires'] = config.dbs.default_expires
        RESTModel.__init__(self, config)
        dbowner = config.database.dbowner
        if dbi:
            self.dbi = dbi
            self.logger = logger
        self.dbsDataset = DBSDataset(self.logger, self.dbi, dbowner)
        self.dbsFile = DBSFile(self.logger, self.dbi, dbowner)
        self.dbsBlock = DBSBlock(self.logger, self.dbi, dbowner)

    def listDatasets(self, dataset="", parent_dataset="", is_dataset_valid=1,
        release_version="", pset_hash="", app_name="", output_module_label="", global_tag="",
        processing_version=0, acquisition_era_name="", run_num=-1,
        physics_group_name="", logical_file_name="", primary_ds_name="", primary_ds_type="",
        processed_ds_name='', data_tier_name="", dataset_access_type="VALID", prep_id='', create_by="", last_modified_by="",
        min_cdate='0', max_cdate='0', min_ldate='0', max_ldate='0', cdate='0',
        ldate='0', detail=False, dataset_id=-1):
        """
        API to list dataset(s) in DBS
        * You can use ANY combination of these parameters in this API
        * In absence of parameters, all valid datasets known to the DBS instance will be returned

        :param dataset:  Full dataset (path) of the dataset
        :type dataset: str
        :param parent_dataset: Full dataset (path) of the dataset
        :type parent_dataset: str
        :param release_version: cmssw version
        :type release_version: str
        :param pset_hash: pset hash
        :type pset_hash: str
        :param app_name: Application name (generally it is cmsRun)
        :type app_name: str
        :param output_module_label: output_module_label
        :type output_module_label: str
        :param global_tag: global_tag
        :type global_tag: str
        :param processing_version: Processing Version
        :type processing_version: str
        :param acquisition_era_name: Acquisition Era
        :type acquisition_era_name: str
        :param run_num: Specify a specific run number or range. Possible format are: run_num, 'run_min-run_max' or ['run_min-run_max', run1, run2, ...].
        :type run_num: int,list,str
        :param physics_group_name: List only dataset having physics_group_name attribute
        :type physics_group_name: str
        :param logical_file_name: List dataset containing the logical_file_name
        :type logical_file_name: str
        :param primary_ds_name: Primary Dataset Name
        :type primary_ds_name: str
        :param primary_ds_type: Primary Dataset Type (Type of data, MC/DATA)
        :type primary_ds_type: str
        :param processed_ds_name: List datasets having this processed dataset name
        :type processed_ds_name: str
        :param data_tier_name: Data Tier
        :type data_tier_name: str
        :param dataset_access_type: Dataset Access Type ( PRODUCTION, DEPRECATED etc.)
        :type dataset_access_type: str
        :param prep_id: prep_id
        :type prep_id: str
        :param create_by: Creator of the dataset
        :type create_by: str
        :param last_modified_by: Last modifier of the dataset
        :type last_modified_by: str
        :param min_cdate: Lower limit for the creation date (unixtime) (Optional)
        :type min_cdate: int, str
        :param max_cdate: Upper limit for the creation date (unixtime) (Optional)
        :type max_cdate: int, str
        :param min_ldate: Lower limit for the last modification date (unixtime) (Optional)
        :type min_ldate: int, str
        :param max_ldate: Upper limit for the last modification date (unixtime) (Optional)
        :type max_ldate: int, str
        :param cdate: creation date (unixtime) (Optional)
        :type cdate: int, str
        :param ldate: last modification date (unixtime) (Optional)
        :type ldate: int, str
        :param detail: List all details of a dataset
        :type detail: bool
        :param dataset_id: dataset table primary key used by CMS Computing Analytics.
        :type dataset_id: int, long, str
        :returns: List of dictionaries containing the following keys (dataset). If the detail option is used. The dictionary contain the following keys (primary_ds_name, physics_group_name, acquisition_era_name, create_by, dataset_access_type, data_tier_name, last_modified_by, creation_date, processing_version, processed_ds_name, xtcrosssection, last_modification_date, dataset_id, dataset, prep_id, primary_ds_type)
        :rtype: list of dicts

        """
        dataset = dataset.replace("*", "%")
        parent_dataset = parent_dataset.replace("*", "%")
        release_version = release_version.replace("*", "%")
        pset_hash = pset_hash.replace("*", "%")
        app_name = app_name.replace("*", "%")
        output_module_label = output_module_label.replace("*", "%")
        global_tag = global_tag.replace("*", "%")
        logical_file_name = logical_file_name.replace("*", "%")
        physics_group_name = physics_group_name.replace("*", "%")
        primary_ds_name = primary_ds_name.replace("*", "%")
        primary_ds_type = primary_ds_type.replace("*", "%")
        data_tier_name = data_tier_name.replace("*", "%")
        dataset_access_type = dataset_access_type.replace("*", "%")
        processed_ds_name = processed_ds_name.replace("*", "%")
        acquisition_era_name = acquisition_era_name.replace("*", "%")
        #processing_version =  processing_version.replace("*", "%")
        #create_by and last_modified_by have be full spelled, no wildcard will allowed.
        #We got them from request head so they can be either HN account name or DN.
        #This is depended on how an user's account is set up.
        try:
            dataset_id = int(dataset_id)
        except:
            dbsExceptionHandler("dbsException-invalid-input2", "Invalid Input for dataset_id that has to be an int.",
                                self.logger.exception, 'dataset_id has to be an int.')
        if create_by.find('*')!=-1 or create_by.find('%')!=-1 or last_modified_by.find('*')!=-1\
                or last_modified_by.find('%')!=-1:
            dbsExceptionHandler("dbsException-invalid-input2", "Invalid Input for create_by or last_modified_by.\
            No wildcard allowed.",  self.logger.exception, 'No wildcards allowed for create_by or last_modified_by')
        try:
            if isinstance(min_cdate, basestring) and ('*' in min_cdate or '%' in min_cdate):
                min_cdate = 0
            else:
                try:
                    min_cdate = int(min_cdate)
                except:
                    dbsExceptionHandler("dbsException-invalid-input", "invalid input for min_cdate")
            
            if isinstance(max_cdate, basestring) and ('*' in max_cdate or '%' in max_cdate):
                max_cdate = 0
            else:
                try:
                    max_cdate = int(max_cdate)
                except:
                    dbsExceptionHandler("dbsException-invalid-input", "invalid input for max_cdate")
            
            if isinstance(min_ldate, basestring) and ('*' in min_ldate or '%' in min_ldate):
                min_ldate = 0
            else:
                try:
                    min_ldate = int(min_ldate)
                except:
                    dbsExceptionHandler("dbsException-invalid-input", "invalid input for min_ldate")
            
            if isinstance(max_ldate, basestring) and ('*' in max_ldate or '%' in max_ldate):
                max_ldate = 0
            else:
                try:
                    max_ldate = int(max_ldate)
                except:
                    dbsExceptionHandler("dbsException-invalid-input", "invalid input for max_ldate")
            
            if isinstance(cdate, basestring) and ('*' in cdate or '%' in cdate):
                cdate = 0
            else:
                try:
                    cdate = int(cdate)
                except:
                    dbsExceptionHandler("dbsException-invalid-input", "invalid input for cdate")
            
            if isinstance(ldate, basestring) and ('*' in ldate or '%' in ldate):
                ldate = 0
            else:
                try:
                    ldate = int(ldate)
                except:
                    dbsExceptionHandler("dbsException-invalid-input", "invalid input for ldate")
        except dbsException as de:
            dbsExceptionHandler(de.eCode, de.message, self.logger.exception, de.serverError)
        except Exception as ex:
            sError = "DBSReaderModel/listDatasets.  %s \n. Exception trace: \n %s" \
                % (ex, traceback.format_exc())
            dbsExceptionHandler('dbsException-server-error', dbsExceptionCode['dbsException-server-error'], self.logger.exception, sError)

        detail = detail in (True, 1, "True", "1", 'true')
        try: 
            return self.dbsDataset.listDatasets(dataset, parent_dataset, is_dataset_valid, release_version, pset_hash,
                app_name, output_module_label, global_tag, processing_version, acquisition_era_name, 
                run_num, physics_group_name, logical_file_name, primary_ds_name, primary_ds_type, processed_ds_name,
                data_tier_name, dataset_access_type, prep_id, create_by, last_modified_by,
                min_cdate, max_cdate, min_ldate, max_ldate, cdate, ldate, detail, dataset_id)
        except dbsException as de:
            dbsExceptionHandler(de.eCode, de.message, self.logger.exception, de.serverError)
        except Exception as ex:
            sError = "DBSReaderModel/listdatasets. %s.\n Exception trace: \n %s" % (ex, traceback.format_exc())
            dbsExceptionHandler('dbsException-server-error', dbsExceptionCode['dbsException-server-error'], self.logger.exception, sError)


    def listBlocks(self, dataset="", block_name="", data_tier_name="", origin_site_name="",
                   logical_file_name="",run_num=-1, min_cdate='0', max_cdate='0',
                   min_ldate='0', max_ldate='0', cdate='0',  ldate='0', open_for_writing=-1, detail=False):

        """
        API to list a block in DBS. At least one of the parameters block_name, dataset, data_tier_name or
        logical_file_name are required. If data_tier_name is provided, min_cdate and max_cdate have to be specified and
        the difference in time have to be less than 31 days.

        :param block_name: name of the block
        :type block_name: str
        :param dataset: dataset
        :type dataset: str
        :param data_tier_name: data tier
        :type data_tier_name: str
        :param logical_file_name: Logical File Name
        :type logical_file_name: str
        :param origin_site_name: Origin Site Name (Optional)
        :type origin_site_name: str
        :param open_for_writing: Open for Writting (Optional)
        :type open_for_writing: int (0 or 1)
        :param run_num: run_num numbers (Optional). Possible format are: run_num, 'run_min-run_max' or ['run_min-run_max', run1, run2, ...].
        :type run_num: int, list of runs or list of run ranges
        :param min_cdate: Lower limit for the creation date (unixtime) (Optional)
        :type min_cdate: int, str
        :param max_cdate: Upper limit for the creation date (unixtime) (Optional)
        :type max_cdate: int, str
        :param min_ldate: Lower limit for the last modification date (unixtime) (Optional)
        :type min_ldate: int, str
        :param max_ldate: Upper limit for the last modification date (unixtime) (Optional)
        :type max_ldate: int, str
        :param cdate: creation date (unixtime) (Optional)
        :type cdate: int, str
        :param ldate: last modification date (unixtime) (Optional)
        :type ldate: int, str
        :param detail: Get detailed information of a block (Optional)
        :type detail: bool
        :returns: List of dictionaries containing following keys (block_name). If option detail is used the dictionaries contain the following keys (block_id, create_by, creation_date, open_for_writing, last_modified_by, dataset, block_name, file_count, origin_site_name, last_modification_date, dataset_id and block_size)
        :rtype: list of dicts

        """
        dataset = dataset.replace("*", "%")
        block_name = block_name.replace("*", "%")
        logical_file_name = logical_file_name.replace("*", "%")
        origin_site_name = origin_site_name.replace("*", "%")
        #
        if isinstance(min_cdate, basestring) and ('*' in min_cdate or '%' in min_cdate):
            min_cdate = 0
        else:
            try:
                min_cdate = int(min_cdate)
            except:
                dbsExceptionHandler("dbsException-invalid-input", "invalid input for min_cdate")
        #
        if isinstance(max_cdate, basestring) and ('*' in max_cdate or '%' in max_cdate):
            max_cdate = 0
        else:
            try:
                max_cdate = int(max_cdate)
            except:
                dbsExceptionHandler("dbsException-invalid-input", "invalid input for max_cdate")
        #
        if isinstance(min_ldate, basestring) and ('*' in min_ldate or '%' in min_ldate):
            min_ldate = 0
        else:
            try:
                min_ldate = int(min_ldate)
            except:
                dbsExceptionHandler("dbsException-invalid-input", "invalid input for max_cdate")
        #
        if isinstance(max_ldate, basestring) and ('*' in max_ldate or '%' in max_ldate):
            max_ldate = 0
        else:
            try:
                max_ldate = int(max_ldate)
            except:
                dbsExceptionHandler("dbsException-invalid-input", "invalid input for max_ldate")
        #
        if isinstance(cdate, basestring) and ('*' in cdate or '%' in cdate):
            cdate = 0
        else:
            try:
                cdate = int(cdate)
            except:
                dbsExceptionHandler("dbsException-invalid-input", "invalid input for cdate")
        #
        if isinstance(cdate, basestring) and ('*' in ldate or '%' in ldate):
            ldate = 0
        else:
            try:
                ldate = int(ldate)
            except:
                dbsExceptionHandler("dbsException-invalid-input", "invalid input for ldate")
        #
        detail = detail in (True, 1, "True", "1", 'true')
        try:
            b= self.dbsBlock.listBlocks(dataset, block_name, data_tier_name, origin_site_name, logical_file_name,
                                  run_num, min_cdate, max_cdate, min_ldate, max_ldate, cdate, ldate, open_for_writing, detail)
            #for item in b:
                #yield item
            return b
#        except HTTPError:
#            raise
        except dbsException as de:
            dbsExceptionHandler(de.eCode, de.message, self.logger.exception, de.serverError)
        except Exception as ex:
            sError = "DBSReaderModel/listBlocks. %s\n. Exception trace: \n %s" \
                    % (ex, traceback.format_exc())
            dbsExceptionHandler('dbsException-server-error', dbsExceptionCode['dbsException-server-error'], self.logger.exception, sError)

    def listFiles(self, dataset = "", block_name = "", logical_file_name = "",
        release_version="", pset_hash="", app_name="", output_module_label="",
        run_num=-1, origin_site_name="", lumi_list="", detail=False, validFileOnly=0):
        """
        API to list files in DBS. Either non-wildcarded logical_file_name, non-wildcarded dataset or non-wildcarded block_name is required.
        The combination of a non-wildcarded dataset or block_name with an wildcarded logical_file_name is supported.

        * For lumi_list the following two json formats are supported:
            - [a1, a2, a3,]
            - [[a,b], [c, d],]
        * lumi_list can be either a list of lumi section numbers as [a1, a2, a3,] or a list of lumi section range as [[a,b], [c, d],]. Thay cannot be mixed.
        * If lumi_list is provided run only run_num=single-run-number is allowed
        * When lfn list is present, no run or lumi list is allowed.

        :param logical_file_name: logical_file_name of the file
        :type logical_file_name: str
        :param dataset: dataset
        :type dataset: str
        :param block_name: block name
        :type block_name: str
        :param release_version: release version
        :type release_version: str
        :param pset_hash: parameter set hash
        :type pset_hash: str
        :param app_name: Name of the application
        :type app_name: str
        :param output_module_label: name of the used output module
        :type output_module_label: str
        :param run_num: run , run ranges, and run list. Possible format are: run_num, 'run_min-run_max' or ['run_min-run_max', run1, run2, ...].
        :type run_num: int, list, string
        :param origin_site_name: site where the file was created
        :type origin_site_name: str
        :param lumi_list: List containing luminosity sections
        :type lumi_list: list
        :param detail: Get detailed information about a file
        :type detail: bool
        :param validFileOnly: default=0 return all the files. when =1, only return files with is_file_valid=1 or dataset_access_type=PRODUCTION or VALID
        :type validFileOnly: int
        :returns: List of dictionaries containing the following keys (logical_file_name). If detail parameter is true, the dictionaries contain the following keys (check_sum, branch_hash_id, adler32, block_id, event_count, file_type, create_by, logical_file_name, creation_date, last_modified_by, dataset, block_name, file_id, file_size, last_modification_date, dataset_id, file_type_id, auto_cross_section, md5, is_file_valid)
        :rtype: list of dicts

        """
        logical_file_name = logical_file_name.replace("*", "%")
        release_version = release_version.replace("*", "%")
        pset_hash = pset_hash.replace("*", "%")
        app_name = app_name.replace("*", "%")
        block_name = block_name.replace("*", "%")
        origin_site_name = origin_site_name.replace("*", "%")
        dataset = dataset.replace("*", "%")
        if lumi_list:
            if run_num ==-1 or not run_num :
                dbsExceptionHandler("dbsException-invalid-input", "When lumi_list is given, require a single run_num.", self.logger.exception)
            else:
                try:
                    lumi_list = self.dbsUtils2.decodeLumiIntervals(lumi_list)
                except Exception as de:
                    dbsExceptionHandler("dbsException-invalid-input", "Invalid lumi_list input: "+ str(de), self.logger.exception)
        else:
            if not isinstance(run_num, list):
                if run_num ==1 or run_num == '1':
                    dbsExceptionHandler("dbsException-invalid-input", "files API does not supprt run_num=1 when no lumi.", self.logger.exception)
            else:
                if 1 in run_num or '1' in run_num :
                 dbsExceptionHandler("dbsException-invalid-input", "files API does not supprt run_num=1 when no lumi.", self.logger.exception)

        detail = detail in (True, 1, "True", "1", 'true')
        output_module_label = output_module_label.replace("*", "%")
        try:
            result =  self.dbsFile.listFiles(dataset, block_name, logical_file_name, release_version, pset_hash, app_name,
                                        output_module_label, run_num, origin_site_name, lumi_list, detail, validFileOnly)
            for item in result:
                yield item
#        except HTTPError as he:
#            raise he
        except dbsException as de:
            dbsExceptionHandler(de.eCode, de.message, self.logger.exception, de.serverError)
        except Exception as ex:
            sError = "DBSReaderModel/listFiles. %s \n Exception trace: \n %s" % (ex, traceback.format_exc())
            dbsExceptionHandler('dbsException-server-error', ex.message,
                    self.logger.exception, sError)

from flask import Flask
from flask import request, g
app = Flask(__name__)
dbs = DBSReaderModel(config) 

@app.route("/test/datasets/")
def datasets():
    dataset = request.args.get("dataset")
    datasets = dbs.listDatasets(dataset=dataset)
    data = [d for d in datasets]
    return json.dumps(data)

@app.route("/test/blocks/")
def blocks():
    dataset = request.args.get("dataset")
    blocks = dbs.listBlocks(dataset=dataset)
    data = [d for d in blocks]
    return json.dumps(data)

@app.route("/test/files/")
def files():
    dataset = request.args.get("dataset")
    files = dbs.listFiles(dataset=dataset)
    data = [d for d in files]
    return json.dumps(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8800)
