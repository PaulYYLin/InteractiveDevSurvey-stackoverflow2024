import pandas as pd
import zipfile
from functools import lru_cache
import streamlit as st

class GetData:
    def __init__(self):
        @st.cache_data
        def load_data():
            with zipfile.ZipFile('survey_results_public.csv.zip', 'r') as zip_ref:
                # 假设 ZIP 文件中只有一个 CSV 文件
                csv_filename = zip_ref.namelist()[0]
                with zip_ref.open(csv_filename) as f:
                    return pd.read_csv(
                        f,
                        usecols=lambda x: x in [
                            'ResponseId', 'Age', 'Employment', 'MainBranch',
                            'EdLevel', 'AISelect', 'AISent', 'AIBen',
                            'AIToolCurrently Using'
                        ]
                    )
        
        self.data = load_data()
        
    @lru_cache(maxsize=1)
    def get_BI(self):
        return self.data[['ResponseId', 'Age', 'Employment','MainBranch']]
    
    @lru_cache(maxsize=1)
    def get_EWC(self):
        return self.data[['ResponseId', 'EdLevel']]
    
    @lru_cache(maxsize=1)
    def get_AI(self):
        return self.data[['ResponseId', 'AISelect', 'AISent', 
                         'AIBen', 'AIToolCurrently Using']]

    def get_TTC(self):
        TTC = pd.concat([self.data.iloc[:, 0],  self.data.iloc[:,22:56]], axis=1)
        return TTC

    def get_SOUC(self):
        SOUC = pd.concat([self.data.iloc[:, 0],  self.data.iloc[:,56:63]], axis=1)
        return SOUC