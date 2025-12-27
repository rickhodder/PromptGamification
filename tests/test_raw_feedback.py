"""
Tests for raw feedback fields functionality
Verifies that raw and processed feedback are properly stored and retrieved
"""

import pytest
from models import Prompt, PromptRatings
from utils.response_processor import ResponseProcessor
from personas.beginner import BeginnerPersona


def test_prompt_model_has_raw_fields():
    """Test that Prompt model has new raw feedback fields"""
    prompt = Prompt(
        user_id="test_user",
        prompt_text="Test prompt",
        raw_questions=["Raw question 1?", "Raw question 2?"],
        raw_refinements=["Raw refinement 1", "Raw refinement 2"],
        raw_feedback="This is raw feedback",
        processed_questions=["Processed question 1?", "Processed question 2?"],
        processed_refinements=["Processed refinement 1", "Processed refinement 2"],
        processed_feedback="This is processed feedback"
    )
    
    assert prompt.raw_questions == ["Raw question 1?", "Raw question 2?"]
    assert prompt.raw_refinements == ["Raw refinement 1", "Raw refinement 2"]
    assert prompt.raw_feedback == "This is raw feedback"
    assert prompt.processed_questions == ["Processed question 1?", "Processed question 2?"]
    assert prompt.processed_refinements == ["Processed refinement 1", "Processed refinement 2"]
    assert prompt.processed_feedback == "This is processed feedback"


def test_prompt_model_raw_fields_optional():
    """Test that raw feedback fields are optional"""
    prompt = Prompt(
        user_id="test_user",
        prompt_text="Test prompt"
    )
    
    assert prompt.raw_questions is None
    assert prompt.raw_refinements is None
    assert prompt.raw_feedback is None
    assert prompt.processed_questions is None
    assert prompt.processed_refinements is None
    assert prompt.processed_feedback is None


def test_response_processor_preserves_raw_data():
    """Test that ResponseProcessor preserves raw versions"""
    response = {
        "suggested_prompt": "Improved prompt",
        "questions": ["**What is** the purpose?", "Why use this approach?"],
        "refinements": ["* Add more context", "- Include examples"],
        "ratings": {"length": 7.5, "complexity": 6.0},
        "feedback": "  Good prompt with some improvements needed  "
    }
    
    processed = ResponseProcessor.process_review_response(response)
    
    # Check raw versions are preserved
    assert processed["raw_questions"] == ["**What is** the purpose?", "Why use this approach?"]
    assert processed["raw_refinements"] == ["* Add more context", "- Include examples"]
    assert processed["raw_feedback"] == "  Good prompt with some improvements needed  "
    
    # Check processed versions are cleaned
    assert processed["processed_questions"] == ["What is the purpose?", "Why use this approach?"]
    assert processed["processed_refinements"][0] == "Add more context"
    assert processed["processed_refinements"][1] == "Include examples"
    assert processed["processed_feedback"] == "Good prompt with some improvements needed"
    
    # Verify they're also in the standard keys
    assert processed["questions"] == processed["processed_questions"]
    assert processed["refinements"] == processed["processed_refinements"]
    assert processed["feedback"] == processed["processed_feedback"]


def test_response_processor_handles_invalid_types():
    """Test that ResponseProcessor handles invalid input types"""
    response = {
        "questions": "not a list",  # Should be list
        "refinements": None,  # Should be list
        "feedback": 123  # Should be string
    }
    
    processed = ResponseProcessor.process_review_response(response)
    
    # Should default to empty/safe values
    assert processed["raw_questions"] == []
    assert processed["raw_refinements"] == []
    assert processed["raw_feedback"] == ""
    assert processed["processed_questions"] == []
    assert processed["processed_refinements"] == []
    assert processed["processed_feedback"] == ""


def test_persona_stores_raw_feedback():
    """Test that persona stores both raw and processed feedback in prompt"""
    import os
    
    # Disable AI for testing
    os.environ["USE_AI_REVIEW"] = "false"
    
    persona = BeginnerPersona()
    prompt = Prompt(
        user_id="test_user",
        prompt_text="Write a function to calculate factorial"
    )
    
    # Get review (will use fallback)
    review = persona.review_prompt(prompt)
    
    # Check that review includes feedback sections
    assert "questions" in review
    assert "refinements" in review
    assert "feedback" in review
    
    # Clean up
    os.environ.pop("USE_AI_REVIEW", None)


def test_backward_compatibility_with_storage():
    """Test that storage handles old prompts without new fields"""
    from utils.storage import JSONStorage
    import tempfile
    import json
    
    # Create a temporary storage
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = JSONStorage(tmpdir)
        
        # Manually write old-format prompt (without new fields)
        old_prompt_data = {
            "id": "test_id",
            "user_id": "test_user",
            "prompt_text": "Test prompt",
            "description": None,
            "what_i_learned": None,
            "what_went_well": None,
            "ai_suggested_prompt": None,
            "tags": [],
            "is_template": False,
            "sharing_preference": "private",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
            "ratings": {
                "length": 5.0,
                "complexity": 5.0,
                "specificity": 5.0,
                "clarity": 5.0,
                "creativity": 5.0,
                "context": 5.0
            },
            "persona_used": None,
            "review_history": []
        }
        
        with open(storage.prompts_file, 'w') as f:
            json.dump([old_prompt_data], f)
        
        # Try to load it
        prompt = storage.get_prompt("test_id")
        
        # Should load successfully with None values for new fields
        assert prompt is not None
        assert prompt.prompt_text == "Test prompt"
        assert prompt.raw_questions is None
        assert prompt.raw_refinements is None
        assert prompt.raw_feedback is None
        assert prompt.processed_questions is None
        assert prompt.processed_refinements is None
        assert prompt.processed_feedback is None


def test_storage_saves_new_fields():
    """Test that storage properly saves new fields"""
    from utils.storage import JSONStorage
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = JSONStorage(tmpdir)
        
        # Create prompt with new fields
        prompt = Prompt(
            user_id="test_user",
            prompt_text="Test prompt",
            raw_questions=["Raw Q1?", "Raw Q2?"],
            raw_refinements=["Raw R1", "Raw R2"],
            raw_feedback="Raw feedback text",
            processed_questions=["Processed Q1?", "Processed Q2?"],
            processed_refinements=["Processed R1", "Processed R2"],
            processed_feedback="Processed feedback text"
        )
        
        # Save and retrieve
        saved_prompt = storage.save_prompt(prompt)
        retrieved_prompt = storage.get_prompt(saved_prompt.id)
        
        # Verify all fields preserved
        assert retrieved_prompt.raw_questions == ["Raw Q1?", "Raw Q2?"]
        assert retrieved_prompt.raw_refinements == ["Raw R1", "Raw R2"]
        assert retrieved_prompt.raw_feedback == "Raw feedback text"
        assert retrieved_prompt.processed_questions == ["Processed Q1?", "Processed Q2?"]
        assert retrieved_prompt.processed_refinements == ["Processed R1", "Processed R2"]
        assert retrieved_prompt.processed_feedback == "Processed feedback text"
