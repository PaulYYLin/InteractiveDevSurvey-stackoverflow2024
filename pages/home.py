import streamlit as st
import plotly.express as px
from utils.client import Client

def get_ai_usage_data():
    try:
        response = Client().get_AI_usage()
        print(response)
        return response
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def create_ai_usage_chart(df):
    # Correct color mapping
    color_map = {
        'Yes': '#c5e1a5',  # Green for "Yes"
        'No, and I don\'t plan to': '#2a2a2a',  # Dark gray for others
        'No, but I plan to soon': '#2a2a2a'
    }
    
    # Sort the dataframe to ensure consistent order
    df = df.sort_values('AISelect', ascending=False)
    
    fig = px.pie(df, 
                 values='percentage', 
                 names='AISelect',
                 title='How many developers are using AI?',
                 color_discrete_sequence=[color_map[name] for name in df['AISelect']],
                 height=600,
                 )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='#c5e1a5',
        font_color='#ffffff',
        title_x=0.02,  # Move title to left
        title={
            'font': {'size': 24},
            'xanchor': 'left'  # Align title text to left
        }
    )
    
    # Highlight the "Yes" slice with a pull-out effect and add separation lines
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=14,
        hole=0.3,
        marker=dict(line=dict(color='#000000', width=2))  # Add black separation lines
    )
    
    return fig

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Get AI usage data
    df = get_ai_usage_data()
    if df is not None:
        yes_percentage = round(df[df['AISelect'] == 'Yes']['percentage'].values[0],2)*100
    else:
        yes_percentage = "..."

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
        button {
            height: 80px;
        }
        </style>
    """, unsafe_allow_html=True)


    # Main content
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Create two columns for the layout
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.markdown('<div class="text-content">', unsafe_allow_html=True)
        st.markdown(f'<h1 class="title"><span style="color: #c5e1a5; font-weight: bold; font-size: 75px;">{yes_percentage}%</span>  of developers are leveraging AI to boost their workflow efficiency. <br><span style="color: #c5e1a5; font-weight: bold; font-size: 20px;">Based on the Developer Survey from StackOverflow 2024.</span></h1>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <h3>
                Curious to know how many developers like you are leveraging AI? 🚀?
            </h3>
        """, unsafe_allow_html=True)
        
        # Button logic
        st.button("➤ Discover how AI is shaping the way developers code, debug, and innovate! 🔍",
                 key="find_out", 
                 use_container_width=True,
                 on_click=change_page)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with right_col:
        if df is not None:
            chart = create_ai_usage_chart(df)
            st.plotly_chart(chart, use_container_width=True)

def change_page():
    st.session_state.current_page = 'knowmoreaboutyou'
    st.session_state.should_rerun = True

if __name__ == "__main__":
    main()