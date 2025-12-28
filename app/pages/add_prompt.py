"""
Add/Review Prompt page
Implements Use Case 1 from PRD
"""

import streamlit as st
from datetime import datetime
from models import Prompt, PromptRatings, ReviewHistoryEntry
from utils.storage import storage
from personas import PersonaFactory


def show_add_prompt_page():
    """Main function for Add/Review Prompt page"""
    
    st.title("➕ Add New Prompt")
    st.markdown("Add a prompt to your knowledge base and get expert AI feedback.")
    
    # Get current user
    user_id = st.session_state.get("user_id", "demo_user")
    selected_persona = st.session_state.get("selected_persona", "beginner")
    
    # Create form
    with st.form("add_prompt_form", clear_on_submit=False):
        st.subheader("Prompt Details")
        
        # Main prompt text
        prompt_text = st.text_area(
            "Prompt Text *",
            height=200,
            help="Enter your prompt here. This is the text you would give to an AI model.",
            placeholder="Example: Write a Python function that calculates the factorial of a number..."
        )
        
        # Description
        description = st.text_area(
            "Description (Optional)",
            height=100,
            help="Describe what this prompt is meant to accomplish",
            placeholder="This prompt is designed to..."
        )
        
        # Reflection fields
        col1, col2 = st.columns(2)
        
        with col1:
            what_i_learned = st.text_area(
                "What I Learned (Optional)",
                height=100,
                help="Reflect on what you learned from creating or using this prompt",
                placeholder="I learned that..."
            )
        
        with col2:
            what_went_well = st.text_area(
                "What Went Well (Optional)",
                height=100,
                help="What aspects of this prompt worked well?",
                placeholder="The prompt worked well because..."
            )
        
        # Tags
        tags_input = st.text_input(
            "Tags (Optional)",
            help="Enter tags separated by commas (e.g., python, code-generation, functions)",
            placeholder="python, code-generation, functions"
        )
        
        # Additional options
        col1, col2 = st.columns(2)
        
        with col1:
            sharing_preference = st.selectbox(
                "Sharing Preference *",
                options=["private", "public", "selective"],
                help="Control who can see this prompt"
            )
        
        with col2:
            is_template = st.checkbox(
                "Save as Template",
                help="Mark this prompt as a reusable template"
            )
        
        # Submit button
        submitted = st.form_submit_button("Save Prompt", type="primary", use_container_width=True)
        
        if submitted:
            if not prompt_text.strip():
                st.error("⚠️ Prompt text is required!")
            else:
                # Parse tags
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                
                # Create prompt object
                prompt = Prompt(
                    user_id=user_id,
                    prompt_text=prompt_text,
                    description=description if description else None,
                    what_i_learned=what_i_learned if what_i_learned else None,
                    what_went_well=what_went_well if what_went_well else None,
                    tags=tags,
                    is_template=is_template,
                    sharing_preference=sharing_preference,
                    persona_used=selected_persona
                )
                
                # Save to storage
                saved_prompt = storage.save_prompt(prompt)
                st.session_state.current_prompt = saved_prompt
                st.success("✅ Prompt saved successfully!")
                st.rerun()
    
    # Review section (only show if there's a current prompt)
    if "current_prompt" in st.session_state:
        st.markdown("---")
        show_review_section(st.session_state.current_prompt)


