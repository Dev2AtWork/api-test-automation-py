# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import unittest
import requests
import pandas as pd

class TestDarkSkyAPI(unittest.TestCase):
    response = None
    
    def setUp(self):
        config_df = pd.read_table('./config/config.txt'
                                  ,delimiter=';')
        self.response = requests.get(config_df['baseURI'][0] + '/' 
                                    + config_df['authKey'][0] +  '/' 
                                    + config_df['coordinates'][0])
        
    def test_api_return_code(self):        
        self.assertEqual(self.response.status_code,200)
     
    def test_validate_high_level_dtype(self):
        
        #get high level structure from response
        resp_body_dtype = pd.DataFrame(pd.DataFrame.from_dict(self.response.json()).dtypes)
        resp_body_dtype.reset_index(level=0, inplace=True)
        resp_body_dtype.columns = ['key', 'dtype']
        
        #get high level structure from data
        resp_body_expected_dtype = pd.read_table('./data/schema.txt'
                                                 ,delimiter=':',header=None, names= ['key', 'dtype'])
        self.assertTrue(resp_body_dtype.equals(resp_body_expected_dtype))
        
    def test_validate_item_count(self):
       resp_body = pd.DataFrame.from_dict(self.response.json())
       #create dataframe from response message
       resp_size_df = pd.DataFrame([{'minutely' : len(resp_body['minutely']['data']), 
                                    'hourly' : len(resp_body['hourly']['data']),
                                    'daily' : len(resp_body['daily']['data'])}])
       #read data in dataframe from data
       df_arr_size = pd.read_csv('./data/arraysize.csv')       
       #compare responses
       self.assertTrue(resp_size_df.equals(df_arr_size))

if __name__ == '__main__':
    unittest.main()
        