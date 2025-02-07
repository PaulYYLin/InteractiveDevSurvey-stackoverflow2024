import streamlit as st
import plotly.graph_objects as go
from utils.client import Client

def create_heatmap(data):
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='Greens',
        text=data.values.round(1),
        texttemplate='%{text}%',
        textfont={"size": 12},
        hoverongaps=False,
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='Take a look of how many people are in your age group and employment status!',
            font=dict(size=35),
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=50, b=50, l=50, r=50),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=12),
            gridcolor='rgba(255,255,255,0.1)',
        ),
        yaxis=dict(
            title='Age Group',
            tickfont=dict(size=12),
            gridcolor='rgba(255,255,255,0.1)',
        ),
        height=600
    )
    
    return fig

def change_page():
    # Save user selections to session state
    if 'Age' in st.session_state and 'Employment' in st.session_state:
        st.session_state.user_age = st.session_state.Age
        st.session_state.user_employment = st.session_state.Employment
        st.session_state.current_page = '3_doyouknow'

def main():
    # Initialize client
    client = Client()
    
    # Get combined distribution data
    distribution_data = client.get_age_employment_distribution()
    
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
            text-align: left;
        }
        .question-box {
            background-color: #1a1a2e;
            border: 2px solid #c5e1a5;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: white;
            height: 100%;
        }
        .question-container {
            margin-bottom: -1rem;
        }
        .next-button {
            text-align: right;
            padding: 1rem 0;
        }
        /* Add styles for selectbox */
        div[data-baseweb="select"] {
            width: 70% !important;
        }
        div[data-baseweb="select"] > div {
            width: 100% !important;
        }
        button {
            height: 80px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main content
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="title">Tell us more about yourself.</h1>', unsafe_allow_html=True)
    
    # Create two columns for inputs
    left_col, right_col = st.columns(2)

    
    
    # Left Column - Age Question
    with left_col:
        st.markdown('<div class="question-container">', unsafe_allow_html=True)
        st.markdown('<h4>What is your age?</h4>', unsafe_allow_html=True)
        age_options = list(distribution_data.index)
        st.selectbox("Select Your Age Group:", age_options, key="Age", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right Column - Employment Status Question
    with right_col:
        st.markdown('<div class="question-container">', unsafe_allow_html=True)
        st.markdown('<h4>Which best describes your current employment status?</h4>', unsafe_allow_html=True)
        employment_options = list(distribution_data.columns)
        st.selectbox("Select your employment status:", employment_options, key="Employment", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    # Add validation before showing the continue button
    if 'Age' in st.session_state and 'Employment' in st.session_state:
        st.markdown('<div class="next-button">', unsafe_allow_html=True)
        st.button("Continue ➤", 
                key="next_page",
                on_click=change_page,
                use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Create the heatmap
    heatmap = create_heatmap(distribution_data)
    st.plotly_chart(heatmap, use_container_width=True)
    
    # Add navigation button with custom styling
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()