import pandas as pd
import gzip
from functools import lru_cache

class GetData:
    def __init__(self):
        # 读取压缩的 CSV 文件
        with gzip.open('survey_results_public.csv.zip', 'rt') as f:
            self.data = pd.read_csv(
                f,
                usecols=lambda x: x in [
                    'ResponseId', 'Age', 'Employment', 'MainBranch',
                    'EdLevel', 'AISelect', 'AISent', 'AIBen',
                    'AIToolCurrently Using'
                ]
            )
        
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