import streamlit as st

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

    # Create two-column layout
    col1, col2 = st.columns([4, 1])

    with col1:
        # Title and main content
        st.markdown("""
            <h1>
                <span style="color: #c5e1a5; font-weight: bold;">Relationship with Coding & AI</span>
            </h1>
            <div style='font-size: 1.4rem; color: #ffffff; margin-top: 2rem;'>
                <p>
                    Different developers have varying relationships with coding and AI tools:
                </p>
                <ul style='margin-top: 1rem;'>
                    <li><span style="color: #c5e1a5;">Professional Developers</span> often see AI as a productivity enhancer</li>
                    <li><span style="color: #c5e1a5;">Students</span> view AI as a learning assistant</li>
                    <li><span style="color: #c5e1a5;">Hobby Programmers</span> use AI for exploration and creativity</li>
                </ul>
                <p style='margin-top: 2rem;'>
                    <span style="color: #c5e1a5; font-size: 30px;">But ... What are their thoughts on AI? 🔍 </span> <br>
                     Let’s dive into the data and explore key insights on AI adoption across the developer community! 🚀
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        if st.button("⏎ Previous Page", use_container_width=True):
            st.switch_page("pages/3_doyouknow.py")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Next Page ➤", use_container_width=True):
            st.switch_page("pages/5_selectrelationship.py")

if __name__ == "__main__":
    main()
