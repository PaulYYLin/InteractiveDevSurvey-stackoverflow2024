import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.client import Client
import pandas as pd

def create_sentiment_pie(sentiment_counts):
    # Define color mapping
    color_map = {
        'Very favorable': '#c5e1a5',
        'Favorable': '#7cb342',
        'Unsure': '#4a4a4a',
        'Unfavorable': '#2a2a2a',
        'Very unfavorable': '#1a1a1a',
        'Indifferent': '#1a1a1a'
    }
    
    # Calculate percentages
    total = sum(sentiment_counts)
    df = pd.DataFrame({
        'Sentiment': sentiment_counts.index,
        'Count': sentiment_counts.values,
        'Percentage': [count/total*100 for count in sentiment_counts.values]
    })
    
    fig = px.pie(df,
                 values='Count',
                 names='Sentiment',
                 color='Sentiment',
                 color_discrete_map=color_map,
                 hole=0.3)
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        showlegend=True,
        margin=dict(l=30, r=30, t=20, b=20),
        legend=dict(
            font=dict(color='#ffffff'),
            bgcolor='rgba(0,0,0,0)'
        ),
        height=400
    )
    
    return fig

def create_tools_bar(tool_counts):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=tool_counts.index,
        x=tool_counts.values,
        orientation='h',
        marker_color='#c5e1a5',
        text=tool_counts.values,
        textposition='outside'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        height=400,
        margin=dict(l=30, r=30, t=20, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            title=None
        ),
        yaxis=dict(
            showgrid=False,
            title=None
        )
    )
    
    return fig

def main():
    st.markdown("""
        <style>
        .highlight {
            color: #c5e1a5;
            font-weight: bold;
        }
        .metric-value {
            font-size: 48px;
            color: #c5e1a5;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Your AI Tools Survey Journey Summary 🚀")
    
    user_selections = st.session_state.get('user_selections', {})
    client = Client()
    
    # Get filtered data
    favorable_data = client.get_favorable_on_edu_and_code()
    filtered_data = favorable_data[
        (favorable_data['MainBranch'] == user_selections.get('developer_status')) & 
        (favorable_data['EdLevel'] == user_selections.get('education_level'))
    ]
    
    # Profile and Key Metrics
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("""
            <h3 style="line-height: 1.8;">
                You are a 
                <span class="highlight">{education}</span> 
                graduate who identifies as a 
                <span class="highlight">{developer}</span> 
                and are 
                <span class="highlight">{sentiment}</span> 
                towards using AI tools.
            </h3>
        """.format(
            education=user_selections.get('education_level', 'N/A'),
            developer=user_selections.get('developer_status', 'N/A'),
            sentiment=user_selections.get('sentiment', 'N/A').lower()
        ), unsafe_allow_html=True)
    
    total_filtered = len(filtered_data)
    with col2:
        st.markdown("#### Similar Developers")
        st.markdown(f"""
            <div class='metric-value'>{total_filtered}</div>
            share your background
        """, unsafe_allow_html=True)
    
    sentiment_match = len(filtered_data[filtered_data['AISent'] == user_selections.get('sentiment')])
    with col3:
        st.markdown("#### Similar Sentiment")
        st.markdown(f"""
            <div class='metric-value'>{sentiment_match}</div>
            share your opinion
        """, unsafe_allow_html=True)

    # Sentiment Distribution and Tools Usage
    col1, col2 = st.columns([1, 1])
    
    with col2:
        st.markdown("### 📊 Sentiment Distribution")
        sentiment_counts = filtered_data['AISent'].value_counts()
        fig = create_sentiment_pie(sentiment_counts)
        st.plotly_chart(fig, use_container_width=True)
    
    with col1:
        AI_tools_data = client.get_AI_tool_currently_using()
        filtered_tools = AI_tools_data[
            AI_tools_data['AISent'] == user_selections.get('sentiment')
        ]
        tool_counts = filtered_tools['AIToolCurrently Using'].value_counts().head(5).sort_values(ascending=True)
        total_tools_responses = len(filtered_tools)
        st.markdown(f"### 🛠️ Popular AI Tools <span style='font-size: 14px; color: #888888;'>(Total: {total_tools_responses})</span>", unsafe_allow_html=True)
        
        # 計算工具使用的百分比
        tool_percentages = (tool_counts / total_tools_responses * 100).round(1)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=tool_counts.index,
            x=tool_percentages,  # 使用百分比而不是原始計數
            orientation='h',
            marker_color='#c5e1a5',
            text=[f'{pct}%' for pct in tool_percentages],  # 顯示百分比
            textposition='outside'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            height=400,
            margin=dict(l=30, r=50, t=20, b=20),  # 增加右邊距以容納標籤
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                title=None,
                range=[0, max(tool_percentages) * 1.2]  # 調整範圍以適應百分比
            ),
            yaxis=dict(
                showgrid=False,
                title=None
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    # Benefits Analysis
    benefits_data = client.get_benefit_wordcloud()
    filtered_benefits = benefits_data[
        benefits_data['AISent'] == user_selections.get('sentiment')
    ].head(5)
    
    total_benefits = len(filtered_benefits['AIBen'].value_counts())
    st.markdown(f"### 💡 Top Benefits Mentioned with Similar Sentiment <span style='font-size: 14px; color: #888888;'>(Total: {total_benefits})</span>", unsafe_allow_html=True)
    
    # 計算每個benefit的百分比
    benefits_total = filtered_benefits['count'].sum()
    benefit_cols = st.columns(5)
    for idx, (_, row) in enumerate(filtered_benefits.iterrows()):
        percentage = (row['count'] / benefits_total * 100).round(1)
        with benefit_cols[idx]:
            st.markdown(f"""
                <div class='metric-value'>{percentage}%</div>
                {row['AIBen']}
            """, unsafe_allow_html=True)

    # Navigation buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    if st.button("⏎ Start Over", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/1_home.py")


if __name__ == "__main__":
    main()