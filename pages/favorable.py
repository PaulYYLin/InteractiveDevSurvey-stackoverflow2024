import streamlit as st
import plotly.graph_objects as go
from utils.client import Client


def create_pie_chart(data):
    total = sum(data.values())
    percentages = {k: (v/total)*100 for k, v in data.items()}
    
    # Define color mapping
    color_map = {
        'Very favorable': '#c5e1a5',  # 淺綠色
        'Favorable': '#7cb342',       # 深綠色
        'Unsure': '#4a4a4a',  # 灰色
        'Unfavorable': '#2a2a2a',     # 深灰色
        'Very unfavorable': '#1a1a1a',
        'Indifferent': '#1a1a1a'  # 更深灰色
    }
    # Create colors list in the same order as the labels
    colors = [color_map[label] for label in percentages.keys()]
    
    fig = go.Figure(data=[go.Pie(
        labels=list(percentages.keys()),
        values=list(percentages.values()),
        hole=.3,
        texttemplate="%{label}: %{value:.1f}%",
        textfont=dict(size=14),
        marker=dict(
            colors=colors,  # Use the list of colors instead of the dictionary
            line=dict(color='#000000', width=2)
        ),
    )])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
    )
    
    return fig

def main():
    # Custom CSS for styling
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
        .info-box {
            background-color: #1a1a2e;
            border: 2px solid #c5e1a5;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: white;
        }
        .text-content {
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    client = Client()
    
    # 從 session state 獲取用戶選擇
    user_selections = st.session_state.get('user_selections', {})
    developer_status = user_selections.get('developer_status')
    education_level = user_selections.get('education_level')
    
    # 獲取數據並過濾
    favorable_data = client.get_favorable_on_edu_and_code()
    if developer_status and education_level:
        filtered_data = favorable_data[
            (favorable_data['MainBranch'] == developer_status) &
            (favorable_data['EdLevel'] == education_level)
        ]
    else:
        filtered_data = favorable_data
    
    sentiment_counts = filtered_data['AISent'].value_counts().to_dict()
    print("Filtered data:", filtered_data)
    print("Sentiment counts:", sentiment_counts)
    
    favorable_percentage = (
        sentiment_counts.get('Very favorable', 0) + 
        sentiment_counts.get('Favorable', 0)
    ) / sum(sentiment_counts.values()) * 100 if sentiment_counts else 0
    
    
    # Create two columns for the layout
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.markdown('<div class="text-content">', unsafe_allow_html=True)
        if developer_status and education_level:
            st.markdown(
                f'''<h2 class="title"><span style="color: #c5e1a5; font-weight: bold; font-size: 75px;">{favorable_percentage:.1f}%</span><br>of developers having
                <span style="color: #c5e1a5; font-weight: bold;">{education_level}</span> background who identified as
                <span style="color: #c5e1a5; font-weight: bold;">{developer_status}</span>
                find AI tools highly favorable in their development workflow.</h2>''',
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<h3 style="font-size: 30px;">Do you think AI tools are favorable in your development workflow?</h3>', unsafe_allow_html=True)
        user_sentiment = st.selectbox(
            label="",
            label_visibility="collapsed",
            placeholder="Share your opinion", 
            options=favorable_data['AISent'].dropna().unique(),
        )
        # Store the sentiment selection
        st.session_state['user_selections']['sentiment'] = user_sentiment

        if st.button(
            " ➤  Let's Find What They Think AI Tools Can Help with!   ", 
            key="next_page",
            use_container_width=True,
        ):
            # Store all user selections in session state
            st.session_state['user_selections'].update({
                'developer_status': developer_status,
                'education_level': education_level,
                'sentiment': user_sentiment
            })
            # Switch to the favorable page
            st.switch_page("pages/knowmoreaboutidea.py")
    
    with right_col:
        fig = create_pie_chart(sentiment_counts)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()