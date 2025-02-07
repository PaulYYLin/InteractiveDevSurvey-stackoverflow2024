import streamlit as st
from pages import 1_home, 2_knowmoreaboutyou, 3_doyouknow, 4_relationshiptocode, 5_selectrelationship, 6_favorable, 8_summary

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Developer Survey Analysis",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={} # This removes the hamburger menu
)

# Add custom CSS to hide the navigation menu and sidebar
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        section[data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Add auto rerun functionality
if 'should_rerun' not in st.session_state:
    st.session_state.should_rerun = False

def main():
    # Check if we need to rerun
    if st.session_state.get('should_rerun', False):
        st.session_state.should_rerun = False
        st.rerun()

    # Page routing
    if st.session_state.current_page == 'home':
        home.main()
    elif st.session_state.current_page == 'knowmoreaboutyou':
        knowmoreaboutyou.main()
    elif st.session_state.current_page == 'doyouknow':
        doyouknow.main()
    elif st.session_state.current_page == 'relationshiptocode':
        relationshiptocode.main()
    elif st.session_state.current_page == 'selectrelationship':
        selectrelationship.main()
    elif st.session_state.current_page == 'favorable':
        favorable.main()
    elif st.session_state.current_page == 'summary':
        summary.main()
    elif st.session_state.current_page == 'analysis':
        # Import analysis page only when needed
        from pages import analysis  
        analysis.main()

if __name__ == "__main__":
    main()