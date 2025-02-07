from utils.get_data import GetData
from utils.calculate import Calculate
import pandas as pd


# Home Page
class Client:
    def __init__(self):
        try:
            # 初始化時就讀取所有數據
            print("Initializing Client...")
            data_loader = GetData()
            
            # 打印調試信息
            print("Loading AI data...")
            self.AI = data_loader.get_AI()
            print("AI columns:", self.AI.columns.tolist())
            print("AI data sample:", self.AI.head())
            
            print("Loading BI data...")
            self.BI = data_loader.get_BI()
            print("BI data loaded")
            
            print("Loading EWC data...")
            self.EWC = data_loader.get_EWC()
            print("EWC data loaded")
            
            # 預處理常用數據
            self._preprocess_data()
            
        except Exception as e:
            print(f"Error in Client initialization: {str(e)}")
            raise
        
    def _preprocess_data(self):
        """預處理常用數據以提高後續計算效率"""
        try:
            print("Starting data preprocessing...")
            
            # 檢查數據是否為空
            if self.AI.empty:
                raise ValueError("AI DataFrame is empty")
                
            # 檢查列是否存在
            print("AI columns before preprocessing:", self.AI.columns.tolist())
            
            # 轉換數據為可哈希格式以用於緩存
            self.AI_hash = tuple(map(tuple, self.AI.values))
            self.BI_hash = tuple(map(tuple, self.BI.values))
            self.EWC_hash = tuple(map(tuple, self.EWC.values))
            
            print("Data preprocessing completed successfully")
            
        except Exception as e:
            print(f"Error in _preprocess_data: {str(e)}")
            raise
        
    def get_AI_usage(self):
        try:
            print("Calculating AI usage...")
            print("AI columns available:", self.AI.columns.tolist())
            print("AI data sample:", self.AI.head())
            
            result = Calculate().calculate_percentage_of_AI_usage(self.AI_hash)
            print("AI usage calculation result:", result)
            return result
            
        except Exception as e:
            print(f"Error in get_AI_usage: {str(e)}")
            raise
    
    def get_age_usage(self):
        age_usage = Calculate().calculate_percentage_of_age(self.BI)
        return age_usage
    
    def get_employment_usage(self):
        employment_usage = Calculate().calculate_percentage_of_employment(self.BI)
        return employment_usage

    def get_age_employment_distribution(self):
        return Calculate().calculate_age_employment_distribution(self.BI_hash)
    
    def get_ai_usage_percentage(self):
        percentage = Calculate().calculate_ai_usage_percentage(self.AI, self.BI)
        return percentage
    
    def get_edu_brain_for_heatmap(self):
        heatmap_data = Calculate().calculate_edu_brain_for_heatmap(self.EWC, self.BI)
        return heatmap_data
    
    def get_favorable_on_edu_and_code(self):
        return Calculate().calculate_favorable_on_edu_and_code(
            self.EWC_hash, 
            self.BI_hash, 
            self.AI_hash
        )
    
    def get_benefit_wordcloud(self):
        benefit_wordcloud = Calculate().benefit_wordcloud(self.AI)
        return benefit_wordcloud

    def get_AI_tool_currently_using(self):
        AI_tool_currently_using = Calculate().calculate_AI_tool_currently_using(self.AI)
        return AI_tool_currently_using