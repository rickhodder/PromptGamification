"""
My Prompts page - Browse and search prompt library
"""

import streamlit as st
from utils.storage import storage
from datetime import datetime


def show_my_prompts_page():
    """Display user's prompt library with search and filters"""
    
    st.title("📚 My Prompts")
    st.markdown("Browse, search, and manage your prompt collection.")
    
    # Get current user
    user_id = st.session_state.get("user_id", "demo_user")
    
    # Search and filter controls
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search",
            placeholder="Search prompts by text...",
            label_visibility="collapsed"
        )
    
    with col2:
        filter_templates = st.checkbox("Templates Only")
    
    with col3:
        sort_order = st.selectbox(
            "Sort",
            ["Newest", "Oldest", "Highest Rated"],
            label_visibility="collapsed"
        )
    
    # Tag filter
    all_prompts = storage.get_user_prompts(user_id)
    all_tags = set()
    for p in all_prompts:
        all_tags.update(p.tags)
    
    if all_tags:
        selected_tags = st.multiselect(
            "Filter by tags",
            options=sorted(list(all_tags)),
            placeholder="Select tags to filter..."
        )
    else:
        selected_tags = []
    
    st.markdown("---")
    
    # Get and filter prompts
    if search_query or selected_tags:
        prompts = storage.search_prompts(user_id, query=search_query, tags=selected_tags if selected_tags else None)
    else:
        prompts = all_prompts
    
    # Filter templates if requested
    if filter_templates:
        prompts = [p for p in prompts if p.is_template]
    
    # Sort prompts
    if sort_order == "Newest":
        prompts.sort(key=lambda x: x.created_at, reverse=True)
    elif sort_order == "Oldest":
        prompts.sort(key=lambda x: x.created_at)
    elif sort_order == "Highest Rated":
        prompts.sort(
            key=lambda x: sum([
                x.ratings.length, x.ratings.complexity, x.ratings.specificity,
                x.ratings.clarity, x.ratings.creativity, x.ratings.context
            ]) / 6,
            reverse=True
        )
    
    # Display count
    st.markdown(f"**Found {len(prompts)} prompt(s)**")
    
    # Display prompts
    if not prompts:
        st.info("No prompts found. Create your first prompt using **➕ Add Prompt**!")
    else:
        for prompt in prompts:
            display_prompt_card(prompt, user_id)


def display_prompt_card(prompt, user_id):
    """Display a single prompt as a card"""
    
    with st.expander(
        f"{'📋' if prompt.is_template else '📝'} {prompt.prompt_text[:80]}..." 
        if len(prompt.prompt_text) > 80 
        else f"{'📋' if prompt.is_template else '📝'} {prompt.prompt_text}",
        expanded=False
    ):
        # Prompt details
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("**Full Prompt:**")
            st.text_area(
                "Prompt",
                value=prompt.prompt_text,
                height=100,
                disabled=True,
                label_visibility="collapsed",
                key=f"prompt_text_{prompt.id}"
            )
            
            if prompt.description:
                st.markdown("**Description:**")
                st.write(prompt.description)
        
        with col2:
            # Metadata
            st.markdown("**Created:**")
            st.write(prompt.created_at.strftime("%Y-%m-%d %H:%M"))
            
            if prompt.tags:
                st.markdown("**Tags:**")
                for tag in prompt.tags:
                    st.markdown(f"🏷️ `{tag}`")
            
            st.markdown(f"**Sharing:** {prompt.sharing_preference}")
            
            if prompt.is_template:
                st.success("Template")
        
        # Show ratings if available
        avg_rating = sum([
            prompt.ratings.length, prompt.ratings.complexity, prompt.ratings.specificity,
            prompt.ratings.clarity, prompt.ratings.creativity, prompt.ratings.context
        ]) / 6
        
        if avg_rating > 0:
            st.markdown("---")
            st.markdown("**Quality Ratings:**")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                st.metric("Length", f"{prompt.ratings.length:.1f}")
            with col2:
                st.metric("Complex", f"{prompt.ratings.complexity:.1f}")
            with col3:
                st.metric("Specific", f"{prompt.ratings.specificity:.1f}")
            with col4:
                st.metric("Clarity", f"{prompt.ratings.clarity:.1f}")
            with col5:
                st.metric("Creative", f"{prompt.ratings.creativity:.1f}")
            with col6:
                st.metric("Context", f"{prompt.ratings.context:.1f}")
        
        # Reflection fields
        if prompt.what_i_learned or prompt.what_went_well:
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if prompt.what_i_learned:
                    st.markdown("**What I Learned:**")
                    st.write(prompt.what_i_learned)
            
            with col2:
                if prompt.what_went_well:
                    st.markdown("**What Went Well:**")
                    st.write(prompt.what_went_well)
        
        # Actions
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Copy to Clipboard", key=f"copy_{prompt.id}", use_container_width=True):
                st.code(prompt.prompt_text, language=None)
                st.success("Copied!")
        
        with col2:
            if st.button("✏️ Edit", key=f"edit_{prompt.id}", use_container_width=True):
                st.info("Edit feature coming soon!")
        
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{prompt.id}", type="secondary", use_container_width=True):
                if storage.delete_prompt(prompt.id):
                    st.success("Prompt deleted!")
                    st.rerun()
                else:
                    st.error("Failed to delete prompt")


if __name__ == "__main__":
    show_my_prompts_page()
