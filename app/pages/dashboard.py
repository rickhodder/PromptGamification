"""
Dashboard page - Display user stats and analytics
"""

import streamlit as st
from utils.storage import storage
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from collections import Counter


def show_dashboard_page():
    """Display user dashboard with stats and analytics"""
    
    st.title("📊 Dashboard")
    st.markdown("Track your prompt engineering progress and improvement.")
    
    # Get current user
    user_id = st.session_state.get("user_id", "demo_user")
    user = storage.get_or_create_user(user_id, username=user_id)
    
    # Get all user prompts
    prompts = storage.get_user_prompts(user_id)
    
    # Update user stats
    user.stats.total_prompts = len(prompts)
    
    # Calculate week and month counts
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    user.stats.prompts_this_week = len([p for p in prompts if p.created_at >= week_ago])
    user.stats.prompts_this_month = len([p for p in prompts if p.created_at >= month_ago])
    
    # Calculate average rating
    if prompts:
        total_ratings = []
        for p in prompts:
            avg = sum([
                p.ratings.length, p.ratings.complexity, p.ratings.specificity,
                p.ratings.clarity, p.ratings.creativity, p.ratings.context
            ]) / 6
            if avg > 0:
                total_ratings.append(avg)
        user.stats.average_rating = sum(total_ratings) / len(total_ratings) if total_ratings else 0.0
    
    storage.save_user(user)
    
    # Display key metrics
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Prompts",
            user.stats.total_prompts,
            help="All-time prompt count"
        )
    
    with col2:
        st.metric(
            "This Week",
            user.stats.prompts_this_week,
            delta=f"{user.stats.prompts_this_week - user.preferences.daily_goal * 7} vs goal"
        )
    
    with col3:
        st.metric(
            "Daily Goal",
            user.preferences.daily_goal,
            help="Your daily target"
        )
    
    with col4:
        st.metric(
            "Avg Rating",
            f"{user.stats.average_rating:.1f}/10" if user.stats.average_rating > 0 else "N/A",
            help="Average quality rating across all prompts"
        )
    
    st.markdown("---")
    
    if not prompts:
        st.info("👋 Welcome to Promptification! Create your first prompt to start tracking your progress.")
        st.markdown("""
        ### Getting Started
        1. Click **➕ Add Prompt** in the sidebar
        2. Enter your prompt and get AI feedback
        3. Watch your skills improve over time!
        """)
        return
    
    # Prompts over time chart
    st.markdown("### 📅 Prompts Over Time")
    
    # Group prompts by date
    prompts_by_date = Counter([p.created_at.date() for p in prompts])
    
    if prompts_by_date:
        dates = sorted(prompts_by_date.keys())
        counts = [prompts_by_date[d] for d in dates]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=counts,
            mode='lines+markers',
            name='Prompts Per Day',
            line=dict(color='#1f77b4', width=3)
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Prompts Per Day",
            height=300,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Tag breakdown
    st.markdown("### 🏷️ Prompt Tags Breakdown")
    
    all_tags = []
    for p in prompts:
        all_tags.extend(p.tags)
    
    if all_tags:
        tag_counts = Counter(all_tags)
        
        fig = px.pie(
            values=list(tag_counts.values()),
            names=list(tag_counts.keys()),
            title="Distribution by Tags"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No tags yet. Add tags to your prompts to see distribution!")
    
    st.markdown("---")
    
    # Average ratings over time
    st.markdown("### ⭐ Quality Ratings Over Time")
    
    # Filter prompts with ratings
    rated_prompts = [p for p in prompts if sum([
        p.ratings.length, p.ratings.complexity, p.ratings.specificity,
        p.ratings.clarity, p.ratings.creativity, p.ratings.context
    ]) > 0]
    
    if rated_prompts:
        # Sort by date
        rated_prompts.sort(key=lambda x: x.created_at)
        
        dates = [p.created_at.date() for p in rated_prompts]
        avg_ratings = [sum([
            p.ratings.length, p.ratings.complexity, p.ratings.specificity,
            p.ratings.clarity, p.ratings.creativity, p.ratings.context
        ]) / 6 for p in rated_prompts]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=avg_ratings,
            mode='lines+markers',
            name='Average Rating',
            line=dict(color='#2ca02c', width=3)
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Average Rating (0-10)",
            yaxis_range=[0, 10],
            height=300,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Get AI reviews on your prompts to see quality ratings over time!")
    
    st.markdown("---")
    
    # Persona usage
    st.markdown("### 🎭 Persona Usage")
    
    persona_counts = Counter([p.persona_used for p in prompts if p.persona_used])
    
    if persona_counts:
        col1, col2, col3, col4 = st.columns(4)
        personas = ["beginner", "intermediate", "advanced", "interviewer"]
        cols = [col1, col2, col3, col4]
        
        for persona, col in zip(personas, cols):
            with col:
                count = persona_counts.get(persona, 0)
                st.metric(persona.title(), count)
    else:
        st.info("Persona usage will appear here as you create prompts.")


if __name__ == "__main__":
    show_dashboard_page()
