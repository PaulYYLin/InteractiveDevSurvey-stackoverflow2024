import streamlit as st
# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Developers Survey Data Story",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={} # This removes the hamburger menu
)

# Add custom CSS with animations
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        section[data-testid="stSidebar"] {display: none;}
        
        /* Animations */
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        
        @keyframes slideIn {
            from {transform: translateY(30px); opacity: 0;}
            to {transform: translateY(0); opacity: 1;}
        }
        
        .tech-container {
            background-color: #1a1a2e;
            padding: 3rem;
            border-radius: 15px;
            margin: 3rem auto;
            max-width: 1000px;
            animation: fadeIn 1.5s ease-out;
        }
        
        .welcome-text {
            color: #c5e1a5;
            font-size: 3.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
            animation: slideIn 1s ease-out;
        }
        
        .tech-box {
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid #c5e1a5;
            border-radius: 10px;
            padding: 2rem;
            margin: 2rem 0;
        }
        
        .description {
            color: #ffffff;
            font-size: 1.5rem;
            line-height: 1.8;
            text-align: center;
            animation: slideIn 1.5s ease-out;
        }
        
        .tech-line {
            height: 2px;
            background: linear-gradient(90deg, transparent, #c5e1a5, transparent);
            margin: 2rem 0;
            animation: fadeIn 2s ease-out;
        }
        
        /* Streamlit Button Styling */
        .stButton > button {
            width: 100%;
            height: 80px;
            background-color: #1a1a2e;
            color: #c5e1a5;
            border: 2px solid #c5e1a5;
            border-radius: 10px;
            font-size: 20px;
            font-weight: bold;
            margin-top: 2rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #c5e1a5;
            color: #1a1a2e;
            transform: scale(1.02);
        }
        
        .stButton > button:active {
            transform: scale(0.98);
        }
        
        /* Add padding to the main container */
        .main {
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

def start_survey():
    st.switch_page("pages/1_home.py")

def main():
    # Display welcome screen
    st.markdown("""
        <div class="tech-container">
            <div class="welcome-text">
                Developers Survey Data Story
            </div>
            <div class="tech-line"></div>
            <div class="tech-box">
                <div class="description">
                    Based on Stack Overflow's 2024 Developer Survey - the largest and most comprehensive survey of people who code around the world.<br>
                    Explore insights about AI from developers worldwide.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create columns to center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Exploring", key="start_button", type="primary", use_container_width=True):
            st.switch_page("pages/1_home.py")

if __name__ == "__main__":
    main()