"""
Pytest configuration and fixtures
Includes AI mocking fixtures to prevent API costs during testing
"""

import pytest
import os
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock, patch

from models import Prompt, User, PromptRatings
from utils.storage import JSONStorage
from personas import PersonaFactory


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory for testing"""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return str(data_dir)


@pytest.fixture
def test_storage(temp_data_dir):
    """Create a test storage instance with temporary directory"""
    return JSONStorage(data_dir=temp_data_dir)


@pytest.fixture
def sample_prompt():
    """Create a sample prompt for testing"""
    return Prompt(
        user_id="test_user",
        prompt_text="Write a Python function that calculates factorial",
        description="A simple factorial calculator",
        what_i_learned="I learned to be more specific about edge cases",
        what_went_well="The prompt was clear and concise",
        tags=["python", "programming", "math"],
        is_template=False,
        sharing_preference="private",
        persona_used="beginner"
    )


@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    return User(
        user_id="test_user",
        username="Test User",
        email="test@example.com"
    )


@pytest.fixture
def mock_ai_review():
    """Mock AI review response to avoid API calls"""
    return {
        "suggested_prompt": "Write a well-documented Python function that calculates the factorial of a non-negative integer, including error handling for invalid inputs.",
        "questions": [
            "What should happen if the input is negative?",
            "Do you need to handle very large numbers?",
            "Should the function use recursion or iteration?"
        ],
        "refinements": [
            "Add input validation for negative numbers",
            "Specify the return type and parameter types",
            "Include docstring with examples",
            "Consider edge cases like 0! = 1"
        ],
        "ratings": {
            "length": 7.0,
            "complexity": 6.0,
            "specificity": 7.5,
            "clarity": 8.0,
            "creativity": 5.0,
            "context": 6.5
        },
        "feedback": "Good start! Your prompt is clear but could benefit from more specificity about edge cases and expected behavior."
    }


@pytest.fixture
def mock_persona(mock_ai_review):
    """Mock persona that returns predetermined responses"""
    with patch('personas.base_persona.BasePersona.review_prompt') as mock:
        mock.return_value = mock_ai_review
        yield mock


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client to prevent actual API calls"""
    with patch('openai.OpenAI') as mock_client:
        # Mock completion response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps({
            "suggested_prompt": "Improved prompt text",
            "questions": ["Question 1", "Question 2"],
            "refinements": ["Refinement 1", "Refinement 2"],
            "ratings": {
                "length": 8.0,
                "complexity": 7.0,
                "specificity": 8.5,
                "clarity": 9.0,
                "creativity": 6.0,
                "context": 7.5
            },
            "feedback": "Great prompt!"
        })
        
        mock_client.return_value.chat.completions.create.return_value = mock_response
        yield mock_client


@pytest.fixture(autouse=True)
def reset_session_state():
    """Reset any global state between tests"""
    # This can be expanded as needed
    yield
    # Cleanup after test


# Test data helpers

def create_test_prompts(storage, user_id, count=5):
    """Helper to create multiple test prompts"""
    prompts = []
    for i in range(count):
        prompt = Prompt(
            user_id=user_id,
            prompt_text=f"Test prompt {i+1}",
            description=f"Description for prompt {i+1}",
            tags=[f"tag{i%3+1}"],
            persona_used=["beginner", "intermediate", "advanced"][i % 3]
        )
        saved = storage.save_prompt(prompt)
        prompts.append(saved)
    return prompts
