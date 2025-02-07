import pandas as pd
from functools import lru_cache


class Calculate:
    def __init__(self):
        pass

    @lru_cache(maxsize=32)
    def calculate_percentage_of_AI_usage(self, AI_data_hash):
        try:
            print("Starting AI usage calculation...")
            # Convert hash back to DataFrame with explicit column names
            AI = pd.DataFrame(AI_data_hash, 
                            columns=['ResponseId', 'AISelect', 'AISent', 'AIBen', 'AIToolCurrently Using'])
            
            print("AI DataFrame columns:", AI.columns.tolist())
            print("AI DataFrame head:", AI.head())
            print("AI DataFrame shape:", AI.shape)
            
            # 直接使用列名而不是位置索引
            counts = AI['AISelect'].value_counts()
            print("Value counts:", counts)
            
            total = counts.sum()
            result = pd.DataFrame({
                'AISelect': counts.index,
                'count': counts.values,
                'percentage': (counts.values / total)
            })
            
            print("Final result:", result)
            return result
            
        except Exception as e:
            print(f"Error in calculate_percentage_of_AI_usage: {str(e)}")
            print("Full error details:", e)
            print("AI DataFrame info:")
            print(AI.info())
            print("AI DataFrame head:")
            print(AI.head())
            raise

    def calculate_percentage_of_age(self, BI):
        age_usage = BI.groupby('Age').count().iloc[:,0].rename('count').reset_index()
        age_usage['percentage'] = age_usage['count'] / age_usage['count'].sum()
        return age_usage
    

    @lru_cache(maxsize=32)
    def calculate_age_employment_distribution(self, BI_data_hash):
        try:
            print("Starting age employment distribution calculation...")
            # Convert hash back to DataFrame with explicit column names - updated to include MainBranch
            BI = pd.DataFrame(BI_data_hash, 
                            columns=['ResponseId', 'Age', 'Employment', 'MainBranch'])
            
            print("BI DataFrame columns:", BI.columns.tolist())
            print("BI DataFrame head:", BI.head())
            print("BI DataFrame shape:", BI.shape)
            
            # 預處理數據
            mask = BI['Age'].notna() & BI['Employment'].notna()
            BI = BI[mask].copy()
            
            # 使用 explode 處理多值
            BI['Employment'] = BI['Employment'].str.split(';')
            BI = BI.explode('Employment')
            BI['Employment'] = BI['Employment'].str.strip()
            
            # 使用 crosstab 直接計算百分比
            cross_tab = pd.crosstab(BI['Age'], BI['Employment'], normalize='all') * 100
            
            # 按總和排序列
            column_sums = cross_tab.sum()
            result = cross_tab[column_sums.sort_values(ascending=False).index]
            
            print("Final result shape:", result.shape)
            print("Final result sample:", result.head())
            return result
            
        except Exception as e:
            print(f"Error in calculate_age_employment_distribution: {str(e)}")
            print("Full error details:", e)
            if 'BI' in locals():
                print("BI DataFrame info:")
                print(BI.info())
                print("BI DataFrame head:")
                print(BI.head())
            print("Original data hash sample:", BI_data_hash[:5])
            raise
    

    def calculate_ai_usage_percentage(self, AI, BI):
        # Use merge instead of join to avoid column overlap
        df = pd.merge(
            AI[['ResponseId', 'AISelect']],
            BI[['ResponseId', 'Employment', 'Age']],
            on='ResponseId',
            how='inner'
        )
        
        # Split employment statuses and explode to separate rows
        df['Employment'] = df['Employment'].str.split(';')
        df = df.explode('Employment')
        df['Employment'] = df['Employment'].str.strip()
        
        # Convert AISelect to boolean for easier calculation
        df['is_using_ai'] = df['AISelect'] == 'Yes'
        
        # First calculate total users for each employment-age combination
        total_users = df.groupby(['Employment', 'Age']).size()
        
        # Then calculate AI users for each employment-age combination
        ai_users = df[df['is_using_ai']].groupby(['Employment', 'Age']).size()
        
        # Calculate percentage
        result = (ai_users / total_users * 100).round(2)
        
        # Sort values in descending order
        result = result.sort_values(ascending=False)
        
        return result
    
    def calculate_edu_brain_for_heatmap(self, EWC, BI):
        try:
            print("Starting edu brain heatmap calculation...")
            
            # 確保數據框不為空
            if EWC.empty or BI.empty:
                raise ValueError("One or both DataFrames are empty")
            
            # 使用 MainBranch 替代 Employment
            eb = pd.merge(
                BI[['ResponseId', 'MainBranch']],  # Changed from Employment to MainBranch
                EWC[['ResponseId', 'EdLevel']],
                on='ResponseId',
                how='inner'
            )
            
            # MainBranch 已經是單一值，不需要 split 和 explode
            
            # 創建交叉表並計算百分比
            total_responses = len(eb['ResponseId'].unique())
            cross_tab = pd.crosstab(
                eb['EdLevel'], 
                eb['MainBranch'],  # Changed from Employment to MainBranch
                normalize='all'
            ) * 100
            
            # 按列總和排序
            column_sums = cross_tab.sum()
            cross_tab = cross_tab[column_sums.sort_values(ascending=False).index]
            
            print("Cross tab shape:", cross_tab.shape)
            print("Cross tab sample:", cross_tab.head())
            
            return cross_tab
            
        except Exception as e:
            print(f"Error in calculate_edu_brain_for_heatmap: {str(e)}")
            print("Full error details:", e)
            print("EWC info:", EWC.info())
            print("BI info:", BI.info())
            raise
    
    @lru_cache(maxsize=32)
    def calculate_favorable_on_edu_and_code(self, EWC_data_hash, BI_data_hash, AI_data_hash):
        try:
            print("Starting favorable calculation...")
            # 轉換回 DataFrame，確保列名與數據匹配
            EWC = pd.DataFrame(EWC_data_hash, 
                             columns=['ResponseId', 'EdLevel'])
            BI = pd.DataFrame(BI_data_hash, 
                            columns=['ResponseId', 'Age', 'Employment', 'MainBranch'])  # 修正列名順序
            AI = pd.DataFrame(AI_data_hash, 
                            columns=['ResponseId', 'AISelect', 'AISent', 'AIBen', 'AIToolCurrently Using'])
            
            # Debug 輸出
            print("BI DataFrame columns:", BI.columns.tolist())
            print("BI DataFrame shape:", BI.shape)
            print("BI data hash first row:", BI_data_hash[0] if BI_data_hash else None)
            
            # 使用更高效的合併方式
            df = pd.merge(
                BI[['ResponseId', 'MainBranch']],
                EWC[['ResponseId', 'EdLevel']],
                on='ResponseId'
            )
            result = pd.merge(
                df,
                AI[['ResponseId', 'AISent']],
                on='ResponseId'
            )
            
            print("Result columns:", result.columns.tolist())
            print("Result shape:", result.shape)
            
            return result
            
        except Exception as e:
            print(f"Error in calculate_favorable_on_edu_and_code: {str(e)}")
            print("Full error details:", e)
            print("BI_data_hash length:", len(BI_data_hash))
            print("BI_data_hash first row:", BI_data_hash[0] if BI_data_hash else None)
            raise
    
    def benefit_wordcloud(self, AI):
        df = AI[['AIBen', 'AISent']].dropna()
        # Split the benefits into separate items
        df['AIBen'] = df['AIBen'].apply(lambda x: x.split(';'))

        # Explode the list to separate rows and count frequencies
        df = df.explode('AIBen')[['AIBen', 'AISent']]
        benefit_counts = df.groupby(['AISent','AIBen']).size().reset_index(name='count')
        benefit_counts = benefit_counts.sort_values(by='count', ascending=False)

        benefit_counts = benefit_counts[benefit_counts['AIBen'] != 'Other (please specify):']
        return benefit_counts
    
    def calculate_AI_tool_currently_using(self, AI):
        df = AI[['AIToolCurrently Using', 'AISent']].dropna()
        df['AIToolCurrently Using'] = df['AIToolCurrently Using'].apply(lambda x: x.split(';'))
        df = df.explode('AIToolCurrently Using')
        df['AIToolCurrently Using'] = df['AIToolCurrently Using'].str.strip()
        return df