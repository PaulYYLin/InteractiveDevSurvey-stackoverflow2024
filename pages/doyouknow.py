import streamlit as st
import plotly.graph_objects as go
from utils.client import Client

def main():
    # Custom CSS styling
    st.markdown("""
        <style>
        .main-container {
            padding: 2rem;
        }
        .title {
            color: #c5e1a5;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # 從 session_state 獲取用戶數據
    user_employment = st.session_state.get('user_employment', 'Student, part-time')
    user_age = st.session_state.get('user_age', '25-34 years old')
    if user_employment:
        # 獲取所有就業類別和年齡的 AI 使用百分比
        percentages = Client().get_ai_usage_percentage()
        
        # 創建兩列佈局
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # 創建條形圖
            fig = go.Figure()
            
            user_percentage = None
            user_age_percentage = None
            show_age_detail = st.session_state.get('show_age_detail', False)
            
            if not show_age_detail:
                # 原始的就業類別視圖
                for emp, age_data in percentages.groupby(level=0):
                    is_user_category = user_employment in emp
                    avg_pct = age_data.mean()
                    
                    fig.add_trace(go.Bar(
                        x=[emp],
                        y=[avg_pct],
                        marker_color='#206546' if is_user_category else '#2a2a2a',
                        width=0.6,
                        text=[f'{avg_pct:.1f}%'],
                        textposition='auto',
                        textfont=dict(
                            size=14,
                            color='#ffffff'
                        ),
                        showlegend=False,
                        name=''
                    ))
                    
                    if is_user_category:
                        user_percentage = avg_pct
                        # 保存用戶年齡組的百分比
                        user_age_percentage = age_data.get((emp, user_age), None)
                
                if user_percentage is not None:
                    st.markdown(f"""
                    <h1>
                        <span style="color: #c5e1a5; font-weight: bold; font-size: 80px;">{user_percentage:.1f}%</span><br> of participating developers 
                        <br>who is also <span style="color: #c5e1a5; font-weight: bold;">{user_employment}</span> are using AI tools.
                    </h1>
                    Some developers have multiple employment statuses, so the percentage may not be 100%.
                    """, unsafe_allow_html=True)
            
            else:
                # 只顯示用戶就業類別的年齡分佈
                employment_data = percentages.loc[user_employment]
                
                # 對年齡組進行排序
                age_order = {
                    'Under 18 years old': 1,
                    '18-24 years old': 2,
                    '25-34 years old': 3,
                    '35-44 years old': 4,
                    '45-54 years old': 5,
                    '55-64 years old': 6,
                    '65 years or older': 7,
                    'Prefer not to say': 8
                }
                
                # 根據自定義順序排序數據
                employment_data = employment_data.reindex(
                    sorted(employment_data.index, key=lambda x: age_order.get(x, 9))
                )
                
                age_groups = employment_data.index.tolist()
                percentages_values = employment_data.values
                
                # 為用戶的年齡組設置特殊顏色
                colors = ['#2a2a2a' if age != user_age else '#c5e1a5' 
                         for age in age_groups]
                
                fig.add_trace(go.Bar(
                    x=percentages_values,
                    y=age_groups,
                    text=[f'{pct:.1f}%' for pct in percentages_values],
                    textposition='outside',
                    marker_color=colors,
                    orientation='h',
                    textfont=dict(
                        size=14,
                        color='#ffffff'
                    ),
                ))
                
                # 找到用戶年齡組的百分比
                user_age_percentage = employment_data.get(user_age, None)

                if user_age_percentage is not None:
                    st.markdown(f"""
                    <h1>
                        <span style="color: #c5e1a5; font-weight: bold; font-size: 80px;">{user_age_percentage:.1f}%</span> of <span style="color: #c5e1a5; font-weight: bold;">{user_employment}</span> developers 
                        in your age group (<span style="color: #c5e1a5; font-weight: bold;">{user_age}</span>) are using AI tools.
                    </h1>
                    The graph shows AI usage across all age groups for {user_employment}.
                    """, unsafe_allow_html=True)

                # 更新圖表布局
                fig.update_layout(
                    barmode='stack',
                    showlegend=False,
                    yaxis_title="Age Groups",
                    xaxis_title="AI Usage Percentage (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    yaxis=dict(
                        showgrid=False,
                        tickfont=dict(color='#ffffff')
                    ),
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.1)',
                        tickfont=dict(color='#ffffff'),
                        range=[0, max(percentages_values) * 1.3]
                    ),
                    height=600,
                    margin=dict(
                        t=50,
                        b=100,
                        l=50,
                        r=50
                    ),
                    bargap=0.3
                )

            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<br>" * 5, unsafe_allow_html=True)  # 添加一些空行來對齊按鈕
            if st.button("➤ How many developers in my age group are using AI tools?" if not show_age_detail else "⏎ Back to Overview",
                        use_container_width=True):
                st.session_state.show_age_detail = not show_age_detail
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)  # 添加間距
            if st.button("➤ Next Page", use_container_width=True):
                st.switch_page("pages/relationshiptocode.py")  # 請替換成實際的下一頁文件名

if __name__ == "__main__":
    main()