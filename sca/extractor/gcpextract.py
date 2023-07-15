"""
Created on May 4th 2022

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""
import logging
import os.path
from sca.common.config import ConfigHolder
from google.cloud import bigquery
from google.oauth2 import service_account


class BigQueryExtractor:
    '''

    '''
    ch = None
    credentials = None
    project_id = None
    customer = None

    def __init__(self, customer, file_name=None, config=None):
        '''
        Create BlackChainExtractor with file_names

        Parameters
        ----------
        customer : TYPE str
        Name of the customer that needs contract analytic. If
        directory doesn't exist, new directory with passed-in customer will be
        created
        file_name : TYPE
            Configuration file names

        Returns
        -------
        None.

        '''
        assert customer is not None
        self.customer = customer
        if file_name is None and config is None:
            raise ValueError("Both file_names and config are None")

        if file_name is not None and config is not None:
            raise ValueError("Both file_names and config are not None")

        if config is None:
            BigQueryExtractor.ch = ConfigHolder(file_name)
        else:
            BigQueryExtractor.ch = config

        self.logger = logging.getLogger(__name__)
        self.log_level = BigQueryExtractor.ch.get_value("log_level")

        if self.log_level == "info":
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)

        path = os.getcwd()+"/sca/resource/"
        gcp_file = BigQueryExtractor.ch.get_value("gcp_credentials_file_name")
        self.credentials = service_account.Credentials.from_service_account_file(path+"/"+gcp_file)
        self.project_id = BigQueryExtractor.ch.get_value("project_id")

        # check if the dir with customer exist, if not create new
        if not os.path.exists(os.getcwd()+"/sca/data/"+self.customer):
            os.makedirs(os.getcwd()+"/sca/data/"+self.customer)



    def get_config_value(self, key):
        '''
        Get the value associated with the parameter "key" from the ConfigHolder
        associated with the BlackChainExtractor

        Parameters
        ----------
        key : str
            Name of the config parameter defined in the config file

        Returns
        -------
        str
            Value of the parameter associated with the key,
            defined in the config file


        '''
        assert key is not None
        return BigQueryExtractor.ch.get_value(key)

    def execute_query(self, query_name, file_name):
        assert query_name is not None
        assert file_name is not None
        path = os.getcwd()+"/sca/resource/sql/"
        with open(path+query_name, 'r') as file:
            sql = file.read()

        client = bigquery.Client(credentials=self.credentials, project=self.project_id)
        query_job = client.query(sql)
        query_df = query_job.to_dataframe()
        path = os.getcwd() + "/sca/data/"+self.customer+"/"
        query_df.to_csv(path+file_name+".csv", index=False)






