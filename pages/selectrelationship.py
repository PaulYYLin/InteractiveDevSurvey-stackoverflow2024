import streamlit as st
import plotly.graph_objects as go
from utils.client import Client

def main():
    client = Client()
    heatmap_data = client.get_edu_brain_for_heatmap()
    # Define options lists
    developer_options = heatmap_data.columns.tolist()

    education_options = heatmap_data.index.tolist()

    st.markdown(
            """
        <style>
        button {
            height: 80px;
            padding-top: 10px !important;
            padding-bottom: 10px !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )


    # Add page title and description
    st.title("""
    Tell us about your journey as a developer and your education background! 🚀
    """)
    
    # Create layout with two columns
    col1, col2 = st.columns([0.5, 0.5])

    # First column - Developer relationship question
    with col1:
        st.subheader("Developer Status")
        developer_index = st.selectbox(
            "Which of the following options best describes you today?*",
            options=developer_options,
            index=0
        )
        st.caption("*For the purpose of this survey, a developer is \"someone who writes code\"")

    # Second column - Education level question
    with col2:
        st.subheader("Education Level")
        education_index = st.selectbox(
            "What is your highest level of formal education completed?",
            options=education_options,
            index=0
        )

    # Add spacing before heatmap
    st.markdown("---")
    
    # Convert values to percentages
    total_responses = heatmap_data.values.sum()
    heatmap_data_percentage = (heatmap_data / total_responses * 100)

    # Create heatmap using plotly
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data_percentage.values,
        y=education_options,
        x=developer_options,
        colorscale='Greens',
        text=heatmap_data_percentage.values,
        texttemplate='%{text:.1f}%',
        textfont={"size": 12},
        hoverongaps=False,
    ))

    # Update layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=50, b=150, l=10, r=50),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=15),
            gridcolor='rgba(255,255,255,0.1)',
            ticktext=[label.replace(', ', ',<br>') for label in developer_options],
            tickvals=list(range(len(developer_options))),
            side='bottom'
        ),
        yaxis=dict(
            tickfont=dict(size=15),
            gridcolor='rgba(255,255,255,0.1)',
            ticktext=[label.split('(')[0] for label in education_options],
            tickvals=list(range(len(education_options))),
            side='left',
        ),
        height=600,
        coloraxis_colorbar=dict(
            title='Percentage',
            tickfont=dict(color='white'),
            title_font=dict(color='white'),
            ticksuffix='%'
        )
    )
    # Display heatmap
    st.markdown("""
        <h3 style='text-align: center;'>
            Curious to see how you compare with the Stackoverflow developer community? 🌍
        </h3>
        <p style='text-align: center;'>
            Check out the heatmap below to explore how developers from different backgrounds and education levels are shaping the future of tech! 🔥
        </p>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig, use_container_width=True)

    if st.button(
        " ➤ Let's Find Out Their Opinions!   ", 
        key="next_page",
        use_container_width=True,
    ):
        # Store user selections in session state
        st.session_state['user_selections'] = {
            'developer_status': developer_index,
            'education_level': education_index
        }
        # Switch to the favorable page
        st.switch_page("pages/favorable.py")
if __name__ == "__main__":
    main()