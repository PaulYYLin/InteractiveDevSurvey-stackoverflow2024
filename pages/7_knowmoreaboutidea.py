from utils.client import Client
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

def main():
    client = Client()
    benefit_wordcloud = client.get_benefit_wordcloud()
    user_sentiment = st.session_state['user_selections']['sentiment']
    st.markdown("<style>button {height: 80px;}</style>", unsafe_allow_html=True)
    # Add page title using selected sentiment
    st.markdown(f"<h1 style='font-size: 60px;'>Let's see what benefits developers who also think AI tools are <span style='color: #c5e1a5; font-weight: bold;'>{user_sentiment}</span> think AI has.</h1>", unsafe_allow_html=True)
    
    
    # Filter data based on sentiment
    filtered_data = benefit_wordcloud[benefit_wordcloud['AISent'] == user_sentiment]

    left_col, right_col = st.columns([0.4, 0.6])
    with left_col:
       
        st.markdown("<h3 style='font-size: 20px;'>Bigger the word, more people think it's a benefit ✨</h3>", unsafe_allow_html=True)
        
        # Create word cloud data with word frequencies
        word_freq = filtered_data.loc[:, ['AIBen', 'count']].set_index('AIBen')['count'].to_dict()
        
        if word_freq:
            # Generate word cloud with updated styling
            wordcloud = WordCloud(
                background_color='rgba(0,0,0,0)',
                mode='RGBA',
                height=300,
                colormap='YlGn',  # Green colormap to match the theme
                max_words=100
            ).generate_from_frequencies(word_freq)
            
            # Display the word cloud with dark theme
            fig, ax = plt.subplots(facecolor='none')  # Transparent figure background
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            
            # Set plot style to match home page
            plt.style.use('dark_background')
            fig.patch.set_alpha(0.0)  # Transparent figure background
            
            # Add custom styling to the Streamlit container
            st.markdown("""
                <style>
                .main-container {
                    background-color: transparent !important;
                }
                .stSelectbox label {
                    color: #c5e1a5 !important;
                    font-size: 1.2rem !important;
                }
                .stTitle {
                    color: #c5e1a5 !important;
                    font-size: 2.5rem !important;
                    margin-bottom: 2rem !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            st.pyplot(fig)
        else:
            st.warning("No data available for the selected sentiment filter.")


    with right_col:
        st.markdown("<h3 style='font-size: 20px; text-align: center;'>These Developers are using AI tools for ...</h3>", unsafe_allow_html=True)
        AI_tool_currently_using = client.get_AI_tool_currently_using()
        AI_tool_currently_using = AI_tool_currently_using[AI_tool_currently_using['AISent'] == user_sentiment]
        AI_tool_currently_using = AI_tool_currently_using.groupby('AIToolCurrently Using').size().reset_index(name='count').sort_values(by='count', ascending=True)
        # 建立長條圖
        fig = px.bar(
            AI_tool_currently_using,
            x='count',
            y='AIToolCurrently Using',
            orientation='h',
            labels={'count': '', 'AIToolCurrently Using': ''},
            text='count'
        )
        
        # 設定圖表樣式
        fig.update_traces(
            textposition='outside',
            marker_color='#c5e1a5',  # 改用相同的綠色主題
            textfont=dict(
                size=14,
                color='#ffffff'  # 白色文字
            )
        )
        
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',  # 透明背景
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',  # 白色字體
            height=max(500, len(AI_tool_currently_using) * 30),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(color='#ffffff')
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',  # 淡白色網格
                tickfont=dict(color='#ffffff')
            ),
            margin=dict(t=50, b=100)
        )
        
        # 顯示圖表
        st.plotly_chart(fig, use_container_width=True)
    # Add navigation button at the bottom
    
    if st.button("➤ LET'S HEADING TO DESTINATION OF SURVEY", use_container_width=True ,):
        st.switch_page("pages/8_summary.py")


if __name__ == "__main__":
    main()