def show_review_section(prompt: Prompt):
    """Display AI review section for a prompt"""
    
    st.subheader("🤖 AI Review")
    
    # Persona selection for this review
    selected_persona = st.session_state.get("selected_persona", "beginner")
    persona_names = PersonaFactory.get_persona_names()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"**Current Persona:** {selected_persona.title()}")
    with col2:
        if st.button("Change Persona", use_container_width=True):
            st.session_state.show_persona_selector = True
    
    # Persona selector modal
    if st.session_state.get("show_persona_selector", False):
        with st.expander("Select Persona", expanded=True):
            personas = PersonaFactory.list_personas()
            for name, description in personas.items():
                if st.button(f"**{name.title()}**: {description}", key=f"persona_{name}", use_container_width=True):
                    st.session_state.selected_persona = name
                    st.session_state.show_persona_selector = False
                    st.rerun()
    
    # Review button
    if st.button("🔍 Get AI Review", type="primary", use_container_width=True):
        with st.spinner(f"Getting feedback from {selected_persona.title()} persona..."):
            # Get persona instance
            persona = PersonaFactory.get_persona(selected_persona)
            
            # Get review (placeholder for now - will integrate with AI API later)
            review = persona.review_prompt(prompt)
            
            # Store review in session state
            st.session_state.current_review = review
            st.rerun()
    
    # Display review if available
    if "current_review" in st.session_state:
        review = st.session_state.current_review
        
        # Overall Feedback
        st.markdown("### 💬 AI Feedback")
        
        # Create tabs for processed vs raw feedback
        tab1, tab2 = st.tabs(["📝 Processed Feedback", "🔍 Raw AI Response"])
        
        with tab1:
            feedback = review.get("feedback", "")
            if feedback:
                st.info(feedback)
            else:
                st.info("No processed feedback available.")
        
        with tab2:
            raw_feedback = review.get("raw_feedback", "")
            if raw_feedback:
                st.info(raw_feedback)
            else:
                st.info("No raw feedback available.")
        
        st.markdown("---")
        
        # Suggested prompt
        st.markdown("### 💡 Suggested Improvement")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Your Prompt:**")
            st.text_area("Original", value=prompt.prompt_text, height=150, disabled=True, key="orig_prompt")
        
        with col2:
            st.markdown("**AI Suggestion:**")
            suggested = review.get("suggested_prompt", prompt.prompt_text)
            st.text_area("Improved", value=suggested, height=150, disabled=True, key="sugg_prompt")
        
        # Apply suggestion button
        if st.button("✅ Apply Suggestion"):
            prompt.prompt_text = suggested
            prompt.ai_suggested_prompt = suggested
            storage.save_prompt(prompt)
            st.success("Suggestion applied!")
            st.rerun()
        
        st.markdown("---")
        
        # Clarifying questions
        st.markdown("### ❓ Clarifying Questions")
        
        # Create tabs for processed vs raw feedback
        tab1, tab2 = st.tabs(["📝 Processed Feedback", "🔍 Raw AI Response"])
        
        with tab1:
            st.markdown("##### Processed Questions")
            questions = review.get("questions", [])
            if questions:
                for i, question in enumerate(questions):
                    st.markdown(f"{i+1}. {question}")
                    answer = st.text_input(f"Your answer", key=f"answer_{i}", placeholder="Optional...")
            else:
                st.info("No clarifying questions provided.")
        
        with tab2:
            st.markdown("##### Raw Questions from AI")
            raw_questions = review.get("raw_questions", [])
            if raw_questions:
                for i, question in enumerate(raw_questions):
                    st.markdown(f"{i+1}. {question}")
            else:
                st.info("No raw questions available.")
        
        st.markdown("---")
        
        # Refinements
        st.markdown("### ✨ Suggested Refinements")
        
        # Create tabs for processed vs raw feedback
        tab1, tab2 = st.tabs(["📝 Processed Feedback", "🔍 Raw AI Response"])
        
        with tab1:
            st.markdown("##### Processed Refinements")
            refinements = review.get("refinements", [])
            selected_refinements = []
            if refinements:
                for i, refinement in enumerate(refinements):
                    if st.checkbox(refinement, key=f"refinement_{i}"):
                        selected_refinements.append(refinement)
                
                if selected_refinements and st.button("Apply Selected Refinements"):
                    st.success(f"Applied {len(selected_refinements)} refinement(s)!")
            else:
                st.info("No refinements provided.")
        
        with tab2:
            st.markdown("##### Raw Refinements from AI")
            raw_refinements = review.get("raw_refinements", [])
            if raw_refinements:
                for i, refinement in enumerate(raw_refinements):
                    st.markdown(f"{i+1}. {refinement}")
            else:
                st.info("No raw refinements available.")
        
        st.markdown("---")
        
        # Ratings
        st.markdown("### 📊 Quality Ratings")
        ratings = review.get("ratings", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Length", f"{ratings.get('length', 0):.1f}/10")
            st.metric("Complexity", f"{ratings.get('complexity', 0):.1f}/10")
        with col2:
            st.metric("Specificity", f"{ratings.get('specificity', 0):.1f}/10")
            st.metric("Clarity", f"{ratings.get('clarity', 0):.1f}/10")
        with col3:
            st.metric("Creativity", f"{ratings.get('creativity', 0):.1f}/10")
            st.metric("Context", f"{ratings.get('context', 0):.1f}/10")
        
        # Update prompt ratings
        if st.button("Save Ratings"):
            prompt.ratings.length = ratings.get('length', 0)
            prompt.ratings.complexity = ratings.get('complexity', 0)
            prompt.ratings.specificity = ratings.get('specificity', 0)
            prompt.ratings.clarity = ratings.get('clarity', 0)
            prompt.ratings.creativity = ratings.get('creativity', 0)
            prompt.ratings.context = ratings.get('context', 0)
            storage.save_prompt(prompt)
            st.success("Ratings saved!")
        
        st.markdown("---")
        
        # Feedback
        st.markdown("### 💬 Feedback")
        
        # Create tabs for processed vs raw feedback
        tab1, tab2 = st.tabs(["📝 Processed Feedback", "🔍 Raw AI Response"])
        
        with tab1:
            st.markdown("##### Processed Feedback")
            feedback = review.get("feedback", "")
            if feedback:
                st.info(feedback)
            else:
                st.info("No processed feedback available.")
        
        with tab2:
            st.markdown("##### Raw Feedback from AI")
            raw_feedback = review.get("raw_feedback", "")
            if raw_feedback:
                st.info(raw_feedback)
            else:
                st.info("No raw feedback available.")
            
            # Show full raw response in expander for debugging
            with st.expander("🔧 Debug: Full Raw Response"):
                st.json(review)
    
    # New prompt button
    st.markdown("---")
    if st.button("➕ Add Another Prompt", use_container_width=True):
        # Clear session state
        if "current_prompt" in st.session_state:
            del st.session_state.current_prompt
        if "current_review" in st.session_state:
            del st.session_state.current_review
        st.rerun()


if __name__ == "__main__":
    show_add_prompt_page()
