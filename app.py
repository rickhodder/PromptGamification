"""
Promptification - AI Prompt Engineering Gamification App
Main Streamlit application entry point
"""

import streamlit as st
from dotenv import load_dotenv
import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

# Import page modules
from app.pages.dashboard import show_dashboard_page
from app.pages.add_prompt import show_add_prompt_page
from app.pages.my_prompts import show_my_prompts_page
from utils.storage import storage
from personas import PersonaFactory

# Page configuration
st.set_page_config(
    page_title="Promptification",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = "demo_user"  # Simple auth for MVP
if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = os.getenv("DEFAULT_PERSONA", "beginner")

def main():
    """Main application function"""
    
    # Sidebar navigation
    st.sidebar.title("🎯 Promptification")
    st.sidebar.markdown("*Master AI Prompt Engineering*")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Dashboard", "➕ Add Prompt", "📚 My Prompts", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    # Display current user info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**User:** {st.session_state.user_id}")
    st.sidebar.markdown(f"**Active Persona:** {st.session_state.selected_persona.title()}")
    
    # Get user stats for sidebar
    user = storage.get_or_create_user(st.session_state.user_id)
    st.sidebar.markdown(f"**Total Prompts:** {user.stats.total_prompts}")
    st.sidebar.markdown(f"**Daily Goal:** {user.preferences.daily_goal}")
    
    # Main content area
    if page == "🏠 Dashboard":
        show_dashboard_page()
        
    elif page == "➕ Add Prompt":
        show_add_prompt_page()
        
    elif page == "📚 My Prompts":
        show_my_prompts_page()
        
    elif page == "⚙️ Settings":
        show_settings_page()

def show_settings_page():
    """Display settings page"""
    st.title("⚙️ Settings")
    
    user_id = st.session_state.get("user_id", "demo_user")
    user = storage.get_or_create_user(user_id)
    
    # Persona selection
    st.subheader("🎭 AI Persona")
    st.markdown("Choose your default AI mentor persona for prompt reviews.")
    
    personas = PersonaFactory.list_personas()
    persona_names = list(personas.keys())
    
    # Display persona options with descriptions
    selected_persona = st.session_state.selected_persona
    
    for name in persona_names:
        description = personas[name]
        is_selected = (name == selected_persona)
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{name.title()}**")
                st.markdown(f"*{description}*")
            with col2:
                if is_selected:
                    st.success("✓ Active")
                else:
                    if st.button("Select", key=f"select_{name}"):
                        st.session_state.selected_persona = name
                        user.preferences.default_persona = name
                        storage.save_user(user)
                        st.rerun()
            st.markdown("---")
    
    # Goals
    st.subheader("🎯 Daily Goals")
    st.markdown("Set your daily prompt creation targets.")
    
    daily_goal = st.number_input(
        "Prompts per day",
        min_value=1,
        max_value=20,
        value=user.preferences.daily_goal,
        help="How many prompts do you want to create each day?"
    )
    
    weekly_goal = st.number_input(
        "Prompts per week",
        min_value=1,
        max_value=100,
        value=user.preferences.weekly_goal,
        help="Your weekly target (usually daily goal × 7)"
    )
    
    if st.button("💾 Save Goals", type="primary"):
        user.preferences.daily_goal = daily_goal
        user.preferences.weekly_goal = weekly_goal
        storage.save_user(user)
        st.success(f"✅ Goals updated! Daily: {daily_goal}, Weekly: {weekly_goal}")
    
    st.markdown("---")
    
    # About
    st.subheader("ℹ️ About Promptification")
    st.markdown("""
    **Version:** 1.0.0 (MVP)
    
    Promptification is a gamified web application designed to help you improve your AI prompt engineering skills through practice, feedback, and structured learning.
    
    **Features:**
    - Add and review prompts with AI feedback
    - Four expert personas (Beginner, Intermediate, Advanced, Interviewer)
    - Track progress with analytics dashboard
    - Build a searchable prompt knowledge base
    - Set and achieve daily goals
    
    **Tech Stack:** Streamlit, Python, JSON storage
    """)

if __name__ == "__main__":
    main()
